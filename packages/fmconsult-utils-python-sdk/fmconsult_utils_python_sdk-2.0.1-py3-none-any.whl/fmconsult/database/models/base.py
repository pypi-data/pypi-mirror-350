from datetime import datetime
from mongoengine.queryset import QuerySet
from mongoengine.document import Document
from mongoengine.fields import BooleanField, DateTimeField

class CustomQuerySet(QuerySet):
	def to_json(self):
		return "[%s]" % (",".join([doc.to_json() for doc in self]))
	def to_json_all(self):
		return "[%s]" % (",".join([doc.to_json_all() for doc in self]))

class CustomBaseDocument(Document):
    meta = { 'queryset_class': CustomQuerySet, 'abstract': True }

    created_at  = DateTimeField(default=datetime.now)
    updated_at  = DateTimeField()
    deleted_at  = DateTimeField()
    deleted     = BooleanField(default=False)
    active      = BooleanField(default=True)
    inactive_at = DateTimeField()

    def set_all_values(self, data):
        for attr in data:
            if hasattr(self, attr):
                setattr(self, attr, data[attr])