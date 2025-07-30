"""Styles module for CV PDFs."""

from .base_style import CVStyle
from .classic_style import ClassicStyle


def get_style(style_name: str) -> CVStyle:
    """Get a CV style by name.

    Args:
        style_name: Name of the style

    Returns:
        CVStyle object

    Raises:
        ValueError: If the style name is not valid
    """
    styles = {
        "classic": ClassicStyle,
    }

    if style_name.lower() not in styles:
        valid_styles = ", ".join(styles.keys())
        raise ValueError(
            f"Invalid style name: {style_name}. Valid styles are: {valid_styles}"
        )

    return styles[style_name.lower()]()
