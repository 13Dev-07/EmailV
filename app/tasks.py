"""
Celery Tasks Module
Defines asynchronous tasks for email validation.
"""

from app.celery_app import celery
from app.utils.validation_orchestrator import validate_email
from app.utils.logger import setup_logger
from app.utils.results_handler import log_results, save_results_to_file, save_results_to_db

logger = setup_logger('CeleryTasks')


@celery.task
def validate_email_task(email: str, save: bool = False, output: str = 'results/validation_results.json'):
    """
    Celery task to validate an email address.

    Args:
        email (str): The email address to validate.
        save (bool): Whether to save the results to a file.
        output (str): The file path to save the results.
    """
    logger.info(f"Starting asynchronous validation for email: {email}")
    try:
        validation_result = validate_email(email)
        log_results(validation_result)
        if save:
            save_results_to_file([validation_result], output)
        logger.info(f"Completed asynchronous validation for email: {email}")
        return validation_result
    except Exception as e:
        logger.error(f"Error in asynchronous validation for {email}: {e}")
        return {"email": email, "error": str(e)}