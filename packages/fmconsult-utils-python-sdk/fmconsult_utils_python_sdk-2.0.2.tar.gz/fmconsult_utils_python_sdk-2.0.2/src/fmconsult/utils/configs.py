import configparser

class ConfigPropertiesHelper(object):
	config = None
	
	def __init__(self, config_path='config/configs.ini'):
		self.config = configparser.ConfigParser()
		self.config.read(config_path)
	
	def get_property_value(self, section, property):
		return self.config.get(section, property)