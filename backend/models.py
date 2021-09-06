import mongoengine

class ShortUrl(mongoengine.Document):
    url = mongoengine.StringField(required=True)
    short_url = mongoengine.StringField(required=True)
    views = mongoengine.ListField(mongoengine.DateTimeField()) # TODO python-dateutil