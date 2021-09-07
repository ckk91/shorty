"""
Routes for the shorty backend.
"""

import mongoengine
from mongoengine.errors import DoesNotExist, MultipleObjectsReturned
from backend.models import ShortUrl
from fastapi import HTTPException
from fastapi.routing import APIRouter
from fastapi.responses import RedirectResponse

from pydantic import BaseModel

from base64 import urlsafe_b64encode
from hashlib import sha1

import datetime
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
    try:
        ShortUrl.objects.get(url=payload.url)
    except MultipleObjectsReturned:
        pass
    except DoesNotExist:
        ShortUrl(url=payload.url, short_url=encoded).save()


    return {"short_url": encoded}


@router.get("/{short_url:str}")
def get_redirected(short_url: str):
    mongoengine.connect("shorty", username="root", password="example", authentication_source="admin")
    try:
        db_obj: ShortUrl = ShortUrl.objects.get(short_url=short_url)
    except MultipleObjectsReturned:
        db_obj: ShortUrl = ShortUrl.objects(short_url=short_url)[0]
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="URL not found.")
    
    db_obj.views.append(datetime.datetime.utcnow())
    db_obj.save()
    
    return RedirectResponse(url=db_obj.url)
