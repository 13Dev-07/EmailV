"""
Test Suite for Syntax Validator
"""

import unittest
from app.utils.syntax_validator import validate_syntax
from app.utils.exceptions import ValidationError

class TestSyntaxValidator(unittest.TestCase):
    def test_valid_syntax(self):
        email = "user@example.com"
        self.assertTrue(validate_syntax(email))
    
    def test_invalid_syntax_missing_at(self):
        email = "userexample.com"
        with self.assertRaises(ValidationError):
            validate_syntax(email)
    
    def test_invalid_syntax_invalid_domain(self):
        email = "user@.com"
        with self.assertRaises(ValidationError):
            validate_syntax(email)
    
    def test_valid_syntax_with_subdomain(self):
        email = "user@mail.example.com"
        self.assertTrue(validate_syntax(email))

if __name__ == '__main__':
    unittest.main()