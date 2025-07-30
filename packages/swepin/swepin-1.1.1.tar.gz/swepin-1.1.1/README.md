# SwePin

<div align="center">

[![PyPI version](https://img.shields.io/badge/pypi-v1.0.0-blue.svg)](https://pypi.org/project/swepin/)
[![Python versions](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://pypi.org/project/swepin/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-orange.svg)](https://swepin.readthedocs.io)

**A comprehensive library for parsing, validating, and handling Swedish Personal Identity Numbers (personnummer)**

</div>

## Features

- ✅ Validate Swedish Personal Identity Numbers
- 📊 Parse and extract all components (birth date, gender, validation digit, etc.)
- 🌍 Multi-language support (English and Swedish)
- 🧮 Age calculation with customizable reference date
- 🔄 Format conversion (with/without separators, 10/12 digits)
- ⚙️ Support for coordination numbers and centenarians
- 🎲 Generate valid random PIN numbers for testing
- 🔒 **Strict mode** for enforcing exact format requirements

## Installation

```bash
pip install swepin
```

## Quick Start

```python
# Import using the full name
from swepin import SwedishIdentityPersonalNumber

# Or using the shorter alias
from swepin import SwePin

# For strict format validation (YYYYMMDD-NNNN only)
from swepin import SwePinStrict

# Parse a Swedish Personal Identity Number
pin = SwePin("198012241234")

# Get basic information
print(f"Birth date: {pin.get_date()}")          # 1980-12-24
print(f"Age: {pin.age}")                        # Current age based on today's date
print(f"Gender: {'Male' if pin.male else 'Female'}")

# Display detailed information
print(pin.pretty_print())                       # Prints a formatted table with all details

# Get structured data
pin.dict                                        # Dictionary representation
pin.json                                        # JSON representation
```

## Understanding Swedish Personal Identity Numbers

Swedish Personal Identity Numbers follow this format: `YYYYMMDD-XXXX` or `YYMMDD-XXXX` (or `+` instead of `-` for separator)

```
┌───────────────┬───────┬───────────────────┐
│  BIRTH DATE   │ SEP   │   BIRTH NUMBER    │
├───┬───┬───┬───┼───────┼───┬───┬───┬───────┤
│ C │ Y │ M │ D │ - / + │ B │ B │ G │ Valid │
└───┴───┴───┴───┴───────┴───┴───┴───┴───────┘
  │   │   │   │     │     │   │   │     │
  │   │   │   │     │     │   │   │     └── Validation Digit (Luhn algorithm)
  │   │   │   │     │     │   │   │
  │   │   │   │     │     │   │   └── Gender Digit (odd = male, even = female)
  │   │   │   │     │     │   │
  │   │   │   │     │     └───┴── Birth Place (regional code for pre-1990)
  │   │   │   │     │
  │   │   │   │     └── Separator (- if < 100 years old, + if >= 100)
  │   │   │   │
  │   │   │   └── Day (01-31, or 61-91 for coordination numbers a.k.a samordningsnummer)
  │   │   │
  │   │   └── Month (01-12)
  │   │
  │   └── Year (last two digits)
  │
  └── Century (optional in short format, derived when not provided)
```

## Features

### Multiple Format Support

SwePin supports all standard formats of Swedish Personal Identity Numbers:

```python
# All these are valid and will parse correctly with SwePin
SwePin("198012241234")    # Full format (12 digits)
SwePin("8012241234")      # Short format (10 digits)
SwePin("19801224-1234")   # With separator
SwePin("801224-1234")     # Short with separator
SwePin("19801284-1234")   # Coordination number (day 24 + 60 = 84)
SwePin("121212+1212")     # Person over 100 years old (+ separator)
```

## Strict Format Validation

For applications that require exact format compliance, use `SwePinStrict` which enforces specific PIN formats through the `PinFormat` enum:

```python
from swepin import SwePinStrict, PinFormat

# Default format (LONG_WITH_SEPARATOR)
pin = SwePinStrict("19801224-1234")  # ✅ Uses default format
pin = SwePinStrict("19801284-1234")  # ✅ Valid coordination number

# Specify format explicitly
pin1 = SwePinStrict("19801224-1234", PinFormat.LONG_WITH_SEPARATOR)    # 13 chars
pin2 = SwePinStrict("198012241234", PinFormat.LONG_WITHOUT_SEPARATOR)  # 12 chars
pin3 = SwePinStrict("801224-1234", PinFormat.SHORT_WITH_SEPARATOR)     # 11 chars
pin4 = SwePinStrict("8012241234", PinFormat.SHORT_WITHOUT_SEPARATOR)   # 10 chars

### Format Conversion

Easily convert between different representations:

```python
pin = SwePin("198012241234")

# Access different format representations
print(pin.long_str_repr)                # "198012241234" (12 digits, no separator)
print(pin.long_str_repr_w_separator)    # "19801224-1234" (12 digits with separator)
print(pin.short_str_repr)               # "801224-1234" (10 digits with separator)
print(pin.short_str_repr_w_separator)   # "8012241234" (10 digits, no separator)
```

### Generate Random Valid PINs for Testing

Read [this!](README_GENERATE.md)

### Language Support

```python
from swepin.swedish_personal_identity_number import SwedishPersonalIdentityNumber, Language

pin = SwedishPersonalIdentityNumber("198012241234")

# Get output in different languages
print(pin.pretty_print(language=Language.ENG))  # Default - English
print(pin.pretty_print(language=Language.SWE))  # Swedish

# Get dictionary with Swedish keys
sv_dict = pin.to_dict(language=Language.SWE)
```

### Detailed Information

Get comprehensive information about a personal number with a beautiful formatted display:

```python
pin = SwePin("198012241234")
print(pin.pretty_print())
```

Output:
```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  Swedish Personal Identity Number Details                         ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃         Property         ┃                 Value                  ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃      Original Number     ┃ 198012241234                           ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃        BIRTH DATE        ┃                                        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃         Century          ┃ 19                                     ┃
┃      Year (2 digits)     ┃ 80                                     ┃
┃    Full Year (4 digits)  ┃ 1980                                   ┃
┃          Month           ┃ 12                                     ┃
┃           Day            ┃ 24                                     ┃
┃         Full Date        ┃ 1980-12-24                             ┃
┃    Coordination Number   ┃ No                                     ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃         SEPARATOR        ┃ -                                      ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃       BIRTH NUMBER       ┃                                        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃      Complete Number     ┃ 123                                    ┃
┃     Birth Place Digits   ┃ 12                                     ┃
┃       Gender Digit       ┃ 3                                      ┃
┃     Validation Digit     ┃ 4                                      ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃    DERIVED PROPERTIES    ┃                                        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃           Age            ┃ 44                                     ┃
┃          Gender          ┃ Male                                   ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃         FORMATS          ┃                                        ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃      Long (12 digits)    ┃ 198012241234                           ┃
┃         Long (sep)       ┃ 19801224-1234                          ┃
┃  Short (10 digits) (sep) ┃ 801224-1234                            ┃
┃     Short without (sep)  ┃ 8012241234                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━┻━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### Validation

The library validates personal numbers using the Luhn algorithm to ensure the check/validation digit is correct:

```python
try:
    pin = SwePin("198012241234")  # Valid personal number
    print("Valid personal identity number")
except Exception as e:
    print(f"Invalid: {e}")

try:
    pin = SwePin("198012241235")  # Invalid check digit
    print("Valid personal identity number")
except Exception as e:
    print(f"Invalid: {e}")  # Will print error about validation digit mismatch
```

### Special Cases

#### Coordination Numbers

For people without a permanent residence in Sweden, coordination numbers (samordningsnummer) are used where the day is increased by 60:

```python
pin = SwePin("198012841234")  # Day 24 + 60 = 84
print(f"Is coordination number: {pin._is_coordination_number()}")  # True
print(f"Birth date: {pin.get_date()}")  # Still returns 1980-12-24
```

#### Centenarians

For people 100 years or older, a `+` separator is used instead of `-` in the short format:

```python
pin = SwePin("121212+1212")  # Person born in 1912
print(pin.short_str_repr)    # "121212+1212"
print(pin.full_year)         # "1912"
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

<div align="center">
Made with ❤️ in Sweden
</div>