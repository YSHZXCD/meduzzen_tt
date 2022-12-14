class ModelException(Exception):
    def __init__(self, message, code=500):
        self.message = message
        self.code = code
        super().__init__(message)


class ViewException(ModelException):
    pass
