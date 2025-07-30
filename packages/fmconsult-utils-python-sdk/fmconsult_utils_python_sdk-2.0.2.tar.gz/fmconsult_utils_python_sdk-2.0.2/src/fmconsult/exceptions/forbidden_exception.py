class ForbiddenException(Exception):
  
    def __init__(self, message="The server understood the request, but refuses to authorize it."):
        self.message = message
        self.status_code = 403
        self.status = 'forbidden'
        super().__init__(self.message)