"""Database models for the Email Validator Service."""

from typing import Dict

class User:
    """User model representing database structure."""
    
    def __init__(self, id: str, email: str, role: str = "user"):
        self.id = id
        self.email = email
        self.role = role

    @classmethod
    def from_db(cls, data: Dict) -> "User":
        """Create User instance from database data."""
        return cls(
            id=data["id"],
            email=data["email"],
            role=data.get("role", "user")
        )

class ValidationResult:
    """Model for email validation results."""
    
    def __init__(self, 
                 id: str,
                 email: str,
                 results: Dict,
                 user_id: str,
                 created_at: str):
        self.id = id
        self.email = email
        self.results = results
        self.user_id = user_id
        self.created_at = created_at

    @classmethod
    def from_db(cls, data: Dict) -> "ValidationResult":
        """Create ValidationResult instance from database data."""
        return cls(
            id=data["id"],
            email=data["email"],
            results=data["results"],
            user_id=data["user_id"],
            created_at=data["created_at"]
        )