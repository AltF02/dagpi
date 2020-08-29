# app = FastAPI(docs_url=None, redoc_url=None)
from pydantic import BaseModel


class Message(BaseModel):
    message: str


rdict = {
    400: {
        "message": Message,
        "content": {
            "application/json": {
                "example": {"error": "We were unable to use the link your provided."}
            }
        },
    },
    500: {
        "message": Message,
        "content": {
            "application/json": {
                "example": {"error": "The Image manipulation had a small error"}
            }
        },
    },
    401: {
        "message": Message,
        "content": {"application/json": {"example": {"error": "Invalid token"}}},
    },
    429: {
        "message": Message,
        "content": {"application/json": {
            "example": {"error": "You are being ratelimited. Please stick to 60 requests per minute"}}},
    },
    415: {
        "message": Message,
        "content": {"application/json": {"example": {"error": "There was no image at your url"}}},
    },
    413: {
        "message": Message,
        "content": {"application/json": {
            "example": {"error": "The image your provided was too large. Please use files under 10 Mb"}}},
    },
    408: {
        "message": Message,
        "content": {"application/json": {"example": {
            "error": "The time taken to connect to the image server and download the image was too long."}}},
    },
    422: {"message": Message},
    200: {
        "message": Message,
        "content": {
            "application/json": {
                "example": {"success": True, "url": "http://dagpi.tk/bin/LezddANR4N.png"}
            }
        },
    },
}