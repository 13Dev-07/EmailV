"""
Test Suite for Results Handler
"""

import unittest
import os
import json
from app.utils.results_handler import format_results_as_json, save_results_to_file, log_results
from app.utils.logger import setup_logger

logger = setup_logger('TestResultsHandler')


class TestResultsHandler(unittest.TestCase):
    def setUp(self):
        self.validation_result = {
            "email": "user@example.com",
            "syntax_valid": True,
            "domain_exists": True,
            "mx_records_valid": True,
            "smtp_verified": True,
            "disposable": False,
            "role_account": False,
            "typo_detected": False,
            "typo_suggestion": None,
            "domain_reputation": 80,
            "spam_trap": False,
            "catch_all": False,
            "risk_score": 10,
            "status": "Valid"
        }
        self.test_filepath = 'tests/results/test_validation_results.json'
    
    def tearDown(self):
        # Clean up the test file if it exists
        if os.path.exists(self.test_filepath):
            os.remove(self.test_filepath)
    
    def test_format_results_as_json(self):
        json_output = format_results_as_json(self.validation_result)
        self.assertIsInstance(json_output, str)
        parsed_json = json.loads(json_output)
        self.assertEqual(parsed_json, self.validation_result)
    
    def test_save_results_to_file_success(self):
        result = save_results_to_file(self.validation_result, self.test_filepath)
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.test_filepath))
        with open(self.test_filepath, 'r') as file:
            data = json.load(file)
            self.assertEqual(data, self.validation_result)
    
    def test_save_results_to_file_failure(self):
        # Attempt to save to an invalid directory
        invalid_filepath = '/invalid_path/test_validation_results.json'
        result = save_results_to_file(self.validation_result, invalid_filepath)
        self.assertFalse(result)
    
    def test_log_results(self):
        # This test checks if logging does not raise any exceptions
        try:
            log_results(self.validation_result)
        except Exception as e:
            self.fail(f"log_results raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()