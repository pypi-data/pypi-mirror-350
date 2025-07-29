"""Transliterate Chechen text from Cyrillic to Latin script."""

from ._transliterator import Transliterator

from importlib.metadata import version
__version__ = version(__name__)

# Create a default instance for simple use cases
_default_transliterator = Transliterator()

# Main entry point function
def transliterate(text: str) -> str:
    """Transliterate Chechen text from Cyrillic to Latin script.
    
    This is the main entry point for the library. Simply import and use:
    
    >>> import ce_translit
    >>> result = ce_translit.transliterate("...")
    
    Args:
        text: The text in Cyrillic script to transliterate.
        
    Returns:
        The transliterated text in Latin script.
    """
    return _default_transliterator.transliterate(text)

# Export the class for advanced use cases
__all__ = ["transliterate", "Transliterator"]