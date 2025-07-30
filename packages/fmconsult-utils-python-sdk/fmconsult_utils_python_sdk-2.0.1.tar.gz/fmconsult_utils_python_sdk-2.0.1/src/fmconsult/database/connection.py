import logging, mongoengine
from fmconsult.utils.configs import ConfigPropertiesHelper

class DatabaseConnector:
  def __init__(self, db_section='MONGODB'):
    self.cph = ConfigPropertiesHelper()

    self.mongodb_environment = self.cph.get_property_value(db_section, 'mongodb.environment')
    self.mongodb_host = self.cph.get_property_value(db_section, f'mongodb.host.{self.mongodb_environment}')
    self.mongodb_user = self.cph.get_property_value(db_section, 'mongodb.user')
    self.mongodb_pass = self.cph.get_property_value(db_section, 'mongodb.pass')
    self.mongodb_name = self.cph.get_property_value(db_section, 'mongodb.database.name')

  def connect(self, db_alias='default'):
    try:
      if self.mongodb_host == 'localhost':
        mongoengine.connect(self.mongodb_name, alias=db_alias)
        logging.info(f"successful connection to local database '{self.mongodb_name}'.")
      else:
        dbqs = f'mongodb+srv://{self.mongodb_user}:{self.mongodb_pass}@{self.mongodb_host}/{self.mongodb_name}?retryWrites=true&w=majority'
        mongoengine.connect(host=dbqs, alias=db_alias)
        logging.info(f"successful connection to remote database '{self.mongodb_name}' in '{self.mongodb_host}'")
    except Exception as e:
      error_message = str(e)
      logging.info(f"error connecting to database: {error_message}")
      raise e
      
  def disconnect(self, db_alias='default'):
    try:
      mongoengine.disconnect(alias=db_alias)
      logging.info(f"disconnected from mongodb with alias {db_alias}.")
    except Exception as e:
      logging.error('error disconnecting from mongodb.')
      logging.error(e)
