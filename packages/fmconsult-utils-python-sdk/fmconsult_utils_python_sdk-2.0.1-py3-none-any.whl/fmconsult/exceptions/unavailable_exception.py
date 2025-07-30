class UnavailableException(Exception):
    
    def __init__(self, message="Service Temporarily Unavailable"):
        self.message = message
        self.status_code = 503
        self.status = 'unavailable'
        super().__init__(self.message)