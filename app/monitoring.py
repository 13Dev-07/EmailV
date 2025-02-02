"""Monitoring and metrics tracking for the Email Validator Service."""

import time
from typing import Dict, Optional
from datetime import datetime
from app.supabase_client import DatabaseClient
from app.monitoring.prometheus_metrics import (
    email_validation_requests_total,
    email_validation_duration_seconds,
    validation_errors_total
)

class MetricsTracker:
    """Track and store service metrics."""
    
    def __init__(self, db_client: DatabaseClient):
        self.db = db_client
        self.start_time = time.time()
    
    async def track_validation_request(
        self,
        user_id: str,
        email: str,
        validation_time: float,
        success: bool,
        error: Optional[str] = None
    ) -> None:
        """Track a validation request."""
        try:
            # Update Prometheus metrics
            status = "success" if success else "failure"
            email_validation_requests_total.labels(status=status).inc()
            email_validation_duration_seconds.observe(validation_time)
            
            if error:
                validation_errors_total.labels(error_type=error).inc()
            
            # Store in database
            await self.db.supabase.from_("audit_logs").insert({
                "user_id": user_id,
                "action": "email_validation",
                "details": {
                    "email": email,
                    "validation_time_ms": validation_time * 1000,
                    "success": success,
                    "error": error,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }).execute()
        except Exception as e:
            # Log error but don't fail the request
            print(f"Error tracking metrics: {str(e)}")
    
    async def get_user_metrics(self, user_id: str) -> Dict:
        """Get metrics for a specific user."""
        try:
            # Get validation counts
            validations = await self.db.supabase.from_("validation_results")\
                .select("*", count="exact")\
                .eq("user_id", user_id)\
                .execute()
            
            # Get error counts
            errors = await self.db.supabase.from_("audit_logs")\
                .select("*", count="exact")\
                .eq("user_id", user_id)\
                .eq("details->success", False)\
                .execute()
            
            # Get usage stats
            usage = await self.db.supabase.from_("usage_quotas")\
                .select("*")\
                .eq("user_id", user_id)\
                .single()\
                .execute()
            
            return {
                "total_validations": validations.count,
                "total_errors": errors.count,
                "current_usage": usage.data["current_usage"],
                "monthly_limit": usage.data["monthly_limit"],
                "usage_percentage": (usage.data["current_usage"] / usage.data["monthly_limit"]) * 100
            }
        except Exception as e:
            print(f"Error getting user metrics: {str(e)}")
            return {}
    
    async def get_system_metrics(self) -> Dict:
        """Get overall system metrics."""
        try:
            # Get total validation count
            validations = await self.db.supabase.from_("validation_results")\
                .select("*", count="exact")\
                .execute()
            
            # Get total user count
            users = await self.db.supabase.from_("users")\
                .select("*", count="exact")\
                .execute()
            
            # Get error rate
            errors = await self.db.supabase.from_("audit_logs")\
                .select("*", count="exact")\
                .eq("details->success", False)\
                .execute()
            
            uptime = time.time() - self.start_time
            
            return {
                "total_validations": validations.count,
                "total_users": users.count,
                "error_rate": (errors.count / validations.count) if validations.count > 0 else 0,
                "uptime_seconds": uptime
            }
        except Exception as e:
            print(f"Error getting system metrics: {str(e)}")
            return {}