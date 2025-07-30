class NotFoundException(Exception):

    def __init__(self, message='The requested resource was not found.'):
        self.message = message
        self.status_code = 404
        self.status = 'Not Found'
        super().__init__(self.message)