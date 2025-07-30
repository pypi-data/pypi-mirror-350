import bottle, jwt
from bottle import request
from fmconsult.utils.configs import ConfigPropertiesHelper
from fmconsult.exceptions.authorization import AuthorizationError
from .profile_builder import ProfileBuilder

class TokenManager(object):
    def __init__(self):
        self.cph = ConfigPropertiesHelper()

    def get_jwt_token_from_header(self):
        auth = bottle.request.headers.get('Authorization', None)
        if not auth:
            raise AuthorizationError(code='authorization_header_missing', description='Authorization header is expected')

        parts = auth.split()

        if parts[0].lower() != 'bearer':
            raise AuthorizationError(code='invalid_header', description='Authorization header must start with Bearer')
        elif len(parts) == 1:
            raise AuthorizationError(code='invalid_header', description='Token not found')
        elif len(parts) > 2:
            raise AuthorizationError(code='invalid_header', description='Authorization header must be Bearer token')
        
        return parts[1]


    def get_jwt_credetials(self):
        token       = self.get_jwt_token_from_header()
        secret_key  = self.cph.get_property_value('JWT', 'jwt.secret')
        algorithm   = self.cph.get_property_value('JWT', 'jwt.algorithm')

        return jwt.decode(token, secret_key, algorithms=[algorithm])

    def get_access_token(self, credentials):
        builder = ProfileBuilder()
        profile     = builder.build_profile(credentials)
        secret_key  = self.cph.get_property_value('JWT', 'jwt.secret')
        algorithm   = self.cph.get_property_value('JWT', 'jwt.algorithm')

        return jwt.encode(profile, secret_key, algorithm=algorithm)