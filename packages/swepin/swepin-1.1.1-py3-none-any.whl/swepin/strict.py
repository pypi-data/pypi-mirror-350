import re
from enum import Enum, auto
from swepin import calculate_luhn_validation_digit
from swepin.loose import SwePinLoose
from datetime import date as Date


class PinFormat(Enum):
    """Supported PIN formats for strict validation."""
    LONG_WITH_SEPARATOR = auto()     # YYYYMMDD-NNNN (13 chars)
    LONG_WITHOUT_SEPARATOR = auto()  # YYYYMMDDNNNN (12 chars)
    SHORT_WITH_SEPARATOR = auto()    # YYMMDD-NNNN (11 chars)
    SHORT_WITHOUT_SEPARATOR = auto() # YYMMDDNNNN (10 chars)


class SwePinStrict(SwePinLoose):
    """
    A strict version of SwePinLoose that accepts specific PIN formats. See docstring of SwePinLoose.

    Supported formats:
    - LONG_WITH_SEPARATOR: 19801224-1234 (13 chars)
    - LONG_WITHOUT_SEPARATOR: 198012241234 (12 chars)
    - SHORT_WITH_SEPARATOR: 801224-1234 (11 chars)
    - SHORT_WITHOUT_SEPARATOR: 8012241234 (10 chars)

    Default format:
    - LONG_WITH_SEPARATOR
    """

    def __init__(self, pin: str,  pin_format: PinFormat = PinFormat.LONG_WITH_SEPARATOR, today: Date | None = None):
        if not isinstance(pin, str):
            raise Exception("Swedish personal identity number must be a string")

        if not self._validate_format(pin, pin_format):
            expected_format = self._get_format_description(pin_format)
            raise Exception(
                f'"{pin}" does not match required format {pin_format.name}. '
                f'Expected: {expected_format}'
            )

        self.pin_format = pin_format
        super().__init__(pin, today)

    def _validate_format(self, pin: str, pin_format: PinFormat) -> bool:
        """Validate PIN matches the specified format."""
        patterns = {
            PinFormat.LONG_WITH_SEPARATOR: (r"^(\d{4})(\d{2})(\d{2})-(\d{3})(\d{1})$", 13),
            PinFormat.LONG_WITHOUT_SEPARATOR: (r"^(\d{4})(\d{2})(\d{2})(\d{3})(\d{1})$", 12),
            PinFormat.SHORT_WITH_SEPARATOR: (r"^(\d{2})(\d{2})(\d{2})-(\d{3})(\d{1})$", 11),
            PinFormat.SHORT_WITHOUT_SEPARATOR: (r"^(\d{2})(\d{2})(\d{2})(\d{3})(\d{1})$", 10),
        }

        pattern, expected_length = patterns[pin_format]
        return len(pin) == expected_length and re.match(pattern, pin) is not None

    def _get_format_description(self, pin_format: PinFormat) -> str:
        """Get human-readable format description."""
        descriptions = {
            PinFormat.LONG_WITH_SEPARATOR: "YYYYMMDD-NNNN",
            PinFormat.LONG_WITHOUT_SEPARATOR: "YYYYMMDDNNNN",
            PinFormat.SHORT_WITH_SEPARATOR: "YYMMDD-NNNN",
            PinFormat.SHORT_WITHOUT_SEPARATOR: "YYMMDDNNNN",
        }
        return descriptions[pin_format]

    def _parse_pin_parts(self) -> None:
        """Override parent method to use strict parsing based on format."""
        patterns = {
            PinFormat.LONG_WITH_SEPARATOR: r"^(\d{4})(\d{2})(\d{2})-(\d{3})(\d{1})$",
            PinFormat.LONG_WITHOUT_SEPARATOR: r"^(\d{4})(\d{2})(\d{2})(\d{3})(\d{1})$",
            PinFormat.SHORT_WITH_SEPARATOR: r"^(\d{2})(\d{2})(\d{2})-(\d{3})(\d{1})$",
            PinFormat.SHORT_WITHOUT_SEPARATOR: r"^(\d{2})(\d{2})(\d{2})(\d{3})(\d{1})$",
        }

        pattern = patterns[self.pin_format]
        match = re.match(pattern, str(self.pin))

        if not match:
            raise Exception(f'Could not parse "{self.pin}" with format {self.pin_format.name}.')

        if self.pin_format in [PinFormat.LONG_WITH_SEPARATOR, PinFormat.LONG_WITHOUT_SEPARATOR]:
            full_year = match.group(1)
            month = match.group(2)
            day = match.group(3)
            birth_number = match.group(4)
            original_validation_digit = match.group(5)
        else:  # SHORT formats
            year_part = match.group(1)
            month = match.group(2)
            day = match.group(3)
            birth_number = match.group(4)
            original_validation_digit = match.group(5)

            # Derive century for short format
            current_year = self.today.year if self.today else Date.today().year
            full_year = str(current_year - ((current_year - int(year_part)) % 100))

        day_int = int(day)
        is_coordination_number: bool = day_int > 60

        self.century = full_year[:2]
        self.year = full_year[2:]
        self.full_year = full_year
        self.month = month
        self.day = day
        self.separator = "-" if "WITHOUT" not in self.pin_format.name else None
        self.birth_number = birth_number
        self.birth_place = birth_number[:2]
        self.gender_digit = birth_number[2]
        self.is_coordination_number = is_coordination_number

        calculated_validation_digit = str(
            calculate_luhn_validation_digit(
                input_digits=f"{self.year}{self.month}{self.day}{self.birth_number}"
            )
        )

        self.validation_digit = calculated_validation_digit

        if calculated_validation_digit != original_validation_digit:
            raise Exception(
                f"Validation digit did not match. Expected {calculated_validation_digit}, got {original_validation_digit}."
            )

        if is_coordination_number:
            self.coordination_number = day
            self.calculated_day_from_coordination_number = str(day_int - 60).zfill(2)
        else:
            self.coordination_number = None
            self.calculated_day_from_coordination_number = None