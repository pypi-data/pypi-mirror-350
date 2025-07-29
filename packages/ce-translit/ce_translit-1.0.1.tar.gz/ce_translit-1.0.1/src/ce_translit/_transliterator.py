"""Core transliteration logic for the ce_translit package."""

import json
import re
import unicodedata
from importlib import resources
from typing import Final, Iterable, Mapping, Optional

# Constants for data file
_DATA_FILE: Final[str] = "cyrl_latn_map.json"

# Load default mapping at import time
with resources.files("ce_translit.data").joinpath(_DATA_FILE).open(encoding="utf-8") as fh:
    _DEFAULT_DATA: Final[dict] = json.load(fh)

# Module-level constants for default configuration
DEFAULT_MAPPING: Final[Mapping[str, str]] = _DEFAULT_DATA["mapping"]
DEFAULT_BLACKLIST: Final[frozenset[str]] = frozenset(_DEFAULT_DATA["blacklist"])
DEFAULT_UNSURELIST: Final[frozenset[str]] = frozenset(_DEFAULT_DATA["unsurelist"])


class Transliterator:
    """Transliterate Chechen text from Cyrillic to Latin script using the Chechen Latin alphabet.
    
    This class allows customization of the transliteration rules by providing
    custom mapping, blacklist, and unsurelist.
    """
    
    def __init__(
        self,
        mapping: Optional[Mapping[str, str]] = None,
        blacklist: Optional[Iterable[str]] = None,
        unsurelist: Optional[Iterable[str]] = None,
    ) -> None:
        """Initialize the transliterator with custom or default configuration.
        
        Args:
            mapping: Custom cyrillic-to-latin mapping. If None, uses default.
            blacklist: Words that should not have special 'н' ending handling.
            unsurelist: Words that should have 'ŋ[REPLACE]' ending.
        """
        self._mapping = mapping if mapping is not None else DEFAULT_MAPPING
        self._blacklist = (
            frozenset(blacklist) if blacklist is not None 
            else DEFAULT_BLACKLIST
        )
        self._unsurelist = (
            frozenset(unsurelist) if unsurelist is not None 
            else DEFAULT_UNSURELIST
        )
    
    def _transliterate_word(self, word: str) -> str:
        """Convert a single word from Cyrillic to Latin script.
        
        Args:
            word: A single word in Cyrillic script.
            
        Returns:
            The word transliterated to Latin script.
        """
        result = ''
        i = 0
        
        while i < len(word):
            match = None
            
            has_next_letter = i + 1 < len(word)
            next_letter = word[i + 1] if has_next_letter else None
            has_pre_letter = i > 0
            pre_letter = word[i - 1] if has_pre_letter else None

            # Check all case variations (3 chars, 2 chars, 1 char)
            for key in [
                word[i:i + 3],
                word[i:i + 2],
                word[i:i + 1],
            ]:
                # Handle 'ъ' and 'Ъ' before 'е', 'ё', 'ю', 'я' and their uppercase versions
                # The lower() method is used to ensure the comparison is case-insensitive.
                if key.lower() == 'ъ' and has_next_letter and next_letter.lower() in 'еёюя':
                    if has_pre_letter and pre_letter.lower() == 'к': # and after 'к'
                        match = 'q̇' if key.islower() else 'Q̇'  # match to 'къ'
                    else:
                        match = ''  # else skip 'ъ'
                elif key.lower() == 'е':
                    # 'е' can be 'ye' or 'e' depending on context
                    if i == 0:  # if 'е' is at the start of the word
                        # match to 'ye' if the next letter is uppercase or if there is no next letter but previous letter is uppercase
                        match = 'ye' if key.islower() else (
                            'YE' if has_next_letter and next_letter.isupper() 
                            or not has_next_letter and has_pre_letter and pre_letter.isupper() 
                            else 'Ye'
                        )
                    elif (has_pre_letter and pre_letter.lower() == 'ъ' and 
                          (i < 2 or word[i - 2:i].lower() != 'къ')):
                        # after 'ъ' but not after 'къ'
                        # match to 'ye' if the next letter is uppercase or if there is no next letter but previous letter is uppercase
                        match = 'ye' if key.islower() else (
                            'YE' if has_next_letter and next_letter.isupper() 
                            or not has_next_letter and has_pre_letter and pre_letter.isupper() 
                            else 'Ye'
                        )
                    else:
                        match = self._mapping.get(key) # regular transliteration for 'е'
                elif key.lower() == 'н' and i == len(word) - 1: # 'н' at the end of the word
                    if word.lower() in self._blacklist:
                        match = self._mapping.get(key)
                    elif word.lower() in self._unsurelist:
                        match = 'ŋ[REPLACE]' if key.islower() else 'Ŋ[REPLACE]'
                    else:
                        match = 'ŋ' if key.islower() else 'Ŋ'
                else:
                    match = self._mapping.get(key) # regular transliteration for other characters

                if match is not None:
                    result += match
                    i += len(key)
                    break

            if match is None:
                result += word[i]
                i += 1
        
        # Normalize to NFC form for proper character composition
        return unicodedata.normalize('NFC', result)
    
    def transliterate(self, text: str) -> str:
        """Convert full text from Cyrillic to Latin script.
        
        Handles special cases like standalone 'а' → 'ə' and applies
        word-by-word transliteration.
        
        Args:
            text: Text in Cyrillic script to transliterate.
            
        Returns:
            Text transliterated to Latin script.
        """
        # Replace standalone 'а' with 'ə'
        text = re.sub(r'\bа\b', 'ə', text)
        text = re.sub(r'\bА\b', 'Ə', text)
        
        # Split text into words, convert each, then join back
        words = text.split()
        converted = ' '.join(self._transliterate_word(word) for word in words)
        
        return converted
