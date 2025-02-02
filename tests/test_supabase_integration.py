"""Integration tests for Supabase database implementation."""

import pytest
import asyncio
from app.supabase_client import DatabaseClient, UserManager, ValidationManager, DatabaseError
from datetime import datetime

@pytest.fixture
async def db_client():
    """Create database client fixture."""
    return DatabaseClient()

@pytest.fixture
async def user_manager(db_client):
    """Create user manager fixture."""
    return UserManager(db_client)

@pytest.fixture
async def validation_manager(db_client):
    """Create validation manager fixture."""
    return ValidationManager(db_client)

@pytest.mark.asyncio
async def test_user_creation(user_manager):
    """Test user creation flow."""
    email = f"test_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}@example.com"
    password = "TestPassword123!"
    
    try:
        result = await user_manager.create_user(email, password)
        assert result["user"] is not None
        assert result["profile"] is not None
        assert result["profile"]["email"] == email
    except DatabaseError as e:
        pytest.fail(f"User creation failed: {str(e)}")

@pytest.mark.asyncio
async def test_api_key_generation(user_manager):
    """Test API key generation and validation."""
    # First create a test user
    email = f"test_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}@example.com"
    user_result = await user_manager.create_user(email, "TestPassword123!")
    user_id = user_result["user"].user.id

    try:
        # Generate API key
        api_key = await user_manager.generate_api_key(user_id)
        assert api_key is not None
        
        # Validate API key
        validated_user_id = await user_manager.validate_api_key(api_key)
        assert validated_user_id == user_id
        
        # Revoke API key
        revoked = await user_manager.revoke_api_key(api_key, user_id)
        assert revoked is True
        
        # Validate revoked key
        revoked_validation = await user_manager.validate_api_key(api_key)
        assert revoked_validation is None
    except DatabaseError as e:
        pytest.fail(f"API key operations failed: {str(e)}")

@pytest.mark.asyncio
async def test_validation_storage(validation_manager, user_manager):
    """Test storing validation results."""
    # Create test user
    email = f"test_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}@example.com"
    user_result = await user_manager.create_user(email, "TestPassword123!")
    user_id = user_result["user"].user.id

    validation_result = {
        "syntax_valid": True,
        "domain_exists": True,
        "disposable": False,
        "risk_score": 0.1
    }

    try:
        # Store result
        result = await validation_manager.store_validation_result(
            "test@example.com",
            validation_result,
            user_id
        )
        assert result is not None

        # Get validation history
        history = await validation_manager.get_validation_history(user_id)
        assert len(history) > 0
        assert history[0]["email"] == "test@example.com"
    except DatabaseError as e:
        pytest.fail(f"Validation storage failed: {str(e)}")

@pytest.mark.asyncio
async def test_usage_tracking(validation_manager, user_manager):
    """Test usage quota tracking."""
    # Create test user
    email = f"test_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}@example.com"
    user_result = await user_manager.create_user(email, "TestPassword123!")
    user_id = user_result["user"].user.id

    try:
        # Get initial usage
        initial_stats = await validation_manager.get_usage_statistics(user_id)
        initial_usage = initial_stats["current_usage"]

        # Perform some validations
        for _ in range(3):
            await validation_manager.store_validation_result(
                "test@example.com",
                {"syntax_valid": True},
                user_id
            )

        # Check updated usage
        updated_stats = await validation_manager.get_usage_statistics(user_id)
        assert updated_stats["current_usage"] == initial_usage + 3
    except DatabaseError as e:
        pytest.fail(f"Usage tracking failed: {str(e)}")

if __name__ == "__main__":
    asyncio.run(pytest.main([__file__]))