import unittest
from tesseral_flask.credentials import is_jwt_format, is_api_key_format


class TestCredentials(unittest.TestCase):
    def test_is_jwt_format_valid(self):
        valid_jwt = (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
            ".eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6"
            "IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"
            ".SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        )
        self.assertTrue(is_jwt_format(valid_jwt))

    def test_is_jwt_format_missing_part(self):
        self.assertFalse(is_jwt_format("header.payload"))

    def test_is_jwt_format_invalid_characters(self):
        invalid_jwt = "header.payload.with=illegal&chars"
        self.assertFalse(is_jwt_format(invalid_jwt))

    def test_is_jwt_format_empty_string(self):
        self.assertFalse(is_jwt_format(""))

    def test_is_jwt_format_extra_segment(self):
        self.assertFalse(is_jwt_format("a.b.c.d"))

    def test_is_api_key_format_valid(self):
        self.assertTrue(is_api_key_format("abc123_test_underscore"))

    def test_is_api_key_format_uppercase(self):
        self.assertFalse(is_api_key_format("ABC123"))

    def test_is_api_key_format_invalid_characters(self):
        self.assertFalse(is_api_key_format("key-with-dash"))

    def test_is_api_key_format_spaces(self):
        self.assertFalse(is_api_key_format("key with space"))

    def test_is_api_key_format_empty_string(self):
        self.assertFalse(is_api_key_format(""))


if __name__ == "__main__":
    unittest.main()
