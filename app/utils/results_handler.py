"""
Results Handler Module
Processes and formats validation results.
"""

from typing import Dict, List
import json
import os
from app.utils.logger import setup_logger
from app.database import SessionLocal, ValidationResult
from sqlalchemy.exc import SQLAlchemyError

logger = setup_logger('ResultsHandler')


def format_results_as_json(validation_result: Dict) -> str:
    """
    Formats the validation results as a JSON string.
    
    Args:
        validation_result (Dict): The dictionary containing validation results.
    
    Returns:
        str: JSON-formatted string of the validation results.
    """
    try:
        return json.dumps(validation_result, indent=4)
    except (TypeError, ValueError) as e:
        logger.error(f"Error formatting results as JSON: {e}")
        return json.dumps({"error": "Failed to format results."})


def save_results_to_file(validation_results: List[Dict], filepath: str = 'results/validation_results.json') -> bool:
    """
    Saves the validation results to a specified JSON file.
    
    Args:
        validation_results (List[Dict]): A list of dictionaries containing validation results.
        filepath (str): The path to the file where results will be saved.
    
    Returns:
        bool: True if save is successful, False otherwise.
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as file:
            json.dump(validation_results, file, indent=4)
        logger.info(f"Validation results saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Failed to save validation results to {filepath}: {e}")
        return False


def save_results_to_db(validation_results: List[Dict]) -> bool:
    """
    Saves the validation results to the PostgreSQL database.
    
    Args:
        validation_results (List[Dict]): A list of dictionaries containing validation results.
    
    Returns:
        bool: True if save is successful, False otherwise.
    """
    session = SessionLocal()
    try:
        for result in validation_results:
            validation_record = ValidationResult(
                email=result.get("email"),
                syntax_valid=result.get("syntax_valid", False),
                domain_exists=result.get("domain_exists", False),
                mx_records_valid=result.get("mx_records_valid", False),
                smtp_verified=result.get("smtp_verified", False),
                disposable=result.get("disposable", False),
                role_account=result.get("role_account", False),
                typo_detected=result.get("typo_detected", False),
                typo_suggestion=result.get("typo_suggestion"),
                domain_reputation=result.get("domain_reputation", 0.0),
                spam_trap=result.get("spam_trap", False),
                catch_all=result.get("catch_all", False),
                risk_score=result.get("risk_score", 0.0),
                status=result.get("status", "Invalid")
            )
            session.add(validation_record)
        session.commit()
        logger.info("Validation results saved to the database successfully.")
        return True
    except SQLAlchemyError as e:
        session.rollback()
        logger.error(f"Database error while saving results: {e}")
        return False
    finally:
        session.close()


def log_results(validation_result: Dict) -> None:
    """
    Logs the validation results using the application's logging system.
    
    Args:
        validation_result (Dict): The dictionary containing validation results.
    """
    try:
        formatted_results = format_results_as_json(validation_result)
        logger.info(f"Email Validation Results:\n{formatted_results}")
    except Exception as e:
        logger.error(f"Failed to log validation results: {e}")