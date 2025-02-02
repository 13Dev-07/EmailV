"""
Validation Orchestrator Module
Coordinates various email validation processes and batch operations.
"""

from app.utils.syntax_validator import validate_syntax
from app.utils.dns_resolver import DNSResolver
from app.utils.cache_manager import CacheManager
from app.utils.smtp_verifier import verify_smtp
from app.utils.disposable_email_detector import is_disposable_email
from app.utils.role_account_detector import is_role_account
from app.utils.typo_detector import detect_typo
from app.utils.domain_reputation import get_domain_reputation
from app.utils.spam_trap_detector import SpamTrapDetector
from app.utils.catch_all_detector import CatchAllDetector
from app.utils.exceptions import ValidationError
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
import asyncio

# Initialize components
spam_trap_detector = SpamTrapDetector()
catch_all_detector = CatchAllDetector()
cache_manager = CacheManager()
dns_resolver = DNSResolver(cache_manager=cache_manager)

def validate_email(email: str) -> dict:
    """
    Validates the provided email through multiple validation steps.
    
    Args:
        email (str): The email address to validate.
    
    Returns:
        dict: Validation results and risk score.
    
    Raises:
        ValidationError: If validation fails.
    """
    result = {
        "email": email,
        "syntax_valid": validate_syntax(email).syntax_valid,
        "domain_exists": False,
        "has_ipv4": False,
        "has_ipv6": False,
        "has_ns": False,
        "has_ptr": False,
        "ptr_record": None,
        "mx_records_valid": False,
        "smtp_verified": False,
        "disposable": False,
        "role_account": False,
        "typo_detected": False,
        "typo_suggestion": None,
        "domain_reputation": 0,
        "spam_trap": False,
        "catch_all": False,
        "risk_score": 0,
        "status": "Invalid"
    }
    
    domain = extract_domain(email)
    if not domain:
        raise ValidationError("Invalid email format: Missing domain.")
    
    # Syntax Validation
    if not validate_syntax(email):
        raise ValidationError("Invalid email syntax.")
    result["syntax_valid"] = True
    
    # Comprehensive Domain Resolution
    dns_results = dns_resolver.resolve_domain(domain)
    result["domain_exists"] = dns_results["any_record"]
    if not result["domain_exists"]:
        raise ValidationError("Domain does not exist.")
    
    # Additional DNS checks
    result["has_ipv4"] = dns_results["a_record"]
    result["has_ipv6"] = dns_results["aaaa_record"]
    result["has_ns"] = dns_results["ns_record"]
    
    # MX Records Verification
    mx_records = dns_resolver.get_mx_records(domain)
    result["mx_records_valid"] = len(mx_records) > 0
    if not result["mx_records_valid"]:
        raise ValidationError("No valid MX records found for domain.")
    
    # PTR Record Check
    ptr_record = dns_resolver.verify_ptr_record(domain)
    result["has_ptr"] = ptr_record is not None
    result["ptr_record"] = ptr_record
    
    # SMTP Verification
    if verify_smtp(email):
        result["smtp_verified"] = True
    else:
        result["smtp_verified"] = False
    
    # Disposable Email Detection
    result["disposable"] = is_disposable_email(email)
    
    # Role Account Detection
    result["role_account"] = is_role_account(email)
    
    # Typo Detection
    typo_suggestion = detect_typo(email)
    if typo_suggestion:
        result["typo_detected"] = True
        result["typo_suggestion"] = typo_suggestion
    
    # Domain Reputation
    result["domain_reputation"] = get_domain_reputation(domain)
    
    # Spam Trap Detection
    result["spam_trap"] = spam_trap_detector.is_spam_trap(email)
    
    # Catch-All Detection
    result["catch_all"] = catch_all_detector.is_catch_all(domain)
    
    # Risk Scoring
    result["risk_score"] = calculate_risk_score(result)
    
    # Final Status
    result["status"] = "Valid" if result["risk_score"] < 50 else "Risky"
    
    return result

async def validate_emails_batch(emails: List[str], batch_size: int = 50) -> List[Dict]:
    """
    Validates multiple email addresses in parallel batches.
    
    Args:
        emails (List[str]): List of email addresses to validate.
        batch_size (int): Size of each batch for parallel processing.
    
    Returns:
        List[Dict]: List of validation results for each email.
    """
    results = []
    
    def process_email(email: str) -> Dict:
        try:
            return validate_email(email)
        except ValidationError as e:
            return {
                "email": email,
                "status": "Invalid",
                "error": str(e)
            }
        except Exception as e:
            return {
                "email": email,
                "status": "Error",
                "error": f"Unexpected error: {str(e)}"
            }
    
    # Process emails in batches using a thread pool
    with ThreadPoolExecutor(max_workers=min(batch_size, 20)) as executor:
        for i in range(0, len(emails), batch_size):
            batch = emails[i:i + batch_size]
            batch_results = list(executor.map(process_email, batch))
            results.extend(batch_results)
            
            # Small delay between batches to prevent rate limiting
            if i + batch_size < len(emails):
                await asyncio.sleep(0.1)
    
    return results

def extract_domain(email: str) -> str:
    """
    Extracts the domain part from the email address.
    
    Args:
        email (str): The email address.
    
    Returns:
        str: The domain if extraction is successful, else an empty string.
    """
    try:
        return email.split('@')[1].lower()
    except IndexError:
        return ""

def calculate_risk_score(validation_result: Dict) -> int:
    """
    Calculates a risk score based on various validation factors.
    
    Args:
        validation_result (dict): Results from validation steps.
    
    Returns:
        int: Calculated risk score between 0-100.
    """
    score = 0
    
    # Core validations (heavily weighted)
    if not validation_result["syntax_valid"]:
        score += 40
    if not validation_result["domain_exists"]:
        score += 40
    if not validation_result["mx_records_valid"]:
        score += 30
    if not validation_result["smtp_verified"]:
        score += 20
        
    # Additional security checks
    if not validation_result["has_ptr"]:
        score += 10
    if validation_result["disposable"]:
        score += 15
    if validation_result["role_account"]:
        score += 5
    if validation_result["spam_trap"]:
        score += 40
    if validation_result["catch_all"]:
        score += 10
        
    # Domain reputation factor (0-100 scale, inversely proportional)
    reputation_factor = (100 - validation_result["domain_reputation"]) * 0.2
    score += reputation_factor
    
    # Cap the score at 100
    return min(100, score)