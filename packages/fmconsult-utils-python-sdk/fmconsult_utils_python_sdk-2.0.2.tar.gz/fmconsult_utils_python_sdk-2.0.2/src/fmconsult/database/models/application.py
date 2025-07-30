# -*- coding: utf-8 -*-
import json
from mongoengine import *
from mongoengine.fields import StringField, ListField
from .base import CustomBaseDocument

class Application(CustomBaseDocument):
	meta = {
		'collection': 'applications',
		'db_alias': 'security'
	}
	
	name = StringField()
	token = StringField()
	client_ids = ListField(default=[])
	api_name = StringField()
	
	def to_dict(self):
		json_string = {
			"name": self.name,
			"token": self.token,
			"client_ids": self.client_ids,
			"api_name": self.api_name,
		}

		return json.dumps(json_string, default=str)