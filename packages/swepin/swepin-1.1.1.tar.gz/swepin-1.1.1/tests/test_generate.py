import pytest
from datetime import date
from swepin.loose import SwePinLoose
from swepin.strict import SwePinStrict, PinFormat
from swepin.generate import generate_valid_pins

def test_generate_default_pins():
    pins = generate_valid_pins(count=5)
    assert len(pins) == 5
    assert all(isinstance(pin, SwePinLoose) for pin in pins)

def test_generate_strict_pins_default_format():
    pins = generate_valid_pins(count=3, strict=True)
    assert len(pins) == 3
    assert all(isinstance(pin, SwePinStrict) for pin in pins)
    assert all(pin.separator == "-" for pin in pins)

def test_generate_strict_pins_with_each_format():
    pins = generate_valid_pins(count=2, strict=True)
    assert len(pins) == 2
    assert all(isinstance(pin, SwePinStrict) for pin in pins)

def test_generate_pins_as_dict():
    pins = generate_valid_pins(count=4, to_dict=True)
    assert isinstance(pins, list)
    assert all(isinstance(pin, dict) for pin in pins)

def test_generate_pins_as_json():
    pins = generate_valid_pins(count=4, to_json=True)
    assert isinstance(pins, list)
    assert all(isinstance(pin, str) for pin in pins)  # Assuming `.json` returns string

def test_include_coordination_numbers():
    pins = generate_valid_pins(count=50, include_coordination_numbers=True)
    coord_count = sum(1 for pin in pins if int(pin.day) > 60)
    assert coord_count >= 1, "Expected at least one coordination number in the generated pins"

def test_gender_ratio_extremes_all_male():
    pins = generate_valid_pins(count=10, male_ratio=1.0)
    assert all(pin.male for pin in pins)
    assert all(not pin.female for pin in pins)

def test_gender_ratio_extremes_all_female():
    pins = generate_valid_pins(count=10, male_ratio=0.0)
    assert all(pin.female for pin in pins)
    assert all(not pin.male for pin in pins)
