"""
Disposable Email Detector Module
Identifies and blocks disposable or temporary email addresses.
"""

import requests
from app.utils.exceptions import ValidationError

DISPOSABLE_EMAIL_API_URL = "https://api.disposable-email-detector.com/check"

def is_disposable_email(email: str) -> bool:
    """
    Checks if the provided email is from a disposable email provider.
    
    Args:
        email (str): The email address to check.
    
    Returns:
        bool: True if disposable, False otherwise.
    """
    domain = email.split('@')[-1]
    try:
        response = requests.get(f"{DISPOSABLE_EMAIL_API_URL}?domain={domain}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("is_disposable", False)
        else:
            # If API fails, assume not disposable to avoid false negatives
            return False
    except requests.RequestException as e:
        # Log the exception and default to non-disposable
        print(f"Disposable Email Detection Failed: {e}")
        return False