"""
Utility functions for data validation and string manipulation.
"""

def is_valid_email(email: str) -> bool:
    """Basic email validity check."""
    if not isinstance(email, str):
        return False
    return "@" in email and "." in email and not email.startswith("@")


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp a numerical value within [min_val, max_val]."""
    return max(min_val, min(value, max_val))
