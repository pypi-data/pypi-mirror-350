# MSX Character Set Converter

[![Test](https://github.com/yamamo-to/msx-charset/actions/workflows/test.yml/badge.svg)](https://github.com/yamamo-to/msx-charset/actions/workflows/test.yml)

A Python package for converting between Unicode and MSX character sets, supporting Japanese, International, and Brazilian character sets.

## Features

- Support for MSX character set conversion:
  - Japanese version
  - International version
  - Brazilian version
- Compatible with Python 3.9 and later

## Installation

```bash
pip install msx-charset
```

## Usage

### Japanese Character Set

```python
import msx_charset

# Encoding
text = "こんにちは"
encoded = text.encode('msx-jp')
print(encoded)  # MSX code byte sequence

# Decoding
decoded = encoded.decode('msx-jp')
print(decoded)  # "こんにちは"
```

### International Character Set

```python
import msx_charset

# Encoding
text = "áéíóú"
encoded = text.encode('msx-intl')
print(encoded)  # MSX code byte sequence

# Decoding
decoded = encoded.decode('msx-intl')
print(decoded)  # "áéíóú"
```

### Brazilian Character Set

```python
import msx_charset

# Encoding
text = "Olá, mundo!"
encoded = text.encode('msx-br')
print(encoded)  # MSX code byte sequence

# Decoding
decoded = encoded.decode('msx-br')
print(decoded)  # "Olá, mundo!"
```

## Development

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install development package
pip install -e .
```

### Running Tests

```bash
python -m unittest discover -s tests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License 