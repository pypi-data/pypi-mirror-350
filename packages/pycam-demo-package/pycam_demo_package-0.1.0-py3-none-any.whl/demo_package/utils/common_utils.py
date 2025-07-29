import uuid


def generate_uuid() -> str:
    """
    Generate a random string UUID4.
    
    :return str:
        The random uuid.
    """
    return uuid.uuid4().hex
