def validate_message(message):
    """Sample validation function for a message."""
    if not message:
        raise ValueError("Message cannot be empty")
    return True
