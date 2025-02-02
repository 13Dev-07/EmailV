"""Supabase client implementation for the Email Validator Service."""

from supabase import create_client
import os
from dotenv import load_dotenv
from typing import Optional, Dict, List
from datetime import datetime

# Load environment variables
load_dotenv()

class DatabaseClient:
    """Main Supabase database client class."""
    
    def __init__(self):
        """Initialize Supabase client with environment variables."""
        self.supabase = create_client(
            os.getenv("SUPABASE_URL"),
            os.getenv("SUPABASE_KEY")
        )

class UserManager:
    """Handle user-related database operations."""
    
    def __init__(self, db_client: DatabaseClient):
        """Initialize with database client."""
        self.db = db_client

    async def create_user(self, email: str, password: str, role: str = "user") -> Dict:
        """Create a new user in the system."""
        try:
            # Create user in auth system
            user = await self.db.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            # Store additional user data
            profile = await self.db.supabase.from_("users").insert({
                "id": user.user.id,
                "email": email,
                "role": role
            }).execute()
            
            # Initialize usage quota
            await self.db.supabase.from_("usage_quotas").insert({
                "user_id": user.user.id,
                "monthly_limit": 1000,
                "current_usage": 0
            }).execute()
            
            # Log user creation
            await self.db.supabase.from_("audit_logs").insert({
                "user_id": user.user.id,
                "action": "user_created",
                "details": {
                    "email": email,
                    "role": role
                }
            }).execute()
            
            return {"user": user, "profile": profile}
        except Exception as e:
            raise DatabaseError(f"Error creating user: {str(e)}")

    async def validate_api_key(self, api_key: str) -> Optional[str]:
        """Validate an API key and return the associated user ID if valid."""
        try:
            result = await self.db.supabase.rpc('check_api_key', {'api_key': api_key}).execute()
            return result.data
        except Exception as e:
            raise DatabaseError(f"Error validating API key: {str(e)}")

    async def revoke_api_key(self, api_key: str, user_id: str) -> bool:
        """Revoke an API key."""
        try:
            result = await self.db.supabase.from_("api_keys")\
                .update({"revoked": True})\
                .eq("key_hash", api_key)\
                .eq("user_id", user_id)\
                .execute()
            return True
        except Exception as e:
            raise DatabaseError(f"Error revoking API key: {str(e)}")

    async def generate_api_key(self, user_id: str) -> str:
        """Generate and store new API key for user."""
        try:
            # Generate new API key using database function
            api_key_result = await self.db.supabase.rpc('generate_api_key').execute()
            api_key = api_key_result.data
            
            # Hash the API key
            key_hash_result = await self.db.supabase.rpc('hash_api_key', {'api_key': api_key}).execute()
            key_hash = key_hash_result.data
            
            # Store the hashed key
            await self.db.supabase.from_('api_keys').insert({
                'user_id': user_id,
                'key_hash': key_hash,
                'name': f'api_key_{datetime.utcnow().strftime("%Y%m%d_%H%M%S")}'
            }).execute()
            
            return api_key
        except Exception as e:
            raise DatabaseError(f"Error generating API key: {str(e)}")

class ValidationManager:
    """Handle validation-related database operations."""
    
    def __init__(self, db_client: DatabaseClient):
        """Initialize with database client."""
        self.db = db_client

    async def store_validation_result(self, email: str, results: Dict, user_id: str) -> Dict:
        """Store email validation results."""
        try:
            # Check usage quota
            quota_check = await self.db.supabase.rpc('check_usage_quota', {'user_id': user_id}).execute()
            if not quota_check.data:
                raise DatabaseError("Usage quota exceeded")

            # Store validation result
            result = await self.db.supabase.from_("validation_results").insert({
                "email": email,
                "results": results,
                "user_id": user_id,
                "created_at": "now()"
            }).execute()

            # Log the validation operation
            await self.db.supabase.from_("audit_logs").insert({
                "user_id": user_id,
                "action": "email_validation",
                "details": {
                    "email": email,
                    "timestamp": "now()"
                }
            }).execute()

            return result
        except Exception as e:
            raise DatabaseError(f"Error storing validation result: {str(e)}")

    async def get_validation_history(self, user_id: str) -> List[Dict]:
        """Retrieve validation history for a user."""
        try:
            history = await self.db.supabase.from_("validation_results")\
                .select("*")\
                .eq("user_id", user_id)\
                .execute()
            return history
        except Exception as e:
            raise DatabaseError(f"Error retrieving validation history: {str(e)}")
            
    async def get_usage_statistics(self, user_id: str) -> Dict:
        """Get usage statistics for a user."""
        try:
            quota = await self.db.supabase.from_("usage_quotas")\
                .select("*")\
                .eq("user_id", user_id)\
                .single()\
                .execute()
            return quota
        except Exception as e:
            raise DatabaseError(f"Error retrieving usage statistics: {str(e)}")

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass