import unittest
from datetime import date
from swepin.loose import SwePinLoose


class TestSwedishPersonalIdentityNumber(unittest.TestCase):
    """Test cases for the SwedishPersonalIdentityNumber class."""

    def test_valid_formats(self):
        """Test various valid input formats."""
        pin1 = SwePinLoose("198012241231")
        self.assertEqual(pin1.full_year, "1980")
        self.assertEqual(pin1.month, "12")
        self.assertEqual(pin1.day, "24")
        self.assertEqual(pin1.birth_number, "123")
        self.assertEqual(pin1.validation_digit, "1")

        pin2 = SwePinLoose("8012241231")
        self.assertEqual(pin2.full_year, "1980")
        self.assertEqual(pin2.month, "12")
        self.assertEqual(pin2.day, "24")
        self.assertEqual(pin2.birth_number, "123")
        self.assertEqual(pin2.validation_digit, "1")

        pin3 = SwePinLoose("19801224-1231")
        self.assertEqual(pin3.full_year, "1980")
        self.assertEqual(pin3.separator, "-")

        pin4 = SwePinLoose("801224-1231")
        self.assertEqual(pin4.full_year, "1980")
        self.assertEqual(pin4.separator, "-")

    def test_coordination_numbers(self):
        """Test coordination numbers (day + 60)."""
        pin = SwePinLoose("199812765452")
        self.assertEqual(pin.day, "76")
        self.assertTrue(pin._is_coordination_number())
        self.assertEqual(pin.birth_date.day, 16)
        self.assertEqual(pin.calculated_day_from_coordination_number, "16")

    def test_centenarians(self):
        """Test handling of people 100 years or older."""
        test_date = date(2024, 3, 1)

        pin1 = SwePinLoose("230101+1231", today=test_date)
        self.assertEqual(pin1.full_year, "1923")
        self.assertEqual(pin1.separator, "+")
        self.assertEqual(pin1.age, 101)

        pin2 = SwePinLoose("19230101-1231", today=test_date)
        self.assertEqual(pin2.full_year, "1923")
        self.assertEqual(pin2.separator, "+")
        self.assertEqual(pin2.age, 101)

    def test_gender(self):
        """Test gender detection."""
        pin_male = SwePinLoose("198012241231")
        self.assertEqual(pin_male.gender_digit, "3")
        self.assertTrue(pin_male.male)
        self.assertFalse(pin_male.female)

        pin_female = SwePinLoose("197911278286")
        self.assertEqual(pin_female.gender_digit, "8")
        self.assertFalse(pin_female.male)
        self.assertTrue(pin_female.female)

    def test_age_calculation(self):
        """Test age calculation for different scenarios."""
        test_date = date(2025, 3, 1)

        pin1 = SwePinLoose("198012241231", today=test_date)
        self.assertEqual(pin1.age, 44)

        pin2 = SwePinLoose("20250127-8283", today=test_date)
        self.assertEqual(pin2.age, 0)

        pin3 = SwePinLoose("20240302-1237", today=test_date)
        self.assertEqual(pin3.age, 0)

        pin4 = SwePinLoose("20240228-1238", today=test_date)
        self.assertEqual(pin4.age, 1)

        pin5 = SwePinLoose("198012241231", today=test_date)
        self.assertEqual(pin5.age, 44)

    def test_validation_digit(self):
        """Test the Luhn algorithm validation."""
        valid_pin = SwePinLoose("198012241231")
        self.assertEqual(valid_pin.validation_digit, "1")

        with self.assertRaises(Exception) as context:
            SwePinLoose("198012241235")
        self.assertIn("Validation digit did not match", str(context.exception))

    def test_invalid_inputs(self):
        """Test various invalid inputs."""
        with self.assertRaises(Exception):
            SwePinLoose(12345678901)

        with self.assertRaises(Exception):
            SwePinLoose("abcdefghijkl")

        with self.assertRaises(Exception):
            SwePinLoose("12345")

        with self.assertRaises(Exception):
            SwePinLoose("1234567890123")

        with self.assertRaises(Exception):
            SwePinLoose("198013241234")

        with self.assertRaises(Exception):
            SwePinLoose("198012321234")

    def test_string_representations(self):
        """Test the different string representations."""
        pin = SwePinLoose("198012241231")

        self.assertEqual(pin.long_str_repr_no_separator, "198012241231")
        self.assertEqual(pin.short_str_repr_no_separator, "8012241231")
        self.assertEqual(pin.long_str_repr_w_separator, "19801224-1231")
        self.assertEqual(pin.short_str_repr_w_separator, "801224-1231")
        self.assertEqual(str(pin), "801224-1231")

    def test_birth_date(self):
        """Test birth date extraction."""
        pin = SwePinLoose("198012241231")
        birth_date = pin.get_birth_date()

        self.assertEqual(birth_date.year, 1980)
        self.assertEqual(birth_date.month, 12)
        self.assertEqual(birth_date.day, 24)

        pin_coord = SwePinLoose("199812165455")
        birth_date_coord = pin_coord.get_birth_date()

        self.assertEqual(birth_date_coord.year, 1998)
        self.assertEqual(birth_date_coord.month, 12)
        self.assertEqual(birth_date_coord.day, 16)

    def test_dictionary_representation(self):
        """Test the dictionary representation."""
        pin = SwePinLoose("198012241231")
        pin_dict = pin.to_dict()

        self.assertEqual(pin_dict["personal_identity_number"], "198012241231")
        self.assertEqual(pin_dict["birth_date"]["full_year"], "1980")
        self.assertEqual(pin_dict["birth_date"]["month"], "12")
        self.assertEqual(pin_dict["birth_date"]["day"], "24")
        self.assertEqual(pin_dict["birth_number"]["complete"], "123")
        self.assertEqual(pin_dict["validation_digit"], "1")
        self.assertEqual(pin_dict["derived_info"]["gender"], "male")
        self.assertFalse(pin_dict["derived_info"]["is_coordination_number"])

    def test_edge_cases(self):
        """Test various edge cases."""
        test_date = date(2024, 3, 1)

        today_pin = SwePinLoose("791127-8286", today=test_date)
        self.assertEqual(today_pin.age, 44)

        leap_year_pin = SwePinLoose("200229-1231", today=test_date)
        self.assertEqual(leap_year_pin.full_year, "2020")
        birth_date = leap_year_pin.birth_date
        self.assertEqual(birth_date.month, 2)
        self.assertEqual(birth_date.day, 29)

        leap_coord_pin = SwePinLoose("791127-8286", today=test_date)
        birth_date = leap_coord_pin.get_birth_date()
        self.assertEqual(birth_date.month, 11)
        self.assertEqual(birth_date.day, 27)

    def test_pretty_print(self):
        """Test that pretty print function runs without errors and contains key data."""
        pin = SwePinLoose("198012241231")
        pretty_output = pin.pretty_print()

        self.assertIn("1980", pretty_output)
        self.assertIn("12", pretty_output)
        self.assertIn("24", pretty_output)
        self.assertIn("123", pretty_output)
        self.assertIn("4", pretty_output)
        self.assertIn("Male", pretty_output)


if __name__ == "__main__":
    unittest.main()
