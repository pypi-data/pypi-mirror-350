"""String utility functions."""

import re
import unicodedata


def slugify(text: str) -> str:
    """Convert a string to a slug.

    Args:
        text: The text to convert

    Returns:
        A slug version of the text
    """
    # Convert to lowercase and normalize unicode characters
    text = unicodedata.normalize("NFKD", text.lower())

    # Remove non-alphanumeric characters
    text = re.sub(r"[^a-z0-9]+", "-", text)

    # Remove leading/trailing hyphens
    text = text.strip("-")

    return text
