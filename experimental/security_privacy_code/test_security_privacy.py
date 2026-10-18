"""Basic tests for RBAC and encryption. Run: python -m unittest."""
import unittest
from access_control import has_permission, require_permission
from encryption import encrypt_text, decrypt_text


class SecurityPrivacyTests(unittest.TestCase):
    def test_employee_can_submit_activity(self):
        self.assertTrue(has_permission("employee", "submit_activity"))

    def test_employee_cannot_view_audit_logs(self):
        self.assertFalse(has_permission("employee", "view_audit_logs"))
        with self.assertRaises(PermissionError):
            require_permission("employee", "view_audit_logs")

    def test_encryption_round_trip(self):
        message = "demo-only sensitive text"
        ciphertext, key = encrypt_text(message)
        self.assertNotEqual(ciphertext, message)
        self.assertEqual(decrypt_text(ciphertext, key), message)


if __name__ == "__main__":
    unittest.main()
