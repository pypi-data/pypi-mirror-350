from enum import Enum

class DataCastUtil:
	
	def parse_to_string(self, _object, _field):
		if _field in _object:
			_object[_field] = str(_object[_field])
		return _object

	def parse_fields_to_string(self, _object, _fields):
		for _field in _fields:
			_object = self.parse_to_string(_object, _field)
		return _object

class JSONCastUtil:

	@staticmethod
	def serialize_enum(obj):
		if isinstance(obj, Enum):
			return obj.value
		raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")