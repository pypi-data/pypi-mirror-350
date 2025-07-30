import aiohttp
import asyncio

from pathlib import Path
from typing import Any

import base64
from io import BytesIO
from PIL import Image

from .utils import urljoin

import logging

import time

from . import types
from .types import HTTPResponse
from .data import __version__, HEADERS

from .exceptions import get_exception, TimeoutError


logger = logging.getLogger(__name__)


class Client:
    def __init__(
        self,
        api_key: str,
        base_url: str | None = None,
        default_text_classification_model: str | None = None,
        default_profile_classification_model: str | None = None,
        default_image_classification_model: str | None = None,
    ):
        """
        Initialize the client

        Args:
            api_key (str): API key
            base_url (str | None): Base URL of the API
            default_text_classification_model (str | None): Default text classification model
            default_profile_classification_model (str | None): Default profile classification model
            default_image_classification_model (str | None): Default image classification model
        """
        assert isinstance(api_key, str), "`api_key` must be a string"

        self._cfg = types.Config(
            api_key=api_key,
        )

        if base_url:
            self._cfg._base_url = base_url
        if default_text_classification_model:
            self._cfg.text_classification_model = default_text_classification_model
        if default_profile_classification_model:
            self._cfg.profile_classification_model = default_profile_classification_model
        if default_image_classification_model:
            self._cfg.image_classification_model = default_image_classification_model

        self._session: aiohttp.ClientSession | None = None

    @property
    def session(self) -> aiohttp.ClientSession:
        """
        Get the session
        """
        if self._session is None:
            raise ValueError(
                "Session is not initialized, use `.init()` method to initialize it"
            )

        logger.debug("Session successfully returned")

        return self._session

    async def init(self):
        """
        Initialize the session
        """
        self._session = aiohttp.ClientSession()
        
        try:
            await self._check_connection()
            await self._check_lib_version()
            
            logger.debug("Client initialized")
        except Exception as e:
            await self._session.close()
            self._session = None
            raise e

    async def close(self):
        """
        Close the session
        """
        if self._session:
            await self.session.close()
            self._session = None
    
    async def _check_connection(self):
        """
        Check the connection to the API
        """
        max_retries = 3
        retry_delay = 1.0
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                async with self.session.post(self._url("/ping", non_api=True), json={}) as response:
                    if response.status != 200:
                        exception = get_exception(response.status, await response.text())
                        raise exception
                end_time = time.time()
                
                logger.debug(f"Ping took {end_time - start_time:.3f} seconds")
                return
            except Exception as e:
                last_exception = e
                if attempt < max_retries - 1:
                    logger.warning(f"Connection attempt {attempt+1} failed: {str(e)}. Retrying in {retry_delay} seconds...")
                    await asyncio.sleep(retry_delay)
                    retry_delay *= 2
        
        # Если все попытки провалились
        logger.error(f"Failed to connect after {max_retries} attempts")
        raise last_exception

    async def _check_lib_version(self):
        """
        Check the library version
        """
        async with self.session.post(
            self._url("/check_python_lib_version"), json={"version": __version__}
        ) as response:
            if response.status != 200:
                logger.warning((await response.json())["message"])

    async def __aenter__(self):
        await self.init()

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.session.close()

        del self.session
        del self._cfg

    def _url(self, path: str, non_api: bool = False) -> str:
        """
        Get the full URL for the given path

        Args:
            path (str): Path to append to the base URL

        Returns:
            str: Full URL
        """
        return urljoin(self._cfg._base_url if non_api else self._cfg.base_url, path)

    def _json(self, **kwargs) -> dict:
        """
        Create a JSON payload for the API request

        Args:
            **kwargs: Keyword arguments to include in the JSON payload

        Returns:
            dict: JSON payload
        """
        return {**kwargs}

    @property
    def _headers(self) -> dict:
        """
        Create a headers payload for the API request
        """
        headers = HEADERS.copy()
        headers["Authorization"] = f"Bearer {self._cfg.api_key}"

        return headers

    def _preprocess_response(self, response: dict, dataclass: Any) -> Any:
        """
        Preprocess the API response

        Args:
            response (dict): API response
            dataclass (Any): Dataclass to parse the response into

        Returns:
            Any: Parsed response
        """
        if "class" in response:
            response["label"] = response["class"]
            del response["class"]

        if "model" in response and dataclass == types.TextClassResponse:
            response["model_id"] = response["model"]
            del response["model"]

        if "class_names" in response:
            response["class_names"] = {
                int(k): v for k, v in response["class_names"].items()
            }

        if "stats" in response:
            response["stats"] = [types.Stat(**stat) for stat in response["stats"]]
        
        if "ips" in response:
            response["ips"] = list(set(response["ips"]))

        if dataclass == types.PricesResponse:
            response["text_classification"] = [
                types.Model(
                    name=model["name"],
                    price=model["price"],
                    class_names={int(k): v for k, v in model["class_names"].items()},
                )
                for model in response["text_classification"]
            ]
            response["image_classification"] = [
                types.Model(
                    name=model["name"],
                    price=model["price"],
                    class_names={int(k): v for k, v in model["class_names"].items()},
                )
                for model in response["image_classification"]
            ]
            response["profile_classification"] = [
                types.Model(
                    name=model["name"],
                    price=model["price"],
                    class_names={int(k): v for k, v in model["class_names"].items()},
                )
                for model in response["profile_classification"]
            ]

        if not response.get("ok", False):
            raise get_exception(response["code"], response)

        try:
            return dataclass(**response)
        except Exception as e:
            raise ValueError(f"Failed to parse response from the API: {e}")
        finally:
            logger.debug("Response successfully parsed")
    
    async def _get(self, path: str, json: dict = {}) -> HTTPResponse:
        """
        Send GET request
        """
        for i in range(12):
            try:
                async with self.session.get(self._url(path), headers=self._headers, json=self._json(**json)) as response:
                    if response.status == 408:
                        raise asyncio.TimeoutError()

                    return HTTPResponse(await response.json(), response.status)
            except asyncio.TimeoutError:
                logger.error(f"A timeout error has occurred. We wait 15 seconds before reconnecting. Attempt: {i}")
                await asyncio.sleep(15)

        raise TimeoutError("The attempt to connect to the server is taking too long.")
    
    async def _post(self, path: str, json: dict = {}) -> HTTPResponse:
        """
        Send POST request
        """
        for i in range(12):
            try:
                async with self.session.post(self._url(path), headers=self._headers, json=self._json(**json)) as response:
                    if response.status == 408:
                        raise asyncio.TimeoutError()

                    return HTTPResponse(await response.json(), response.status)
            except asyncio.TimeoutError:
                logger.error(f"A timeout error has occurred. We wait 15 seconds before reconnecting. Attempt: {i}")
                await asyncio.sleep(15)

        raise TimeoutError("The attempt to connect to the server is taking too long.")

    async def get_text_class(self, text: str, context: types.Context | None = None, model: str | None = None) -> types.TextClassResponse:
        """
        Get the label of the text

        Args:
            text (str): Text to classify
            context (types.Context | None): Context to use
            model (str | None): Model to use

        Returns:
            classes.TextClassResponse: Text classification response
        """
        if model is None:
            model = self._cfg.text_classification_model

        data = {"text": text, "model": model}

        if context:
            data["context"] = context.to_dict()

        response = await self._post("/predict/text", json=data)
        return self._preprocess_response(
            response.json, types.TextClassResponse
        )

    async def get_text_tokenization(self, text: str, context: types.Context | None = None, model: str | None = None) -> types.TokenizeResponse:
        """
        Tokenize the text

        Args:
            text (str): Text to classify
            context (types.Context | None): Context to use
            model (str | None): Model to use

        Returns:
            classes.TokenizeResponse: Text tokenization response
        """
        if model is None:
            model = self._cfg.text_classification_model

        data = {"text": text, "model": model}

        if context:
            data["context"] = context.to_dict()

        response = await self._post("/tokenize/text", json=data)
        return self._preprocess_response(
            response.json, types.TokenizeResponse
        )

    async def get_profile_class(
        self,
        *,
        first_name: str,
        last_name: str | None = None,
        username: str | None = None,
        description: str | None = None,
        channel_title: str | None = None,
        is_premium: bool = False,
        model: str | None = None
    ) -> types.TextClassResponse:
        """
        Get the label of the profile

        Args:
            username (str | None): Username
            first_name (str): First name
            last_name (str | None): Last name
            description (str | None): Description
            channel_title (str | None): Personal channel title
            is_premium (bool): Whether the user has Telegram Premium
            model (str | None): Model to use

        Returns:
            classes.TextClassResponse: Profile classification response
        """
        if model is None:
            model = self._cfg.profile_classification_model

        data = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "description": description,
            "channel_title": channel_title,
            "is_premium": is_premium,
            "model": model,
        }

        response = await self._post("/predict/profile", json=data)
        return self._preprocess_response(
            response.json, types.TextClassResponse
        )

    async def get_image_class(
        self, image: Image.Image | Path | str, model: str | None = None
    ) -> types.ImageClassResponse:
        """
        Get the label of the image

        Args:
            image (PIL.Image.Image | Path | str): Image or path to the image to classify
            model (str | None): Model to use

        Returns:
            classes.ImageClassResponse: Image classification response
        """
        if model is None:
            model = self._cfg.image_classification_model

        if isinstance(image, Path | str):
            image = Image.open(image)

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        data = {"image": img_str, "model": model}

        buffered.close()

        response = await self._post("/predict/image", json=data)
        return self._preprocess_response(
            response.json, types.ImageClassResponse
        )
    
    async def get_ocr(self, image: Image.Image | Path | str) -> types.OcrResponse:
        """
        Get the OCR of the image

        Args:
            image (PIL.Image.Image | Path | str): Image or path to the image to OCR

        Returns:
            classes.OcrResponse: OCR response
        """
        if isinstance(image, Path | str):
            image = Image.open(image)

        buffered = BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        data = {
            "image": img_str
        }

        response = await self._post("/predict/ocr", json=data)
        return self._preprocess_response(
            response.json, types.OcrResponse
        )

    async def get_multimodal_text_class(self, text: str | None = None,
                                        images: list[Image.Image | Path | str] | None = None,
                                        context: types.Context | None = None,
                                        model: str | None = None) -> types.TextClassResponse:
        """
        Get the label of the multimodal text

        Args:
            text (str | None): Text to classify
            images (list[PIL.Image.Image | Path | str] | None): Images to classify
            context (types.Context | None): Context to use
            model (str | None): Model to use

        Returns:
            classes.TextClassResponse: Multimodal text classification response
        """
        if model is None:
            model = self._cfg.text_classification_model

        images, _images = [], images
        for image in _images:
            if isinstance(image, Path | str):
                image = Image.open(image)
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            images.append(base64.b64encode(buffered.getvalue()).decode())
            buffered.close()
        
        del _images

        assert text or images, "Either text or images must be provided"

        data = {
            "text": text,
            "images": images,
            "model": model
        }

        if context:
            data["context"] = context.to_dict()

        response = await self._post("/predict/multimodal_text", json=data)
        return self._preprocess_response(response.json, types.TextClassResponse)

    async def get_stats(self, limit: int = 3) -> types.StatsResponse:
        """
        Get stats

        Args:
            limit (int): Number of hours to get stats for

        Returns:
            classes.StatsResponse: Stats response
        """
        data = {"limit": limit}

        response = await self._get("/stats", json=data)
        return self._preprocess_response(
            response.json, types.StatsResponse
        )

    async def get_key_info(self) -> types.KeyInfoResponse:
        """
        Get info about your API key

        Returns:
            classes.KeyInfoResponse: Key info response
        """
        response = await self._get("/key")
        return self._preprocess_response(
            response.json, types.KeyInfoResponse
        )

    async def get_prediction(self, unique_id: str) -> types.PredictionResponse:
        """
        Get the prediction by unique ID

        Args:
            unique_id (str): Unique ID

        Returns:
            classes.PredictionResponse: Prediction response
        """
        response = await self._get("/prediction", json=self._json(unique_id=unique_id))
        return self._preprocess_response(
            response.json, types.PredictionResponse
        )

    async def get_ips(self) -> types.IpsResponse:
        """
        Get IPs who have used your API key

        Returns:
            classes.IpsResponse: IPs response
        """
        response = await self._get("/ips")
        return self._preprocess_response(response.json, types.IpsResponse)

    async def get_prices(self) -> types.PricesResponse:
        """
        Get prices

        Returns:
            classes.PricesResponse: Prices response
        """
        response = await self._get("/price")
        return self._preprocess_response(
            response.json, types.PricesResponse
        )
