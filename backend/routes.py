"""
Routes for the shorty backend.
"""

import mongoengine
from backend.models import ShortUrl
from fastapi import HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse

from pydantic import BaseModel

from base64 import urlsafe_b64encode
from hashlib import sha1

router = APIRouter()

pseudodb = {
    "foo": "https://www.google.de"
}

@router.get("/")
def get_app_description():
    return {
        "name": "SHORTY",
        "description": "An URL shortener"
    }

class URLSchema(BaseModel):
    url: str

class ShortenResponse(BaseModel):
    short_url: str

@router.put("/shorten", response_model=ShortenResponse)
def put_shorten(payload: URLSchema):
    # inspo : https://stackoverflow.com/a/2510733
    enc=sha1(payload.url.encode()).digest()[:10]
    encoded = urlsafe_b64encode(enc).decode().rstrip("=")
    # pseudodb[encoded] = payload.url
    # TODO user and pass from container as scratchpad. remove
    # TODO ensure unique url
    mongoengine.connect("shorty", username="root", password="example", authentication_source="admin")
    url = ShortUrl(url=payload.url, short_url=encoded)
    url.save()


    return {"short_url": encoded}


@router.get("/{short_url:str}")
def get_redirected(short_url: str):
    url = pseudodb.get(short_url)
    if url is None:
        raise HTTPException(status_code=404, detail="URL not found.")
    
    return RedirectResponse(url=url)
