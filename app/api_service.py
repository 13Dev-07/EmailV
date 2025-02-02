"""
API Service for email validation.

This module provides the REST API endpoints for email validation services.
Includes both synchronous and asynchronous validation endpoints.
"""

from functools import wraps
from flask import jsonify, request, current_app as app
from celery.result import AsyncResult
import json

from .utils.logger import logger
from .utils.authentication import validate_api_key
from .utils.exceptions import RateLimitError
from .tasks import validate_email_batch
from .utils.rate_limiter import rate_limiter

def require_api_key(f):
    """
    Decorator to require API key authentication for endpoints.
    
    Args:
        f: The function to wrap
        
    Returns:
        decorated function that includes API key validation
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if not api_key:
            logger.warning("API key missing in request headers")
            return jsonify({"error": "API key missing", "status": "error"}), 401
            
        if not validate_api_key(api_key):
            logger.warning("Invalid API key provided")
            return jsonify({"error": "Invalid API key", "status": "error"}), 403
            
        return f(*args, **kwargs)
    return decorated

@app.route('/api/v1/validate_async', methods=['POST'])
@require_api_key
def validate_async():
    """
    Endpoint for asynchronous email validation.
    Accepts a list of emails and enqueues validation tasks.
    
    Request Body:
        {
            "emails": ["email1@domain.com", "email2@domain.com"],
            "save": boolean,  # Optional: save results to file
            "output": "path/to/output.json"  # Optional: output file path
        }
    
    Returns:
        JSON response with task ID and status:
        {
            "task_id": "uuid",
            "status": "success",
            "message": "Validation task created"
        }
        
    Raises:
        400: Bad Request - Invalid input format
        401: Unauthorized - Missing API key
        403: Forbidden - Invalid API key
        429: Too Many Requests - Rate limit exceeded
    """
    try:
        # Rate limiting check
        client_ip = request.remote_addr
        if not rate_limiter.is_allowed(client_ip):
            logger.warning(f"Rate limit exceeded for IP: {client_ip}")
            return jsonify({
                "error": "Rate limit exceeded. Please try again later.",
                "status": "error"
            }), 429

        # Parse and validate request data
        try:
            data = request.get_json()
        except json.JSONDecodeError:
            logger.error("Malformed JSON in request")
            return jsonify({
                "error": "Invalid JSON format",
                "status": "error"
            }), 400

        if not data:
            return jsonify({
                "error": "Empty request body",
                "status": "error"
            }), 400

        emails = data.get('emails', [])
        save = data.get('save', False)
        output = data.get('output', 'results/validation_results.json')

        if not emails:
            logger.warning("No emails provided in the asynchronous request")
            return jsonify({
                "error": "At least one email is required",
                "status": "error"
            }), 400

        if not isinstance(emails, list):
            logger.warning("Emails should be provided as a list")
            return jsonify({
                "error": "Emails must be provided as a list",
                "status": "error"
            }), 400

        # Create async task
        task = validate_email_batch.delay(emails, save=save, output_path=output)
        
        return jsonify({
            "task_id": task.id,
            "status": "success",
            "message": "Validation task created"
        }), 202

    except Exception as e:
        logger.error(f"Unexpected error in validate_async: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "status": "error"
        }), 500

@app.route('/api/v1/validate_async/status/<task_id>', methods=['GET'])
@require_api_key
def get_task_status(task_id):
    """
    Get the status of an async validation task.
    
    Args:
        task_id: The ID of the task to check
        
    Returns:
        JSON response with task status and results if complete:
        {
            "task_id": "uuid",
            "status": "pending|success|failure",
            "results": [...] # Only included if status is "success"
        }
    """
    task = AsyncResult(task_id)
    
    response = {
        "task_id": task_id,
        "status": task.status,
    }
    
    if task.ready():
        if task.successful():
            response["results"] = task.get()
        else:
            response["error"] = str(task.result)
            
    return jsonify(response)