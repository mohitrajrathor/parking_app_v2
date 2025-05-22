# to crete custom errors

# imports


class APIError(Exception):
    def __init__(self, message, status_code=400, **kwargs):
        """
        Custom API error, to facilate API error handling with predefined schema with the use of flask_smorest abort
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.extra = kwargs
