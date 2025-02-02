"""
Test Suite for API Service
"""

import unittest
from app.api_service import app
import json

class TestApiService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_validate_valid_email(self):
        response = self.app.post('/validate', 
                                 data=json.dumps({"email": "test@gmail.com"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get("syntax_valid"))
        self.assertEqual(data.get("status"), "Valid")
    
    def test_validate_invalid_email_syntax(self):
        response = self.app.post('/validate', 
                                 data=json.dumps({"email": "invalid-email"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Invalid email syntax.", data.get("error"))
    
    def test_validate_rate_limiter(self):
        # Simulate exceeding rate limit
        for _ in range(101):
            self.app.post('/validate', 
                          data=json.dumps({"email": "test@gmail.com"}),
                          content_type='application/json')
        response = self.app.post('/validate', 
                                 data=json.dumps({"email": "test@gmail.com"}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 429)
        data = json.loads(response.data)
        self.assertIn("Rate limit exceeded", data.get("error"))

if __name__ == '__main__':
    unittest.main()