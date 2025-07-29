"""
Base exception classes for the Frekil SDK
"""


class FrekilError(Exception):
    """Base exception for all Frekil SDK errors"""

    pass


class FrekilAPIError(FrekilError):
    """Exception raised for API errors (5xx)"""

    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code if response else None

        try:
            self.error_details = response.json() if response else None
        except (ValueError, AttributeError):
            self.error_details = None


class FrekilClientError(FrekilError):
    """Exception raised for client errors (4xx)"""

    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code if response else None

        try:
            self.error_details = response.json() if response else None
        except (ValueError, AttributeError):
            self.error_details = None
