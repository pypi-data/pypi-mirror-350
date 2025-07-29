class InvalidCliendID(Exception):
    """
    Exception raised when the client ID is invalid.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidTaksID(Exception):
    """
    Exception raised when the task ID is invalid.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidStepID(Exception):
    """
    Exception raised when the step ID is invalid.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidOperation(Exception):
    """
    Exception raised when the operation is invalid.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class InvalidIDFormatException(Exception):
    """
    Exception raised when the ID format is invalid.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message

class InvalidDateFormatException(Exception):
    """
    Exception raised when the date format is invalid.
    """
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message