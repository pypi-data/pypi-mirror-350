"""
Helper functions for the Frekil SDK
"""
import uuid


def validate_uuid(id_value):
    """
    Validate if a string is a valid UUID

    Args:
        id_value (str): The string to validate

    Returns:
        bool: True if the string is a valid UUID, False otherwise
    """
    try:
        uuid_obj = uuid.UUID(str(id_value))
        return str(uuid_obj) == str(id_value)
    except (ValueError, AttributeError, TypeError):
        return False
