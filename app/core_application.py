"""
Core Application Module
Initializes and starts the Ultimate Email Validation System.
"""

from app.utils.logger import setup_logger
from app.api_service import run as run_api_service
from app.database import init_db

def main():
    """
    Main function to start the application.
    """
    logger = setup_logger('CoreApplication')
    logger.info("Initializing Ultimate Email Validation System...")
    
    # Initialize the database
    init_db()
    
    # Start the API Service
    run_api_service()
    
    logger.info("Ultimate Email Validation System is running.")

if __name__ == '__main__':
    main()