"""Load testing suite for email validation service.

This module contains load testing scenarios using locust to simulate
various levels of concurrent user access and API requests.
"""
from locust import HttpUser, task, between
import json

class EmailValidationUser(HttpUser):
    wait_time = between(1, 2)
    
    def on_start(self):
        """Setup test user with API key."""
        # TODO: Implement API key acquisition for load testing
        self.api_key = "test_key"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
    
    @task(1)
    def validate_single_email(self):
        """Test single email validation endpoint."""
        payload = {
            "email": "test@example.com"
        }
        self.client.post(
            "/api/v1/validate",
            json=payload,
            headers=self.headers
        )
    
    @task(2)
    def validate_bulk_emails(self):
        """Test bulk email validation endpoint."""
        payload = {
            "emails": [
                "test1@example.com",
                "test2@example.com",
                "test3@example.com"
            ]
        }
        self.client.post(
            "/api/v1/validate/bulk",
            json=payload,
            headers=self.headers
        )