from pydantic import BaseModel


class Item(BaseModel):
    id: str
    value: str


class BadUrl(Exception):
    pass


class InvalidToken(Exception):
    pass


class RateLimit(Exception):
    pass


class BadImage(Exception):
    pass


class FileLarge(Exception):
    pass


class ServerTimeout(Exception):
    pass
