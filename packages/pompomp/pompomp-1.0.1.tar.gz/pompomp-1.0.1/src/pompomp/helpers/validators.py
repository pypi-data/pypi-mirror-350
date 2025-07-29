"""Basic email validation utility."""
import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    """Check if the provided email string is in a valid format."""
    return EMAIL_REGEX.fullmatch(email.strip()) is not None
