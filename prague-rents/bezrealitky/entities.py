from datetime import datetime
from dataclasses import dataclass
from dacite import from_dict
from mongoengine import Document, EmbeddedDocument, IntField, StringField, BooleanField, FloatField, \
    EmbeddedDocumentField, DictField, DateTimeField
from mongo_utils import update_modified


class Coordinates(EmbeddedDocument):
    lat = FloatField(required=True)
    lon = FloatField(required=True)


@update_modified.apply
class BezrealitkyListing(Document):
    listing_id = IntField(required=True)
    uri = StringField(required=True)
    title = StringField(required=True)
    sub_title = StringField(required=True)
    coordinates = EmbeddedDocumentField(Coordinates)
    info = DictField()
    active = BooleanField(default=True)
    created_on = DateTimeField(default=datetime.utcnow)
    modified_on = DateTimeField(default=datetime.utcnow)

    meta = {'collection': 'bezrealitky'}


@dataclass
class BezrealitkyListingBaseDto:
    id: int = None
    uri: str = None

    @classmethod
    def from_dict(cls, data):
        data['id'] = int(data['id'])
        return from_dict(cls, data)
