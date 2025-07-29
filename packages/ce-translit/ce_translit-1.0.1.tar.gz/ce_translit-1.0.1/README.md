# Chechen Transliterator

[![PyPI version](https://img.shields.io/pypi/v/ce-translit.svg)](https://pypi.org/project/ce-translit/)
[![Python versions](https://img.shields.io/pypi/pyversions/ce-translit.svg)](https://pypi.org/project/ce-translit/)
[![License](https://img.shields.io/github/license/chechen-language/ce-translit-py.svg)](https://github.com/chechen-language/ce-translit-py/blob/main/LICENSE)

A Python library for transliterating Chechen text from Cyrillic to Latin script using the Chechen Latin alphabet.

## Installation

```bash
pip install ce-translit
```

## Quick Start

```python
import ce_translit

# Simple usage - transliterate Chechen text
text = "Нохчийн мотт"
result = ce_translit.transliterate(text)
print(result)  # Outputs: "Noxçiyŋ mott"
```

## Features

- **Simple API**: Clean, single-function interface
- **Linguistically Accurate**: Handles all Chechen-specific rules
- **Context-Aware**: Special handling for letter position rules
- **Customizable**: Advanced options for specialized use cases
- **Pure Python**: No external dependencies
- **Memory Efficient**: Uses minimal memory and efficient string handling

## Detailed Usage

### Basic Usage

```python
import ce_translit

# Transliterate a single word
word_result = ce_translit.transliterate("дош")  # "doş"

# Transliterate a sentence
sentence = "Муха ду хьал де?"
sentence_result = ce_translit.transliterate(sentence)  # "Muxa du ẋal de?"
```

### Advanced Usage with Custom Rules

```python
from ce_translit import Transliterator

# Create a custom transliterator with your own rules
custom_transliterator = Transliterator(
    # Custom letter mapping
    mapping={
        **Transliterator()._mapping, # First define base mapping
        # Then override specific mappings
        "й": "j",
        # Append completely new mappings
        "1": "j"
    },
    # Override blacklist (Words that should keep the regular 'н' at the end)
    blacklist=["дин", "гӏан", "сан"],
    # Override unsurelist (Words that should use 'ŋ[REPLACE]' at the end)
    unsurelist=["шун", "бен", "цӏен"]
)

# Use the custom transliterator
result = custom_transliterator.transliterate("1аж дин шун")
```

If you omit `**Transliterator()._mapping**` from the custom mapping, the custom transliterator will only use the custom mappings you provide.

### Oveeride just one of list by defining a list outside

```python
from ce_translit import Transliterator

# Define your own list
my_blacklist = ["дин", "гӏан", "сан"]

# Create a custom transliterator with defined blacklist
custom_transliterator = Transliterator(blacklist=my_blacklist)
result = custom_transliterator.transliterate("дин")
```

## Special Transliteration Rules

The library handles several special rules in Chechen transliteration:

1. **Letter 'е'**:
   - At the start of a word → 'ye' (ex: "елар" → "yelar")
   - After 'ъ' → 'ye' (ex: "шелъелча" → "şelyelça")
   - In other positions → 'e' (ex: "мела" → "mela")

2. **Letter 'н' at end of words**:
   - Regular handling → 'ŋ' (ex: "сан" → "saŋ")
   - Blacklisted words keep 'n' (ex: "хан" → "xan")
   - Unsurelist words use 'ŋ[REPLACE]' (ex: "шун" → "şuŋ[REPLACE]")

3. **Standalone 'а'**:
   - When 'а' is a standalone word → 'ə' (ex: "а" → "ə")

4. **Special Character Combinations**:
   - 'къ' → 'q̇'
   - 'хь' → 'ẋ'
   - 'гӏ' → 'ġ'

## Technical Details

### Performance

The library is optimized for both startup time and runtime performance:

- Data is loaded once at import time
- Efficient string handling for minimal memory usage
- Uses sets for O(1) lookups in blacklists and unsure lists

## Development

### Setting up the Development Environment

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install development tools
pip install --upgrade hatch pytest

# Run tests
hatch run test

# Build the package
hatch build

# Test the built package
pip install --force-reinstall dist/ce_translit-1.0.0-py3-none-any.whl
```

### Running Tests

```bash
# Install test dependencies
pip install pytest

# Run tests
pytest
```

### Repository Structure

```
ce-translit-py/
├── src/
│   └── ce_translit/
│       ├── __init__.py         # Public API
│       ├── _transliterator.py  # Core implementation
│       ├── data/
│       │   └── cyrl_latn_map.json  # Character mapping
├── tests/
│   └── test_transliterator.py
├── LICENSE
├── README.md
└── pyproject.toml
```

## License

This project is licensed under the [MIT License](https://github.com/chechen-language/ce-translit-py/blob/main/LICENSE).

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests on the [GitHub repository](https://github.com/chechen-language/ce-translit-py).

## Related Projects

- [ce-translit-js](https://github.com/chechen-language/ce-translit-js) - JavaScript version of this library
