class UnauthorizedException(Exception):
    def __init__(self, message="Unauthorized access"):
        self.message = message
        self.status_code = 401
        self.status = 'unauthorized'
        super().__init__(self.message)