import sys, logging
import mongoengine
from bottle import request, response
from fmconsult.utils.configs import ConfigPropertiesHelper
from fmconsult.database.models.application import Application
from fmconsult.database.connection import DatabaseConnector

class AuthDecorator(object):
	required_headers = {
		'x-api-token': {
			'type': 'str'
		}
	}

	def __init__(self, additional_required_headers=None):
		if not additional_required_headers is None:
			for header in additional_required_headers:
				self.required_headers[header] = additional_required_headers[header]

	def require_auth(self, func):
		def decorated(*args, **kwargs):
			db_connector = None
			try:
				logging.info('getting headers from request...')
				for header in self.required_headers:
					value = request.headers.get(header, None)

					if not value:
						raise Application.DoesNotExist(f"{header} not found in headers")
				
					self.required_headers[header]['value'] = value
				
				logging.info(self.required_headers)

				token = self.required_headers['x-api-token']['value']
 
				logging.info('iniatlizing database connector...')
				db_connector = DatabaseConnector('API-SECURITY')
				try:
					logging.info('try getting connection to security database...')
					mongoengine.get_connection(alias='security')
				except mongoengine.ConnectionFailure:
					logging.info('failed to connect to security database. creating new connection...')
					db_connector.connect(db_alias='security')

				cph = ConfigPropertiesHelper()
				api_name = cph.get_property_value('SELF', 'self.api.name')

				logging.info(f'find exists token: {token} from application: {api_name}')

				application = None
 
				try:
					logging.info('try getting application from database...')
					application = Application.objects.get(token=token, api_name=api_name)

				except Exception as e:
					try:
						logging.info('try getting connection to security database again...')
						mongoengine.get_connection(alias='security')
					except mongoengine.ConnectionFailure:
						logging.info('failed to connect to security database. creating new connection again...')
						db_connector.connect(db_alias='security')

						logging.info('try getting application from database again...')
						application = Application.objects.get(token=token, api_name=api_name)
				
				if application is None:
					apps = Application.objects.filter()
					logging.info(f'found {len(apps)} applications in database \o/...')
					raise Application.DoesNotExist(f"{token} not found in database or error in connection to database...")

				for header in self.required_headers:
					if not (header == 'x-api-token'):
						header_type = self.required_headers[header]['type']
						header_field = self.required_headers[header]['field']
						header_value = self.required_headers[header]['value']

						logging.info(f'find exists header: {header_field} in database')
						
						db_field_value = getattr(application, header_field)
						
						logging.info(f'validating db value: {db_field_value} with header value: {header_value}')

						if header_type == 'str':
							if not (str(header_value) == str(db_field_value)):
								raise Application.DoesNotExist(f"{header}:{header_value} does not match to the provided token {token}")

						if header_type == 'list':
							db_items = set(str(item) for item in db_field_value)
							header_values_list = [str(value.strip()) for value in header_value.split(',')]
       
							for header_value in header_values_list:
								if header_value not in db_items:
									raise Application.DoesNotExist(f"{header}:{header_value} does not match any of the provided tokens")

					logging.info('api protection process successfully!')
			except Application.DoesNotExist as e:
				response.status = 401
				response.headers['Content-Type'] = 'application/json'
				logging.error(e)
				message = 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)
				logging.error(message)
				return {'status': 'Unauthorized', 'message': str(message)}
			
			except Exception as e:
				response.status = 500
				response.headers['Content-Type'] = 'application/json'
				logging.error(e)
				message = 'Error ocurred: {msg} on {line}'.format(msg=str(e), line=sys.exc_info()[-1].tb_lineno)
				logging.error(message)
				return {'status': 'Error', 'message': str(message)}
		
			return func(*args, **kwargs)
		
		return decorated