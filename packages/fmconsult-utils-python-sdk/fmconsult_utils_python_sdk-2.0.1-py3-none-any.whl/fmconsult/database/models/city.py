# -*- coding: utf-8 -*-
import json
from mongoengine import *
from mongoengine.fields import StringField, EmbeddedDocumentListField
from .base import CustomBaseDocument

class City(CustomBaseDocument):
    meta = { 'collection': 'cities' }

    name = StringField()
    code = StringField()
    country_code = StringField()
    state_code = StringField()

    def to_dict(self):
        json_string = {
            'id': str(self.id),
            'name': self.name,
            'code': self.code,
            'country_code': self.country_code,
            'state_code': self.state_code,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at is not None else None,
            'deleted_at': self.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if self.deleted_at is not None else None,
            'deleted': self.deleted
        }
        return json.dumps(json_string, default=str)