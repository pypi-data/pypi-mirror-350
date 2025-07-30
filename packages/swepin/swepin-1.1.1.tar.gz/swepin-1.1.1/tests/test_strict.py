import pytest
from datetime import date
from swepin import SwePinStrict, PinFormat


class TestSwePinStrictValidFormats:
    """Test cases for valid SwePinStrict formats."""

    def test_valid_format_regular_number_long_with_separator(self):
        """Test valid regular personal number in long format with separator."""
        pin = SwePinStrict("19801224-1231", PinFormat.LONG_WITH_SEPARATOR)
        assert pin.pin == "19801224-1231"
        assert pin.century == "19"
        assert pin.year == "80"
        assert pin.full_year == "1980"
        assert pin.month == "12"
        assert pin.day == "24"
        assert pin.separator == "-"
        assert pin.birth_number == "123"
        assert pin.validation_digit == "1"

    def test_valid_format_regular_number_long_without_separator(self):
        """Test valid regular personal number in long format without separator."""
        pin = SwePinStrict("198012241231", PinFormat.LONG_WITHOUT_SEPARATOR)
        assert pin.pin == "198012241231"
        assert pin.full_year == "1980"
        assert pin.separator == None

    def test_valid_format_regular_number_short_with_separator(self):
        """Test valid regular personal number in short format with separator."""
        pin = SwePinStrict("801224-1231", PinFormat.SHORT_WITH_SEPARATOR)
        assert pin.pin == "801224-1231"
        assert pin.year == "80"
        assert pin.separator == "-"

    def test_valid_format_regular_number_short_without_separator(self):
        """Test valid regular personal number in short format without separator."""
        pin = SwePinStrict("8012241231", PinFormat.SHORT_WITHOUT_SEPARATOR)
        assert pin.pin == "8012241231"
        assert pin.year == "80"
        assert pin.separator == None

    def test_valid_format_coordination_number(self):
        """Test valid coordination number in all formats."""
        # Long with separator
        pin1 = SwePinStrict("19801284-1238", PinFormat.LONG_WITH_SEPARATOR)
        assert pin1.day == "84"
        assert pin1.is_coordination_number
        assert pin1.calculated_day_from_coordination_number == "24"

        # Long without separator
        pin2 = SwePinStrict("198012841238", PinFormat.LONG_WITHOUT_SEPARATOR)
        assert pin2.is_coordination_number

        # Short with separator
        pin3 = SwePinStrict("801284-1238", PinFormat.SHORT_WITH_SEPARATOR)
        assert pin3.is_coordination_number

        # Short without separator
        pin4 = SwePinStrict("8012841238", PinFormat.SHORT_WITHOUT_SEPARATOR)
        assert pin4.is_coordination_number

    def test_valid_format_different_years(self):
        """Test valid format with different years."""
        valid_test_cases: list[tuple[str, PinFormat]] = [
            ("20001201-1231", PinFormat.LONG_WITH_SEPARATOR),
            ("19501015-5678", PinFormat.LONG_WITH_SEPARATOR),
            ("200012011231", PinFormat.LONG_WITHOUT_SEPARATOR),
            ("001201-1231", PinFormat.SHORT_WITH_SEPARATOR),
            ("0012011231", PinFormat.SHORT_WITHOUT_SEPARATOR),
        ]

        future_test_cases: list[tuple[str, PinFormat]] = [
            ("20251231-9876", PinFormat.LONG_WITH_SEPARATOR),
        ]

        # Test valid historical dates
        for pin_str, pin_format in valid_test_cases:
            from swepin.loose import calculate_luhn_validation_digit

            if pin_format in [PinFormat.LONG_WITH_SEPARATOR, PinFormat.LONG_WITHOUT_SEPARATOR]:
                base_digits: str = pin_str.replace("-", "")[2:-1]
            else:
                base_digits: str = pin_str.replace("-", "")[:-1]

            correct_digit: int = calculate_luhn_validation_digit(base_digits)
            valid_pin: str = pin_str[:-1] + str(correct_digit)

            pin = SwePinStrict(valid_pin, pin_format)
            assert pin.pin == valid_pin

        # Test future dates raise error
        for pin_str, pin_format in future_test_cases:
            from swepin.loose import calculate_luhn_validation_digit

            base_digits: str = pin_str.replace("-", "")[2:-1]
            correct_digit: int = calculate_luhn_validation_digit(base_digits)
            valid_pin: str = pin_str[:-1] + str(correct_digit)

            with pytest.raises(ValueError):
                SwePinStrict(valid_pin, pin_format)

    def test_inherited_functionality(self):
        """Test that all inherited functionality works correctly."""
        pin = SwePinStrict("19801224-1231", PinFormat.LONG_WITH_SEPARATOR)

        # Test properties
        assert isinstance(pin.birth_date, date)
        assert pin.birth_date == date(1980, 12, 24)
        assert isinstance(pin.age, int)
        assert pin.male
        assert not pin.female

        # Test format representations
        assert pin.long_str_repr_no_separator == "198012241231"
        assert pin.long_str_repr_w_separator == "19801224-1231"


