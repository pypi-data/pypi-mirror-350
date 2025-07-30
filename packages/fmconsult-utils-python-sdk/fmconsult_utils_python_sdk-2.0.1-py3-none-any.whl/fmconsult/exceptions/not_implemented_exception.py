class NotImplementedException(Exception):

    def __init__(self, message='This functionality is not yet available.'):
        self.message = message
        self.status_code = 501
        self.status = 'Not Implemented'
        super().__init__(self.message)