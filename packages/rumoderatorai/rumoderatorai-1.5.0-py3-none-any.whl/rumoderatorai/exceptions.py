import json

import re

from typing import Final


HEADER_REGEX: Final = re.compile(r"<h1>(.*?)</h1>")


def get_exception(code: int, body: str | dict) -> Exception:
    error: str

    try:
        body_json: dict = body if isinstance(body, dict) else json.loads(body)

        error = body_json.get("message", body)
    except json.JSONDecodeError:
        match = HEADER_REGEX.search(body)

        if match:
            error = match.group(1)
        else:
            error = body

    if code == 403:
        return Forbidden(error)
    elif code == 401:
        return InvalidToken(error)
    elif code == 400:
        return BadRequest(error)
    elif code == 402:
        return InsufficientBalance(error)
    elif code == 404:
        return NotFound(error)
    elif code == 500:
        return InternalServerError(error)
    else:
        return UnknownError(error)


class BaseError(Exception):
    """
        Base error
    """

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        if reccomendations := getattr(self, "reccomendations", None):
            return f"{self.message}\n\n{reccomendations}"

        return self.message


class UnknownError(BaseError):
    """
        Unknown error
    """


class Forbidden(BaseError):
    """
        Forbidden error
    """


class InternalServerError(BaseError):
    """
        Internal server error
    """

    reccomendations = "Try again later."


class InvalidToken(BaseError):
    """
        Internal server error
    """


class BadRequest(BaseError):
    """
        Bad request error
    """


class InsufficientBalance(BaseError):
    """
        Insufficient balance error
    """

    reccomendations = "Please top up your balance in https://t.me/RuModeratorAI_API_Bot bot."


class NotFound(BaseError):
    """
        Not found error
    """


class TimeoutError(BaseError):
    """
        Timeout error
    """

    reccomendations = "Please check your internet connection."
