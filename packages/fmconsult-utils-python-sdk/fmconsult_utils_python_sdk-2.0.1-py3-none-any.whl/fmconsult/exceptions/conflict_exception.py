class ConflictException(Exception):

    def __init__(self, message="A conflict occurred with the current state of the resource."):
        self.message = message
        self.status_code = 409
        self.status = 'Conflict'
        super().__init__(self.message)