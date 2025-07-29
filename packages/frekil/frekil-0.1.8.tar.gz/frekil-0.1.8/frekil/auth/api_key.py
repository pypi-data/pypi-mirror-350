"""
API Key authentication for the Frekil SDK
"""


class APIKeyAuth:
    """
    API Key authentication for the Frekil SDK

    Args:
        api_key (str): Your Frekil API key
    """

    def __init__(self, api_key):
        if not api_key:
            raise ValueError("API key is required")

        self.api_key = api_key
