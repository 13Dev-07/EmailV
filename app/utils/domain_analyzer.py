"""
Domain Analysis Module
Coordinates various domain analysis checks and aggregates results.
"""

from typing import Dict, Optional
from app.utils.cache_manager import CacheManager
from app.utils.disposable_detector import DisposableDetector
from app.utils.domain_reputation import DomainReputation
from app.utils.typo_detector import TypoDetector

class DomainAnalyzer:
    """Coordinates domain analysis operations."""
    
    def __init__(self, cache_manager: Optional[CacheManager] = None):
        """Initialize domain analyzer with component instances."""
        self.cache_manager = cache_manager
        self.disposable_detector = DisposableDetector(cache_manager)
        self.reputation_checker = DomainReputation(cache_manager)
        self.typo_detector = TypoDetector(cache_manager)
        
    async def analyze_domain(self, domain: str) -> Dict[str, any]:
        """
        Perform comprehensive domain analysis.
        
        Args:
            domain: Domain to analyze
            
        Returns:
            Dict containing analysis results from all checks
        """
        # Check cache first
        if self.cache_manager:
            cache_key = f"domain_analysis:{domain}"
            cached_result = self.cache_manager.get(cache_key)
            if cached_result is not None:
                return cached_result
                
        result = {
            "domain": domain,
            "disposable": self.disposable_detector.check_domain(domain),
            "reputation": await self.reputation_checker.get_reputation(domain),
            "typo_analysis": self.typo_detector.check_domain(domain),
            "risk_score": 0
        }
        
        # Calculate overall risk score
        risk_score = 0
        
        # Add points for disposable characteristics
        if result["disposable"]["is_disposable"]:
            risk_score += 40
        if result["disposable"]["is_temporary"]:
            risk_score += 30
        if result["disposable"]["is_suspicious"]:
            risk_score += 20
            
        # Add points based on reputation
        if result["reputation"]["risk_level"] == "very_high":
            risk_score += 50
        elif result["reputation"]["risk_level"] == "high":
            risk_score += 30
        elif result["reputation"]["risk_level"] == "medium":
            risk_score += 15
            
        # Add points for potential typos
        if result["typo_analysis"]["has_typo"]:
            risk_score += 10
            
        result["risk_score"] = min(risk_score, 100)
        
        # Cache result
        if self.cache_manager:
            self.cache_manager.set(cache_key, result, 3600)  # 1 hour cache
            
        return result