class TestSwePinStrictInvalidFormats:
    """Test cases for invalid SwePinStrict formats."""

    def test_reject_wrong_format_for_enum(self):
        """Test rejection when PIN doesn't match specified format."""
        # Long format PIN with short format enum
        with pytest.raises(Exception, match="does not match required format"):
            SwePinStrict("19801224-1231", PinFormat.SHORT_WITH_SEPARATOR)

        # Short format PIN with long format enum
        with pytest.raises(Exception, match="does not match required format"):
            SwePinStrict("801224-1231", PinFormat.LONG_WITH_SEPARATOR)

        # With separator PIN using without separator enum
        with pytest.raises(Exception, match="does not match required format"):
            SwePinStrict("19801224-1231", PinFormat.LONG_WITHOUT_SEPARATOR)

        # Without separator PIN using with separator enum
        with pytest.raises(Exception, match="does not match required format"):
            SwePinStrict("198012241231", PinFormat.LONG_WITH_SEPARATOR)

    def test_reject_wrong_length(self):
        """Test rejection of wrong length strings for each format."""
        test_cases: list[tuple[str, PinFormat]] = [
            ("1980122-1231", PinFormat.LONG_WITH_SEPARATOR),  # Too short
            ("198012241-1231", PinFormat.LONG_WITH_SEPARATOR),  # Too long before separator
            ("19801224-12315", PinFormat.LONG_WITH_SEPARATOR),  # Too long after separator
            ("19801224123", PinFormat.LONG_WITHOUT_SEPARATOR),  # Too short
            ("1980122412345", PinFormat.LONG_WITHOUT_SEPARATOR),  # Too long
            ("80122-1231", PinFormat.SHORT_WITH_SEPARATOR),  # Too short
            ("8012241-1231", PinFormat.SHORT_WITH_SEPARATOR),  # Too long before separator
            ("801224123", PinFormat.SHORT_WITHOUT_SEPARATOR),  # Too short
            ("80122412345", PinFormat.SHORT_WITHOUT_SEPARATOR),  # Too long
        ]

        for invalid_pin, pin_format in test_cases:
            with pytest.raises(Exception, match="does not match required format"):
                SwePinStrict(invalid_pin, pin_format)

    def test_reject_non_numeric_parts(self):
        """Test rejection of non-numeric parts."""
        test_cases: list[tuple[str, PinFormat]] = [
            ("ABCD1224-1231", PinFormat.LONG_WITH_SEPARATOR),
            ("198O1224-1231", PinFormat.LONG_WITH_SEPARATOR),
            ("19801224-ABCD", PinFormat.LONG_WITH_SEPARATOR),
            ("ABCD12241231", PinFormat.LONG_WITHOUT_SEPARATOR),
            ("AB1224-1231", PinFormat.SHORT_WITH_SEPARATOR),
            ("AB12241231", PinFormat.SHORT_WITHOUT_SEPARATOR),
        ]

        for invalid_pin, pin_format in test_cases:
            with pytest.raises(Exception, match="does not match required format"):
                SwePinStrict(invalid_pin, pin_format)

    def test_reject_non_string_input(self):
        """Test rejection of non-string input."""
        with pytest.raises(Exception, match="Swedish personal identity number must be a string"):
            SwePinStrict(198012241234, PinFormat.LONG_WITHOUT_SEPARATOR)

    def test_reject_invalid_luhn_validation(self):
        """Test rejection of invalid Luhn validation digit."""
        test_cases: list[tuple[str, PinFormat]] = [
            ("19801224-1235", PinFormat.LONG_WITH_SEPARATOR),
            ("198012241235", PinFormat.LONG_WITHOUT_SEPARATOR),
            ("801224-1235", PinFormat.SHORT_WITH_SEPARATOR),
            ("8012241235", PinFormat.SHORT_WITHOUT_SEPARATOR),
        ]

        for invalid_pin, pin_format in test_cases:
            with pytest.raises(Exception, match="Validation digit did not match"):
                SwePinStrict(invalid_pin, pin_format)


