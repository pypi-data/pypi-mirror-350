import datetime
import re
from datetime import date as Date
import json
from enum import Enum, auto


class Language(Enum):
    """Language options for output formatting."""

    ENG = auto()  # English
    SWE = auto()  # Swedish (Svenska)


class SwePinLoose:
    """
    A class for parsing, validating and handling Swedish Personal Identity Numbers (personnummer).

    ## Format Explanation

    Swedish Personal Identity Number follows the format: YYYYMMDD-XXXX or YYMMDD-XXXX

    ```
    ┌───────────────┬───────┬───────────────────┐
    │  BIRTH DATE   │ SEP   │   BIRTH NUMBER    │
    ├───┬───┬───┬───┼───────┼───┬───┬───┬───────┤
    │ C │ Y │ M │ D │ - / + │ B │ B │ G │ Valid │
    │ C │ Y │ M │ D │ - / + │ B │ B │ G │ Valid │
    └───┴───┴───┴───┴───────┴───┴───┴───┴───────┘
    │   │   │   │     │     │   │   │     │
    │   │   │   │     │     │   │   │     └── Validation Digit (calculated with Luhn algorithm)
    │   │   │   │     │     │   │   │
    │   │   │   │     │     │   │   └── Gender Digit (odd = male, even = female)
    │   │   │   │     │     │   │
    │   │   │   │     │     └───┴── Birth Place (historical regional code for pre-1990)
    │   │   │   │     │
    │   │   │   │     └── Separator (- if < 100 years old, + if >= 100)
    │   │   │   │
    │   │   │   └── Day (01-31, or 61-91 for coordination numbers)
    │   │   │
    │   │   └── Month (01-12)
    │   │
    │   └── Year (last two digits)
    │
    └── Century (optional in short format, derived when not provided)
    ```

    ## Examples

    Full format (12 digits): `198012241234`
    Short format (10 digits): `8012241234`
    With separators: `19801224-1234` or `801224-1234`
    Coordination number: `19801284-1234` (day 24 + 60 = 84)
    Person over 100: `191212121212` or `121212+1212`

    ## Language Support

    The class provides multi-language support through the Language enum:
    - Language.ENG: English (default)
    - Language.SWE: Swedish (Svenska)

    Language selection can be applied to:
    - The `pretty_print()` method to get output in the selected language
    - The `to_dict()` method to get dictionary keys in the selected language

    ## Instance Properties

    * `pin`: Original Personal Identity Number string provided
    * `today`: Reference date for age calculations (defaults to current date)
    * `century`: Century part of the birth year (e.g., "19")
    * `year`: Year part without century (e.g., "80")
    * `full_year`: Complete 4-digit year (e.g., "1980")
    * `month`: Month part (e.g., "12")
    * `day`: Day part (e.g., "24"), can be > 60 for coordination numbers
    * `separator`: Separator character ("-" or "+")
    * `birth_number`: 3-digit birth number, excluding check digit (e.g., "123")
    * `birth_place`: Birth place code (first 2 digits of birth_number, e.g., "12")
    * `gender_digit`: Gender digit (3rd digit of birth_number, e.g., "3")
    * `validation_digit`: Validation digit calculated using Luhn algorithm (e.g., "4")
    * `is_coordination_number`: Boolean indicating if this is a coordination number
    * `coordination_number`: The original coordination number value (day + 60)
    * `calculated_day_from_coordination_number`: The actual day derived from a coordination number
    * `birth_date`: Date object representing the birth date (derived from year, month, day)
    * `age`: Calculated age based on the birth date and reference date
    * `male`: Boolean indicating if the person is male
    * `female`: Boolean indicating if the person is female
    * `long_str_repr`: Full 12-digit representation without separator (e.g., "198012241234")
    * `short_str_repr`: 10-digit representation with separator (e.g., "801224-1234")
    * `long_str_repr_w_separator`: Full 12-digit representation with separator (e.g., "19801224-1234")
    * `short_str_repr_w_separator`: 10-digit representation without separator (e.g., "8012241234")
    * `pretty`: Formatted tabular representation of all properties
    * `dict`: Dictionary representation of all properties
    * `json`: JSON string representation of all properties

    ## Special Cases

    * **Coordination Numbers**: For people without a permanent residence in Sweden,
    the day number is increased by 60 (e.g., day 24 becomes 84).

    * **Centenarians**: People 100 years or older use a "+" separator instead of "-"
    in the short format.

    ## Usage Examples

    ```python
    # Import the class and language enum
    from swedish_pin import SwedishPersonalIdentityNumber, Language

    # Parse a Swedish Personal Identity Number
    pin = SwedishPersonalIdentityNumber("198012241234")

    # Parse with a specific reference date
    from datetime import date
    pin = SwedishPersonalIdentityNumber("198012241234", today=date(2024, 3, 1))

    # Get the age
    age = pin.age  # 44 (assuming today is in 2024)

    # Check if male
    is_male = pin.male  # True if odd gender digit

    # Get birth date as Date object
    birth_date = pin.birth_date  # 1980-12-24

    # Check if it's a coordination number
    is_coord = pin.is_coordination_number  # False for this example

    # Different format representations
    full_no_sep = pin.long_str_repr           # "198012241234"
    short_with_sep = pin.short_str_repr       # "801224-1234"
    full_with_sep = pin.long_str_repr_w_separator    # "19801224-1234"
    short_no_sep = pin.short_str_repr_w_separator    # "8012241234"

    # Get dictionary representation (English - default)
    data_dict = pin.dict
    # or explicitly:
    data_dict_en = pin.to_dict(language=Language.ENG)

    # Get JSON representation (English - default)
    data_json = pin.json

    # Get a pretty-printed table in English (default)
    print(pin.pretty)
    # or explicitly:
    print(pin.pretty_print(language=Language.ENG))

    # Get Swedish output
    sv_pretty = pin.pretty_print(language=Language.SWE)
    print(sv_pretty)  # Prints the table in Swedish

    # Get dictionary with Swedish keys
    sv_dict = pin.to_dict(language=Language.SWE)
    print(sv_dict["personnummer"])  # Access using Swedish key names

    # Get JSON with Swedish keys
    import json
    sv_json = json.dumps(pin.to_dict(language=Language.SWE))
    ```

    ## Extending Language Support

    To add support for additional languages:

    1. Add a new enum value to the Language class
    2. Add translations to the _language_translations dictionary
    """

    pin: str
    today: Date | None = None
    _language_translations: dict[Enum, dict[str, str]] = {
        Language.ENG: {
            "title": "Swedish Personal Identity Number",
            "property": "Property",
            "value": "Value",
            "original_number": "Original number",
            "birth_date": "Birth date",
            "century": "Century",
            "year_2digits": "Year (2 digits)",
            "full_year": "Full year (4 digits)",
            "month": "Month",
            "day": "Day",
            "full_date": "Full date",
            "coordination_number": "Coordination number",
            "yes_day_60": "Yes (day + 60)",
            "no": "No",
            "actual_day": "Actual Day",
            "separator": "Separator",
            "birth_number": "Birth Number",
            "complete_number": "Complete number",
            "birth_place_digits": "Birth place digits",
            "gender_digit": "Gender digit",
            "validation_digit": "Validation digit",
            "derived_properties": "Derived properties",
            "age": "Age",
            "gender": "Gender",
            "male": "Male",
            "female": "Female",
            "formats": "Formats",
            "long_wo_sep": "12 digits",
            "long_w_sep": "12 digits w/ separator",
            "short_wo_sep": "10 digits",
            "short_w_sep": "10 digits w/ separator",
        },
        Language.SWE: {
            "title": "Svenskt Personnummer",
            "property": "Egenskap",
            "value": "Värde",
            "original_number": "Ursprungligt personnummer",
            "birth_date": "Födelsedatum",
            "century": "Sekel",
            "year_2digits": "År (2 siffror)",
            "full_year": "Fullständigt år (4 siffror)",
            "month": "Månad",
            "day": "Dag",
            "full_date": "Fullständigt datum",
            "coordination_number": "Samordningsnummer",
            "yes_day_60": "Ja (dag + 60)",
            "no": "Nej",
            "actual_day": "Faktisk dag",
            "separator": "Skiljetecken",
            "birth_number": "Födelsenummer",
            "complete_number": "Fullständigt nummer",
            "birth_place_digits": "Födelseortssiffror",
            "gender_digit": "Könssiffra",
            "validation_digit": "Kontrollsiffra",
            "derived_properties": "Härledda egenskaper",
            "age": "Ålder",
            "gender": "Kön",
            "male": "Man",
            "female": "Kvinna",
            "formats": "Format",
            "long_wo_sep": "12 siffror utan skiljetecken",
            "long_w_sep": "12 siffror med skiljetecken",
            "short_w_sep": "10 siffror med skiljetecken",
            "short_wo_sep": "10 siffror skiljetecken",
        },
    }

    def __init__(self, pin: str, today: Date | None = None):
        if not isinstance(pin, str):
            raise Exception("Swedish personal identity number must be a string")
        self.pin = pin
        self.today = today
        self.century = None
        self.year = None
        self.month = None
        self.day = None
        self.separator = None
        self.birth_place = None
        self.gender_digit = None
        self.birth_number = None
        self.validation_digit = None
        self.is_coordination_number = None
        self.coordination_number = None
        self.calculated_day_from_coordination_number = None
        self.birth_date = None
        self.age = None
        self.male = None
        self.female = None
        self.full_year = None
        self.long_str_repr_no_separator = None
        self.short_str_repr_no_separator = None
        self.long_str_repr_w_separator = None
        self.short_str_repr_w_separator = None
        self.dict = None
        self.json = None

        if not self.today:
            self.today = datetime.date.today()

        self._parse_pin_parts()

        if not self.validation_digit:
            raise Exception("Validation digit is missing.")

        calculated_validation_digit = calculate_luhn_validation_digit(
            input_digits=f"{self.year}{self.month}{self.day}{self.birth_number}"
        )
        if calculated_validation_digit != int(self.validation_digit):
            raise Exception(
                f"Validation digit did not match the personal identity number. Expected {calculated_validation_digit}, got {self.validation_digit}."
            )

        self.is_coordination_number = self._is_coordination_number()
        self.birth_date = self.get_birth_date()
        self.age = self.get_age()
        self.male = self._is_male()
        self.female = not self._is_male()

        year_month_day = f"{self.year}{self.month}{self.day}"
        self.long_str_repr_no_separator = (
            f"{self.century}{year_month_day}{self.birth_number}{self.validation_digit}"
        )
        self.short_str_repr_no_separator = f"{year_month_day}{self.birth_number}{self.validation_digit}"
        self.long_str_repr_w_separator = f"{self.century}{year_month_day}{self.separator}{self.birth_number}{self.validation_digit}"
        self.short_str_repr_w_separator = (
            f"{year_month_day}{self.separator}{self.birth_number}{self.validation_digit}"
        )
        self.dict = self.to_dict()
        self.json = json.dumps(self.dict)

    def _is_coordination_number(self):
        return int(self.day) > 60

    def get_birth_date(self) -> Date:
        day = int(self.day)
        if self.is_coordination_number:
            day = day - 60
        birth_date = datetime.date(
            year=int(self.full_year), month=int(self.month), day=day
        )

        if birth_date > self.today:
            raise ValueError("Birth date cannot be in the future")

        return birth_date

    def get_age(self) -> int:
        day = int(self.day)
        if self.is_coordination_number:
            day = day - 60

        return (
            self.today.year
            - int(self.full_year)
            - ((self.today.month, self.today.day) < (int(self.month), day))
        )

    def _is_male(self) -> bool:
        gender_digit = int(self.birth_number[2])  # The third digit in the number part
        return gender_digit % 2 == 1  # Odd for males, even for females

    def _parse_pin_parts(self):
        match = re.match(
            r"^(\d{2}){0,1}(\d{2})(\d{2})(\d{2})([\-\+]{0,1})?((\d{2})(\d{1}))((\d{1}))$",
            str(self.pin),
        )
        if not match:
            raise Exception(
                f'Could not parse "{self.pin}" as Swedish Personal Identity Number.'
            )

        century = match.group(1)
        year = match.group(2)
        separator = match.group(5)

        this_year = self.today.year
        if not century:
            this_year = self.today.year
            if separator == "+":
                this_year -= 100
            else:
                separator = "-"
            full_year = this_year - ((this_year - int(year)) % 100)
            century = str(int(full_year / 100))
        else:
            separator = "-" if self.today.year - int(f"{century}{year}") < 100 else "+"

        self.century = century
        self.full_year = century + year
        self.year = year
        self.month = match.group(3)

        self.day = match.group(4)
        if self._is_coordination_number():
            self.calculated_day_from_coordination_number = str(int(self.day) - 60)
        self.separator = separator
        self.birth_number = match.group(6)
        self.birth_place = match.group(7)
        self.gender_digit = match.group(8)
        self.validation_digit = match.group(10)

    def __str__(self):
        return self.short_str_repr_w_separator

    def pretty_print(self, language: Language = Language.ENG) -> str:
        """
        Returns a nicely formatted table displaying all properties of the Swedish Personal Identity Number.

        Args:
            language: Language for the output. Default is English.

        Returns:
            str: A multi-line string containing the formatted table
        """
        # Get translations for the selected language
        t = self._language_translations[language]

        # Define the maximum width for property names and values
        prop_width = 36 if language == Language.SWE else 28
        val_width = 40

        # Prepare a list to hold all lines of the table
        lines = []

        # Build header
        lines.append("┏" + "━" * prop_width + "┳" + "━" * val_width + "┓")
        title = t["title"]
        # Calculate the exact space needed for proper centering
        title_padding = prop_width + val_width + 1 - len(title)
        left_pad = title_padding // 2
        right_pad = title_padding - left_pad
        lines.append("┃" + " " * left_pad + title + " " * right_pad + "┃")
        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")

        # Add property and value header
        lines.append(
            "┃"
            + f" {t['property']:^{prop_width-2}} "
            + "┃"
            + f" {t['value']:^{val_width-2}} "
            + "┃"
        )
        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")

        # Add the original PIN
        lines.append(
            "┃"
            + f" {t['original_number']:^{prop_width-2}} "
            + "┃"
            + f" {self.pin:<{val_width-2}} "
            + "┃"
        )
        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")

        # Add birth date section
        lines.append(
            "┃"
            + f" {t['birth_date']:^{prop_width-2}} "
            + "┃"
            + f" {'':<{val_width-2}} "
            + "┃"
        )
        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")
        lines.append(
            "┃"
            + f" {'  ' + t['century']:^{prop_width-2}} "
            + "┃"
            + f" {self.century:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['year_2digits']:^{prop_width-2}} "
            + "┃"
            + f" {self.year:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['full_year']:^{prop_width-2}} "
            + "┃"
            + f" {self.full_year:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['month']:^{prop_width-2}} "
            + "┃"
            + f" {self.month:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['day']:^{prop_width-2}} "
            + "┃"
            + f" {self.day:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['full_date']:^{prop_width-2}} "
            + "┃"
            + f" {self.get_birth_date().strftime('%Y-%m-%d'):<{val_width-2}} "
            + "┃"
        )

        # Always show coordination number information
        if self.is_coordination_number:
            lines.append(
                "┃"
                + f" {'  ' + t['coordination_number']:^{prop_width-2}} "
                + "┃"
                + f" {t['yes_day_60']:<{val_width-2}} "
                + "┃"
            )
            lines.append(
                "┃"
                + f" {'  ' + t['actual_day']:^{prop_width-2}} "
                + "┃"
                + f" {self.calculated_day_from_coordination_number:<{val_width-2}} "
                + "┃"
            )
        else:
            lines.append(
                "┃"
                + f" {'  ' + t['coordination_number']:^{prop_width-2}} "
                + "┃"
                + f" {t['no']:<{val_width-2}} "
                + "┃"
            )

        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")

        # Add separator section
        lines.append(
            "┃"
            + f" {t['separator']:^{prop_width-2}} "
            + "┃"
            + f" {self.separator:<{val_width-2}} "
            + "┃"
        )
        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")

        # Add birth number section
        lines.append(
            "┃"
            + f" {t['birth_number']:^{prop_width-2}} "
            + "┃"
            + f" {'':<{val_width-2}} "
            + "┃"
        )
        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")
        lines.append(
            "┃"
            + f" {'  ' + t['complete_number']:^{prop_width-2}} "
            + "┃"
            + f" {self.birth_number:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['birth_place_digits']:^{prop_width-2}} "
            + "┃"
            + f" {self.birth_place:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['gender_digit']:^{prop_width-2}} "
            + "┃"
            + f" {self.gender_digit:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['validation_digit']:^{prop_width-2}} "
            + "┃"
            + f" {self.validation_digit:<{val_width-2}} "
            + "┃"
        )
        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")

        # Add derived properties section
        lines.append(
            "┃"
            + f" {t['derived_properties']:^{prop_width-2}} "
            + "┃"
            + f" {'':<{val_width-2}} "
            + "┃"
        )
        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")
        lines.append(
            "┃"
            + f" {'  ' + t['age']:^{prop_width-2}} "
            + "┃"
            + f" {self.age:<{val_width-2}} "
            + "┃"
        )
        gender_value = t["male"] if self.male else t["female"]
        lines.append(
            "┃"
            + f" {'  ' + t['gender']:^{prop_width-2}} "
            + "┃"
            + f" {gender_value:<{val_width-2}} "
            + "┃"
        )

        # Format section with all combinations
        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")
        lines.append(
            "┃"
            + f" {t['formats']:^{prop_width-2}} "
            + "┃"
            + f" {'':<{val_width-2}} "
            + "┃"
        )
        lines.append("┣" + "━" * prop_width + "╋" + "━" * val_width + "┫")
        lines.append(
            "┃"
            + f" {'  ' + t['long_wo_sep']:^{prop_width-2}} "
            + "┃"
            + f" {self.long_str_repr_no_separator:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['long_w_sep']:^{prop_width-2}} "
            + "┃"
            + f" {self.long_str_repr_w_separator:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['short_w_sep']:^{prop_width-2}} "
            + "┃"
            + f" {self.short_str_repr_no_separator:<{val_width-2}} "
            + "┃"
        )
        lines.append(
            "┃"
            + f" {'  ' + t['short_wo_sep']:^{prop_width-2}} "
            + "┃"
            + f" {self.short_str_repr_w_separator:<{val_width-2}} "
            + "┃"
        )

        # Add footer
        lines.append("┗" + "━" * prop_width + "┻" + "━" * val_width + "┛")

        # Join all lines with newlines and return the result
        return "\n".join(lines)

    def to_dict(self, language: Language = Language.ENG) -> dict:
        if language == Language.SWE:
            return {
                "personnummer": self.pin,
                "födelsedatum": {
                    "sekel": self.century,
                    "år": self.year,
                    "fullständigt_år": self.full_year,
                    "månad": self.month,
                    "dag": self.day,
                    "iso_datum": self.get_birth_date().isoformat(),
                },
                "skiljetecken": self.separator,
                "födelsenummer": {
                    "komplett": self.birth_number,
                    "födelseort": self.birth_place,
                    "könssiffra": self.gender_digit,
                },
                "kontrollsiffra": self.validation_digit,
                "härledda_egenskaper": {
                    "ålder": self.age,
                    "kön": "man" if self.male else "kvinna",
                    "är_samordningsnummer": self.is_coordination_number,
                },
                "format": {
                    "12 siffror": self.long_str_repr_no_separator,
                    "10 siffror": self.short_str_repr_no_separator,
                    "12 siffror med skiljetecken": self.long_str_repr_w_separator,
                    "10 siffror med skiljetecken": self.short_str_repr_w_separator,
                },
            }
        else:
            return {
                "personal_identity_number": self.pin,
                "birth_date": {
                    "century": self.century,
                    "year": self.year,
                    "full_year": self.full_year,
                    "month": self.month,
                    "day": self.day,
                    "iso_date": self.get_birth_date().isoformat(),
                },
                "separator": self.separator,
                "birth_number": {
                    "complete": self.birth_number,
                    "birth_place": self.birth_place,
                    "gender_digit": self.gender_digit,
                },
                "validation_digit": self.validation_digit,
                "derived_info": {
                    "age": self.age,
                    "gender": "male" if self.male else "female",
                    "is_coordination_number": self.is_coordination_number,
                },
                "formats": {
                    "12 digits": self.long_str_repr_no_separator,
                    "10 digits": self.short_str_repr_no_separator,
                    "12 digits w/ separator": self.long_str_repr_w_separator,
                    "10 digits w/ separator": self.short_str_repr_w_separator,
                },
            }


def calculate_luhn_validation_digit(input_digits: str) -> int:
    """Calculate the validation digit for a Swedish personal number using the Luhn algorithm."""
    total_sum = 0

    for position, digit in enumerate(input_digits):
        value = int(digit)
        if position % 2 == 0:
            value *= 2
        else:
            value *= 1

        if value > 9:
            value -= 9

        total_sum += value

    return (10 - (total_sum % 10)) % 10
