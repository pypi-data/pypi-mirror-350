import logging, jsonpickle, requests
from enum import Enum
from http import HTTPMethod
from requests.exceptions import ConnectionError, ChunkedEncodingError
from fmconsult.exceptions.bad_request_exception import BadRequestException
from fmconsult.exceptions.unavailable_exception import UnavailableException
from fmconsult.exceptions.not_found_exception import NotFoundException
from fmconsult.exceptions.unauthorized_exception import UnauthorizedException
from fmconsult.exceptions.conflict_exception import ConflictException
from fmconsult.utils.configs import ConfigPropertiesHelper

class ContentType(Enum):
  APPLICATION_JSON = 'application/json'
  TEXT_PLAIN = 'text/plain'

class ApiBase(object):
  def __init__(self, additional_headers=None):
    self.logging_level = None
    try:
      self.cph = ConfigPropertiesHelper()
      self.logging_level = self.cph.get_property_value('SELF', 'self.logging.level')
    except:
      logging.warning('Logging level not found in config file')
      pass

    self.headers = { 
      'x-api-token': self.api_token
    }

    if not(additional_headers is None):
      for header in additional_headers:
        self.headers[header] = additional_headers[header]

  def __make_request(self, req_args):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Define o timeout, ajustável conforme a necessidade
            res = requests.request(**req_args, timeout=60)
            res.raise_for_status() # Verifica se ocorreu algum erro HTTP
            return res
        except (ConnectionError, ChunkedEncodingError) as e:
            logging.error(f"Connection error occurred: {e}. Retrying {attempt + 1}/{max_retries}...")
            if attempt == max_retries - 1:
                raise # Lança a exceção se o limite de tentativas for atingido
        except requests.exceptions.RequestException as e:
            logging.error(f"An error occurred: {e}")
            raise # Lança qualquer outra exceção que não for de conexão

  def call_request(self, http_method:HTTPMethod, request_url, params=None, payload=None, content_type:ContentType=ContentType.APPLICATION_JSON):
    try:
      logging.info(f'{str(http_method).upper()} url:')
      logging.info(request_url)

      self.headers['Content-Type'] = content_type.value
      
      if not(self.logging_level is None) and self.logging_level == 'DEBUG':
        logging.info(f'{str(http_method).upper()} headers:')
        logging.info(jsonpickle.encode(self.headers))

      # Verifica se há parâmetros a serem enviados na URL
      if not params is None:
        if not(self.logging_level is None) and self.logging_level == 'DEBUG':
          logging.info(f'{str(http_method).upper()} params:')
          logging.info(jsonpickle.encode(params))

      # Log do payload (apenas se for POST ou PUT)
      if not payload is None:
        if not(self.logging_level is None) and self.logging_level == 'DEBUG':
          logging.info(f'{str(http_method).upper()} payload:')
          if content_type == ContentType.APPLICATION_JSON:
            logging.info(jsonpickle.encode(payload))
          else:
            logging.info(payload)

      # Configuração dos parâmetros para requisição
      req_args = {
        'method': http_method,
        'url': request_url,
        'headers': self.headers
      }

      if params:
        req_args['params'] = params

      if payload:
        if content_type == ContentType.APPLICATION_JSON:
          req_args['json'] = payload
        else:
          req_args['data'] = payload
      
      if not(self.logging_level is None) and self.logging_level == 'DEBUG':
        logging.info(f'request args:')
        logging.info(req_args)

      res = self.__make_request(req_args)
      
      if res.status_code == 503:
        raise UnavailableException()
      elif res.status_code == 404:
        raise  NotFoundException(res.content)
      elif res.status_code == 409:
        raise ConflictException(res.content)
      elif res.status_code == 401:
        raise UnauthorizedException(res.content)
      elif res.status_code == 400:
        raise BadRequestException(res.content)
      elif res.status_code != 200:
        raise Exception(res.content)
        
      res = res.content.decode('utf-8')

      if not(self.logging_level is None) and self.logging_level == 'DEBUG':
        logging.info(f'{str(http_method).upper()} response:')
        logging.info(jsonpickle.encode(res))
      
      return res
    except UnavailableException as e:
      raise e
    except BadRequestException as e:
        raise e
    except NotFoundException as e:
        raise e
    except Exception as e:
        raise e