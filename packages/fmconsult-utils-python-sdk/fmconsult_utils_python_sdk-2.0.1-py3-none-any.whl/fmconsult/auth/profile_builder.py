import time
from fmconsult.utils.configs import ConfigPropertiesHelper

class ProfileBuilder(object):
    def __init__(self):
        self.cph = ConfigPropertiesHelper()

    def build_profile(self, credentials):
        return {
            'user': credentials,
            'exp': time.time() + float(self.cph.get_property_value('JWT', 'jwt.expireoffset'))
        }