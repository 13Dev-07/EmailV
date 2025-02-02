"""
Main Entry Point for Email Validation CLI
Allows users to validate emails directly from the command line.
"""

import argparse
from app.utils.validation_orchestrator import validate_email
from app.utils.results_handler import log_results, save_results_to_file
from app.utils.logger import setup_logger

def parse_arguments():
    """
    Parses command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description='Ultimate Email Validation System - CLI',
        epilog='Example usage: python main.py user@example.com another.user@domain.com --save'
    )
    parser.add_argument(
        'emails',
        metavar='EMAIL',
        type=str,
        nargs='+',
        help='Email addresses to validate'
    )
    parser.add_argument(
        '--save',
        action='store_true',
        help='Save validation results to a file'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='results/validation_results.json',
        help='Path to save the validation results JSON file (default: results/validation_results.json)'
    )
    return parser.parse_args()

def main():
    """
    Main function to execute email validations based on CLI input.
    """
    # Initialize logger
    logger = setup_logger('MainCLI')
    
    # Parse arguments
    args = parse_arguments()
    
    # Prepare list to hold all validation results
    all_results = []
    
    # Iterate over each email and perform validation
    for email in args.emails:
        logger.info(f"Starting validation for email: {email}")
        try:
            validation_result = validate_email(email)
            log_results(validation_result)
            all_results.append(validation_result)
            logger.info(f"Completed validation for email: {email}")
        except Exception as e:
            logger.error(f"Error validating email {email}: {e}")
            all_results.append({
                "email": email,
                "error": str(e)
            })
    
    # Save results to file if requested
    if args.save:
        success = save_results_to_file(all_results, args.output)
        if success:
            logger.info(f"All validation results saved to {args.output}")
        else:
            logger.error(f"Failed to save validation results to {args.output}")

if __name__ == '__main__':
    main()