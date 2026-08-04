"""
Formatting utilities for rendering strings and JSON outputs.
"""
import json

def format_currency(amount: float, symbol: str = "$") -> str:
    """Format a floating point number as currency."""
    return f"{symbol}{amount:,.2f}"


def format_json_response(data: dict, indent: int = 2) -> str:
    """Serialize dictionary to formatted JSON string."""
    return json.dumps(data, indent=indent, sort_keys=True)
