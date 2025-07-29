import string
import unittest

from terminusgps.wialon import utils


class WialonUtilsTestCase(unittest.TestCase):
    def test_generate_wialon_password_min_length(self) -> None:
        with self.assertRaises(ValueError) as context:
            utils.generate_wialon_password(length=7)
        self.assertTrue(
            "Password cannot be less than 8 characters in length, got 7."
            in str(context.exception)
        )

    def test_generate_wialon_password_max_length(self) -> None:
        with self.assertRaises(ValueError) as context:
            utils.generate_wialon_password(length=65)
        self.assertTrue(
            "Password cannot be greater than 64 characters in length, got 65."
            in str(context.exception)
        )

    def test_generate_wialon_password_valid(self) -> None:
        password = utils.generate_wialon_password()
        s0 = list(string.ascii_uppercase)
        s1 = list(string.ascii_lowercase)
        s2 = list(string.digits)
        s3 = list("!@#$%^*()[]-_+")

        if len(password) < 8 or len(password) > 64:
            self.fail(f"Generated password was {len(password)} chars in length.")
        if not any([c for c in password if c in s0]):
            self.fail("Generated password did not contain an uppercase letter.")
        if not any([c for c in password if c in s1]):
            self.fail("Generated password did not contain a lowercase letter.")
        # TODO: Make this check for 3 digits
        if not any([c for c in password if c in s2]):
            self.fail("Generated password did not contain a digit.")
        if not any([c for c in password if c in s3]):
            self.fail("Generated password did not contain a special symbol.")
