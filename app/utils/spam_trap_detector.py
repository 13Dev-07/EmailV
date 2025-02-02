"""
Spam Trap Detector Module
Identifies and blocks known spam trap email addresses.
"""

import os
from typing import Set
from app.utils.logger import setup_logger

logger = setup_logger('SpamTrapDetector')

class SpamTrapDetector:
    def __init__(self, spam_trap_file: str = 'config/spam_traps.txt'):
        """
        Initializes the SpamTrapDetector with a list of known spam trap emails.
        
        Args:
            spam_trap_file (str): Path to the file containing spam trap emails.
        """
        self.spam_trap_emails = self.load_spam_trap_emails(spam_trap_file)
        logger.info(f"Loaded {len(self.spam_trap_emails)} known spam trap emails.")

    def load_spam_trap_emails(self, filepath: str) -> Set[str]:
        """
        Loads spam trap emails from a file.
        
        Args:
            filepath (str): Path to the spam trap emails file.
        
        Returns:
            Set[str]: A set of spam trap email addresses.
        """
        spam_traps = set()
        if not os.path.exists(filepath):
            logger.warning(f"Spam trap file not found at {filepath}. Continuing without spam trap detection.")
            return spam_traps
        
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    email = line.strip().lower()
                    if email:
                        spam_traps.add(email)
            logger.debug(f"Loaded spam trap emails from {filepath}.")
        except Exception as e:
            logger.error(f"Error loading spam trap emails from {filepath}: {e}")
        
        return spam_traps

    def is_spam_trap(self, email: str) -> bool:
        """
        Checks if the provided email is a known spam trap.
        
        Args:
            email (str): The email address to check.
        
        Returns:
            bool: True if it's a spam trap, False otherwise.
        """
        email_lower = email.lower()
        if email_lower in self.spam_trap_emails:
            logger.info(f"Email {email} identified as a known spam trap.")
            return True
        return False

    def add_spam_trap(self, email: str) -> bool:
        """
        Adds a new spam trap email to the list and updates the file.
        
        Args:
            email (str): The spam trap email to add.
        
        Returns:
            bool: True if added successfully, False otherwise.
        """
        email_lower = email.lower()
        if email_lower not in self.spam_trap_emails:
            self.spam_trap_emails.add(email_lower)
            try:
                with open('config/spam_traps.txt', 'a') as file:
                    file.write(f"{email_lower}\n")
                logger.info(f"Added {email} to spam trap list.")
                return True
            except Exception as e:
                logger.error(f"Failed to add {email} to spam trap list: {e}")
        else:
            logger.debug(f"Email {email} is already in the spam trap list.")
        return False