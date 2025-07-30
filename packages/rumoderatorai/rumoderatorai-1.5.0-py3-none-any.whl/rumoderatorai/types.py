from dataclasses import dataclass
from typing import Dict, List, Optional

from .data import API_VERSION

from .utils import urljoin


@dataclass
class Config:
    """
        Config
    """

    api_key: str | None = None
    _base_url: str = "https://moderator.omni-devel.ru"

    text_classification_model: str = "bert"
    profile_classification_model: str = "profiles_antispam_bert"
    image_classification_model: str = "nsfw_detector"

    @property
    def base_url(self) -> str:
        if not self._base_url.endswith(f"/api/{API_VERSION}"):
            return urljoin(self._base_url, f"/api/{API_VERSION}")
        return self._base_url


@dataclass
class BasicResponse:
    """
        Basic response class for all API responses
    """

    ok: bool
    code: int
    message: str

    def __str__(self):
        return f"""BasicResponse(
    ok={self.ok},
    code={self.code},
    message="{self.message}"
)"""


@dataclass
class TextClassResponse(BasicResponse):
    """
        Text classification response
    """

    label: int
    time_taken: float
    class_names: Dict[str, str]
    confidence: float
    model_id: str
    unique_id: str
    balance: float
    tokens_count: int
    price: float

    def __str__(self):
        return f"""TextClassResponse(
    ok={self.ok},
    code={self.code},
    message="{self.message}",
    label={self.label},
    time_taken={self.time_taken},
    class_names={self.class_names},
    confidence={self.confidence},
    model_id={self.model_id},
    unique_id="{self.unique_id}",
    balance={self.balance},
    tokens_count={self.tokens_count},
    price={self.price}
)"""


@dataclass
class TokenizeResponse(BasicResponse):
    """
        Text tokenization response
    """

    tokens: list[str]

    def __str__(self):
        return f"""TokenizeResponse(
    ok={self.ok},
    code={self.code},
    message="{self.message}",
    tokens={self.tokens}
)"""


@dataclass
class ImageClassResponse(BasicResponse):
    """
        Image classification response
    """

    label: int
    time_taken: float
    class_names: Dict[str, str]
    confidence: float
    balance: float
    price: float

    def __str__(self):
        return f"""ImageClassResponse(
    ok={self.ok},
    code={self.code},
    message="{self.message}",
    label={self.label},
    time_taken={self.time_taken},
    class_names={self.class_names},
    confidence={self.confidence},
    balance={self.balance},
    price={self.price}
)"""


@dataclass
class Stat:
    """
        Statistic class
    """

    date: str
    money_spent: float
    queries: int

    def __str__(self):
        return f"Stat(date=\"{self.date}\", money_spent={self.money_spent}, queries={self.queries})"


@dataclass
class StatsResponse(BasicResponse):
    """
        Stats response
    """

    stats: List[Stat]
    date_format: str

    def __str__(self):
        stats_str = ",\n\t".join(str(stat) for stat in self.stats)
        return f"""StatsResponse(
    ok={self.ok},
    code={self.code},
    message="{self.message}",
    stats=[
        {stats_str}
    ],
    date_format="{self.date_format}"
)"""


@dataclass
class KeyInfoResponse(BasicResponse):
    """
        Key info response
    """

    balance: float

    def __str__(self):
        return f"""KeyInfoResponse(
    ok={self.ok},
    code={self.code},
    message="{self.message}",
    balance={self.balance}
)"""

@dataclass
class PredictionResponse(BasicResponse):
    """
        Prediction response
    """

    text: str
    label: int
    confidence: float
    model: str

    def __str__(self):
        text = self.text.replace("\n", "\\n")
        return f"""PredictionResponse(
    ok={self.ok},
    code={self.code},
    message="{self.message}",
    text="{text}",
    label={self.label},
    confidence={self.confidence},
    model="{self.model}"
)"""


@dataclass
class IpsResponse(BasicResponse):
    """
        List of IPs who used the API key
    """

    ips: List[str]

    def __str__(self):
        ips_str = ",\n\t".join(f"\"{ip}\"" for ip in self.ips)
        return f"""IpsResponse(
    ok={self.ok},
    code={self.code},
    message="{self.message}",
    ips=[
        {ips_str}
    ]
)"""


@dataclass
class Model:
    name: str
    price: float
    class_names: dict[int, str]

    def __str__(self):
        return f"""Model(
    name="{self.name}",
    price={self.price} per 128 tokens,
    class_names={self.class_names}
)"""


@dataclass
class PricesResponse(BasicResponse):
    """
        Prices response
    """

    text_classification: List[Model]
    image_classification: List[Model]
    profile_classification: List[Model]
    ocr: float

    def __str__(self):
        text_classification_str = ",\n\t".join(str(model).replace("\n", "\n\t") + "," for model in self.text_classification)
        image_classification_str = ",\n\t".join(str(model).replace("\n", "\n\t") + "," for model in self.image_classification)
        profile_classification_str = ",\n\t".join(str(model).replace("\n", "\n\t") + "," for model in self.profile_classification)
        return f"""PricesResponse(
    ok={self.ok},
    code={self.code},
    message="{self.message}",
    text_classification=[
        {text_classification_str}
    ],
    image_classification=[
        {image_classification_str}
    ],
    profile_classification=[
        {profile_classification_str}
    ],
    ocr={self.ocr} per 128 pixels
)"""


@dataclass
class OcrResponse(BasicResponse):
    """
        OCR response
    """

    text: str
    num_of_pixels: int
    price: float 
    balance: float
    time_taken: float

    def __str__(self):
        text = self.text.replace("\n", "\\n")
        return f"""OcrResponse(
    ok={self.ok},
    code={self.code},
    message="{self.message}",
    text="{text}",
    num_of_pixels={self.num_of_pixels},
    price={self.price},
    balance={self.balance},
    time_taken={self.time_taken}
)"""


@dataclass
class HTTPResponse:
    """
        HTTP response
    """

    json: dict
    status: int


@dataclass
class ChatContext:
    """
        Chat context
    """

    title: str
    topic_title: Optional[str] = None


@dataclass
class Context:
    """
        Context for moderation model
    """

    chat_context: Optional[ChatContext] = None
    allowed_rules: Optional[List[str]] = None

    def to_dict(self) -> dict:
        result = {}
        if self.chat_context:
            result["chat"] = self.chat_context.__dict__
        if self.allowed_rules:
            result["allowed_rules"] = self.allowed_rules

        return result
