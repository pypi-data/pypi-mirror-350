class BadRequestException(Exception):

    def __init__(self, message="he request is malformed or missing required parameters"):
        self.message = message
        self.status_code = 400
        self.status = 'bad request'
        super().__init__(self.message)