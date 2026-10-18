import unittest

from ai import (
    check_ai_response,
    mask_sensitive_data,
)


class TestPrivacyProtection(unittest.TestCase):

    def test_email_is_masked(self):
        text = "Contact demo.person@example.com for details"
        masked = mask_sensitive_data(text)

        self.assertNotIn(
            "demo.person@example.com",
            masked,
        )

    def test_pan_is_masked(self):
        text = "Demo PAN: ABCDE1234F"
        masked = mask_sensitive_data(text)

        self.assertNotIn("ABCDE1234F", masked)

    def test_ai_response_is_checked(self):
        response = (
            "Please contact demo.person@example.com for help."
        )
        result = check_ai_response(response)

        self.assertNotIn(
            "demo.person@example.com",
            result["response"],
        )

    def test_normal_text_does_not_crash(self):
        text = "Explain the basics of encryption."
        masked = mask_sensitive_data(text)

        self.assertIsInstance(masked, str)
        self.assertTrue(masked)


if __name__ == "__main__":
    unittest.main()
