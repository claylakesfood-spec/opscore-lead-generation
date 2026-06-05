"""
Lead scoring engine for prioritizing qualified leads
"""
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum
from loguru import logger

logger.add("logs/scoring_engine.log", level="DEBUG")


class PropertyType(Enum):
    """Enumeration of property types"""
    HOSTEL_CHAIN = "Hostel Chain"
    INDEPENDENT_HOSTEL = "Independent Hostel"
    BOUTIQUE_HOTEL = "Boutique Hotel"
    HOTEL_GROUP = "Hotel Group"
    SERVICED_APARTMENTS = "Serviced Apartments"
    COWORKING = "Coworking Space"
    EVENT_VENUE = "Event Venue"
    PMC = "Property Management Company"
    FMC = "Facilities Management Company"
    STUDENT_ACCOMMODATION = "Student Accommodation"
    COMMERCIAL_PROPERTY = "Commercial Property"


@dataclass
class LeadData:
    """Data class for lead information"""
    company_name: str
    property_name: str
    property_type: str
    city: str
    country: str
    website: str
    linkedin_company: str
    decision_maker: str
    decision_maker_title: str
    decision_maker_linkedin: str
    email: str
    phone: str
    num_locations: int = 1
    source_url: str = ""
    notes: str = ""


@dataclass
class ScoringResult:
    """Result of lead scoring"""
    company_name: str
    priority_score: int
    reasoning: Dict[str, any]
    tier: str


class LeadScoringEngine:
    """Scoring engine for evaluating and prioritizing leads"""

    # Scoring factors
    BASE_SCORE = 0
    LOCATION_MULTIPLIER = 1.5  # Multi-location operators score higher
    PROPERTY_TYPE_SCORES = {
        "Hostel Chain": 10,
        "Hotel Group": 10,
        "Coworking Space": 8,
        "Serviced Apartments": 8,
        "Boutique Hotel": 7,
        "Facilities Management Company": 7,
        "Property Management Company": 7,
        "Student Accommodation": 6,
        "Event Venue": 6,
        "Commercial Property": 5,
        "Independent Hostel": 4,
    }
    
    TITLE_BOOST = {
        "Founder": 2,
        "Owner": 2,
        "Managing Director": 2,
        "Operations Director": 1.5,
        "General Manager": 1.5,
        "Operations Manager": 1,
        "Facilities Manager": 1,
        "Property Manager": 1,
        "Engineering Manager": 1,
        "Asset Manager": 1,
    }

    def __init__(self):
        self.logger = logger

    def score_lead(self, lead: LeadData) -> ScoringResult:
        """
        Score a lead and return priority ranking
        
        Args:
            lead: LeadData object with company and decision-maker info
            
        Returns:
            ScoringResult with priority score and reasoning
        """
        self.logger.info(f"Scoring lead: {lead.company_name}")
        
        reasoning = {}
        score = self.BASE_SCORE
        
        # 1. Property Type Score
        property_score = self.PROPERTY_TYPE_SCORES.get(lead.property_type, 3)
        score += property_score
        reasoning['property_type'] = {
            'value': lead.property_type,
            'score': property_score
        }
        
        # 2. Multi-location boost
        if lead.num_locations >= 5:
            location_bonus = 3
            score += location_bonus
            reasoning['multi_location'] = {
                'locations': lead.num_locations,
                'bonus': location_bonus,
                'tier': 'Tier 1 (5+ locations)'
            }
        elif lead.num_locations >= 2:
            location_bonus = 1.5
            score += location_bonus
            reasoning['multi_location'] = {
                'locations': lead.num_locations,
                'bonus': location_bonus,
                'tier': 'Tier 2 (2-4 locations)'
            }
        else:
            reasoning['multi_location'] = {
                'locations': lead.num_locations,
                'bonus': 0,
                'tier': 'Single location'
            }
        
        # 3. Decision Maker Title Boost
        title_boost = self._calculate_title_boost(lead.decision_maker_title)
        score += title_boost
        reasoning['decision_maker_title'] = {
            'title': lead.decision_maker_title,
            'boost': title_boost
        }
        
        # 4. Complete Information Bonus
        info_score = self._calculate_information_completeness(lead)
        score += info_score
        reasoning['information_completeness'] = {
            'score': info_score,
            'has_email': bool(lead.email),
            'has_phone': bool(lead.phone),
            'has_linkedin': bool(lead.decision_maker_linkedin)
        }
        
        # Normalize and cap score at 10
        final_score = min(int(round(score)), 10)
        final_score = max(final_score, 1)
        
        # Determine tier
        tier = self._determine_tier(final_score)
        
        self.logger.info(
            f"Lead {lead.company_name} scored {final_score}/10 (Tier: {tier})"
        )
        
        return ScoringResult(
            company_name=lead.company_name,
            priority_score=final_score,
            reasoning=reasoning,
            tier=tier
        )

    def _calculate_title_boost(self, title: str) -> float:
        """Calculate boost based on decision-maker title"""
        for key, boost in self.TITLE_BOOST.items():
            if key.lower() in title.lower():
                return boost
        return 0

    def _calculate_information_completeness(self, lead: LeadData) -> float:
        """Bonus points for complete information"""
        bonus = 0
        if lead.email and self._is_valid_email(lead.email):
            bonus += 0.5
        if lead.phone and self._is_valid_phone(lead.phone):
            bonus += 0.5
        if lead.decision_maker_linkedin:
            bonus += 0.5
        if lead.website:
            bonus += 0.5
        return min(bonus, 2)  # Cap at 2 points

    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _is_valid_phone(self, phone: str) -> bool:
        """Validate phone format"""
        import re
        pattern = r'^\+?[\d\s\-\(\)]{7,}$'
        return bool(re.match(pattern, phone))

    def _determine_tier(self, score: int) -> str:
        """Determine lead tier based on score"""
        if score == 10:
            return "PRIORITY_1_TIER_1 (10) - Multi-property operators"
        elif 7 <= score <= 9:
            return "PRIORITY_2_TIER_2 (7-9) - Boutique/Coworking operators"
        elif 4 <= score <= 6:
            return "PRIORITY_3_TIER_3 (4-6) - Independent operators"
        else:
            return "PRIORITY_4_TIER_4 (1-3) - Single-location operators"

    def bulk_score_leads(self, leads: List[LeadData]) -> List[ScoringResult]:
        """
        Score multiple leads
        
        Args:
            leads: List of LeadData objects
            
        Returns:
            List of ScoringResult objects
        """
        self.logger.info(f"Scoring {len(leads)} leads...")
        results = [self.score_lead(lead) for lead in leads]
        
        # Sort by score descending
        results.sort(key=lambda x: x.priority_score, reverse=True)
        
        self.logger.info(f"Completed scoring {len(leads)} leads")
        return results

    def get_score_distribution(self, results: List[ScoringResult]) -> Dict:
        """
        Get distribution of scores
        
        Args:
            results: List of ScoringResult objects
            
        Returns:
            Dictionary with score distribution
        """
        distribution = {
            "tier_1": 0,
            "tier_2": 0,
            "tier_3": 0,
            "tier_4": 0,
            "total": len(results)
        }
        
        for result in results:
            if result.priority_score == 10:
                distribution["tier_1"] += 1
            elif 7 <= result.priority_score <= 9:
                distribution["tier_2"] += 1
            elif 4 <= result.priority_score <= 6:
                distribution["tier_3"] += 1
            else:
                distribution["tier_4"] += 1
        
        return distribution
