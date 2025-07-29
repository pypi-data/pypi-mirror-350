"""
Base API class for all Frekil API endpoints
"""


class BaseAPI:
    """
    Base API class for all Frekil API endpoints

    Args:
        client (FrekilClient): The Frekil client instance
    """

    def __init__(self, client):
        self.client = client
