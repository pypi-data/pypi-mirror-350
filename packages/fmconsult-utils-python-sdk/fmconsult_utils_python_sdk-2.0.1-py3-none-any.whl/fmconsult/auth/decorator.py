import sys, logging, jwt, mongoengine, bottle
from bottle import request, response
from .token_manager import TokenManager
from fmconsult.utils.configs import ConfigPropertiesHelper
from fmconsult.database.models.application import Application
from fmconsult.database.connection import DatabaseConnector

class AuthDecorator(object):
    def requires_auth(self, f):
        def decorated(*args, **kwargs):
            token = None
            token_manager = TokenManager()

            try:
                idx_localhost = bottle.request.url.index('127.0.0.1')
            except:
                try:
                    token = token_manager.get_jwt_token_from_header()
                except AuthorizationError as reason:
                    response.status = 401
                    response.headers['Content-Type'] = 'application/json'
                    return {'status': reason.code, 'message': reason.description}
                
                try:
                    token_decoded = token_manager.get_jwt_credetials()
                except jwt.ExpiredSignature:
                    response.status = 401
                    response.headers['Content-Type'] = 'application/json'
                    return {'status': 'ExpiredToken', 'message': 'Token is expired'}
                except jwt.DecodeError as message:
                    response.status = 401
                    response.headers['Content-Type'] = 'application/json'
                    return {'status': 'InvalidToken', 'message': str(message)}
            
            return f(*args, **kwargs)

        return decorated