class TestSwePinStrictEdgeCases:
    """Test edge cases for SwePinStrict."""

    def test_coordination_number_luhn_validation(self):
        from swepin.loose import calculate_luhn_validation_digit

        # Valid coordination number (day 84 = 24 + 60)
        base_digits: str = "801284123"
        correct_digit: int = calculate_luhn_validation_digit(base_digits)

        valid_coord_pin: str = f"19801284-123{correct_digit}"

        # Should not raise exception
        pin = SwePinStrict(valid_coord_pin, PinFormat.LONG_WITH_SEPARATOR)
        assert pin.is_coordination_number
        assert pin.coordination_number == "84"
        assert pin.calculated_day_from_coordination_number == "24"

        # Invalid validation digit
        wrong_digit: int = (correct_digit + 1) % 10
        invalid_coord_pin: str = f"19801284-123{wrong_digit}"

        with pytest.raises(Exception, match="Validation digit did not match"):
            SwePinStrict(invalid_coord_pin, PinFormat.LONG_WITH_SEPARATOR)

    def test_leap_year_dates(self):
        """Test leap year dates in strict format."""
        from swepin.loose import calculate_luhn_validation_digit

        base_digits = "80022912"
        validation_digit = calculate_luhn_validation_digit(base_digits + "3")
        pin_str = f"19800229-123{validation_digit}"

        pin = SwePinStrict(pin_str, PinFormat.LONG_WITH_SEPARATOR)
        assert pin.birth_date == date(1980, 2, 29)

    def test_custom_reference_date(self):
        """Test SwePinStrict with custom reference date."""
        reference_date = date(2020, 1, 1)
        pin = SwePinStrict("19801224-1231", PinFormat.LONG_WITH_SEPARATOR, today=reference_date)

        expected_age = 2020 - 1980 - 1
        assert pin.age == expected_age
        assert pin.today == reference_date

    def test_all_format_combinations(self):
        """Test that all format combinations work with same PIN data."""
        from swepin.loose import calculate_luhn_validation_digit

        base_digits = "8012241"
        correct_digit = calculate_luhn_validation_digit(base_digits + "23")

        pins = [
            SwePinStrict(f"19801224-123{correct_digit}", PinFormat.LONG_WITH_SEPARATOR),
            SwePinStrict(f"19801224123{correct_digit}", PinFormat.LONG_WITHOUT_SEPARATOR),
            SwePinStrict(f"801224-123{correct_digit}", PinFormat.SHORT_WITH_SEPARATOR),
            SwePinStrict(f"801224123{correct_digit}", PinFormat.SHORT_WITHOUT_SEPARATOR),
        ]

        # All should represent the same person
        for pin in pins:
            assert pin.full_year == "1980"
            assert pin.month == "12"
            assert pin.day == "24"
            assert pin.birth_date == date(1980, 12, 24)


class TestSwePinStrictFormatProperties:
    """Test format property consistency in SwePinStrict."""

    def test_format_consistency(self):
        """Test that all format properties are consistent."""
        pin = SwePinStrict("19801224-1231", PinFormat.LONG_WITH_SEPARATOR)

        assert pin.long_str_repr_w_separator == "19801224-1231"
        assert len(pin.long_str_repr_no_separator) == 12
        assert len(pin.short_str_repr_w_separator) == 11

    def test_separator_property_matches_format(self):
        """Test that separator property matches the format used."""
        pin_with_sep = SwePinStrict("19801224-1231", PinFormat.LONG_WITH_SEPARATOR)
        assert pin_with_sep.separator == "-"

        pin_without_sep = SwePinStrict("198012241231", PinFormat.LONG_WITHOUT_SEPARATOR)
        assert not pin_without_sep.separator

    def test_json_output(self):
        """Test JSON output for SwePinStrict."""
        pin = SwePinStrict("19801224-1231", PinFormat.LONG_WITH_SEPARATOR)

        import json
        json_data = json.loads(pin.json)
        assert "personal_identity_number" in json_data
        assert json_data["personal_identity_number"] == "19801224-1231"


if __name__ == "__main__":
    pytest.main([__file__])