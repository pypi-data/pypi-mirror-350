"""Base CVStyle class."""

from abc import ABC, abstractmethod

from reportlab.lib.styles import StyleSheet1, getSampleStyleSheet


class CVStyle(ABC):
    """Base class for CV styling."""

    def __init__(self) -> None:
        """Initialize the style."""
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    @abstractmethod
    def _setup_styles(self) -> None:
        """Setup the styles. Should be implemented by subclasses."""
        pass

    def get_styles(self) -> StyleSheet1:
        """Get the styles dictionary."""
        return self.styles
