from typing import List


class UploadException(BaseException):
    def __init__(self, status: str, message: str, error_code: str, errors: List):
        self.status = status
        self.message = message
        self.error_code = error_code
        self.errors = errors
