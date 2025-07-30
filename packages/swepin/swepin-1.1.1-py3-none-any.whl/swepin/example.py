from swepin.generate import generate_valid_pins
pins = generate_valid_pins(count=3)
for pin in pins:
    print(pin)
    print(pin.pretty_print())
