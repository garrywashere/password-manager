import random
import string


class Generator:
    def __init__(self):
        # Default strength set to 1
        self.strength = 1

        # Character banks for lowercase, uppercase, digits, and special characters
        self.lower_char_bank = list(string.ascii_lowercase)
        self.upper_char_bank = list(string.ascii_uppercase)
        self.digi_bank = list(string.digits)
        self.spec_bank = list("!@#$%^&*_-")

    def generate(self, length, strength):
        # Combine all character banks
        all_chars = (
            self.lower_char_bank
            + self.upper_char_bank
            + self.digi_bank
            + self.spec_bank
        )

        # Ensure strength is at least 1
        strength = strength if not strength < 1 else 1

        # Set minimum length based on strength
        min_length = strength * 4
        if length < min_length:
            length = min_length

        running = True
        while running:
            lower_char_count, upper_char_count, digi_count, spec_count = 0, 0, 0, 0
            password = []

            # Generate a random password
            for x in range(length):
                password.append(random.choice(all_chars))

            # Count the occurrences of each character type
            lower_char_count = sum(
                1 for char in password if char in self.lower_char_bank
            )
            upper_char_count = sum(
                1 for char in password if char in self.upper_char_bank
            )
            digi_count = sum(1 for char in password if char in self.digi_bank)
            spec_count = sum(1 for char in password if char in self.spec_bank)

            # Check if the password meets the strength criteria
            if (
                lower_char_count >= strength
                and upper_char_count >= strength
                and digi_count >= strength
                and spec_count >= strength
            ):
                running = False

            if all(
                count >= strength
                for count in [
                    lower_char_count,
                    upper_char_count,
                    digi_count,
                    spec_count,
                ]
            ):
                running = False

        return "".join(password)
