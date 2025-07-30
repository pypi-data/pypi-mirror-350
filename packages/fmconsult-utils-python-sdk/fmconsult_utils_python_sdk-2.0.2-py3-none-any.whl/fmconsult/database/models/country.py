# -*- coding: utf-8 -*-
import json
from mongoengine import *
from mongoengine.fields import StringField, EmbeddedDocumentListField
from .base import CustomBaseDocument

class Country(CustomBaseDocument):
    meta = { 'collection': 'countries' }

    name = StringField()
    code = StringField()

    def to_dict(self):
        json_string = {
            'id': str(self.id),
            'name': self.name,
            'code': self.code,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'updated_at': self.updated_at.strftime("%Y-%m-%d %H:%M:%S") if self.updated_at is not None else None,
            'deleted_at': self.deleted_at.strftime("%Y-%m-%d %H:%M:%S") if self.deleted_at is not None else None,
            'deleted': self.deleted
        }
        return json.dumps(json_string, default=str)