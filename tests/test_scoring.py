"""
Tests for lead scoring engine
"""
import pytest
from src.lead_scoring.scoring_engine import LeadScoringEngine, LeadData


class TestLeadScoringEngine:
    """Test cases for LeadScoringEngine"""
    
    def setup_method(self):
        """Setup for each test"""
        self.engine = LeadScoringEngine()
    
    def test_hostel_chain_scoring(self):
        """Test scoring for hostel chains (should be Tier 1)"""
        lead = LeadData(
            company_name="Mad Monkey Hostels",
            property_name="Mad Monkey Bangkok",
            property_type="Hostel Chain",
            city="Bangkok",
            country="Thailand",
            website="https://madmonkeyhostels.com",
            linkedin_company="https://linkedin.com/company/mad-monkey",
            decision_maker="John Doe",
            decision_maker_title="Founder",
            decision_maker_linkedin="https://linkedin.com/in/johndoe",
            email="john@madmonkey.com",
            phone="+66812345678",
            num_locations=5
        )
        
        result = self.engine.score_lead(lead)
        assert result.priority_score == 10
        assert "Tier 1" in result.tier
    
    def test_independent_hostel_scoring(self):
        """Test scoring for independent hostels (should be Tier 3-4)"""
        lead = LeadData(
            company_name="Once Again Hostel",
            property_name="Once Again Hostel",
            property_type="Independent Hostel",
            city="Chiang Mai",
            country="Thailand",
            website="https://onceagain.com",
            linkedin_company="",
            decision_maker="Sarah Smith",
            decision_maker_title="Manager",
            decision_maker_linkedin="",
            email="sarah@onceagain.com",
            phone="",
            num_locations=1
        )
        
        result = self.engine.score_lead(lead)
        assert result.priority_score <= 6
    
    def test_multi_location_boost(self):
        """Test that multi-location companies get scoring boost"""
        lead_single = LeadData(
            company_name="Test Hostel",
            property_name="Test",
            property_type="Boutique Hotel",
            city="Bangkok",
            country="Thailand",
            website="https://test.com",
            linkedin_company="https://linkedin.com/company/test",
            decision_maker="John",
            decision_maker_title="Manager",
            decision_maker_linkedin="",
            email="john@test.com",
            phone="",
            num_locations=1
        )
        
        lead_multi = LeadData(
            company_name="Test Hostel Multi",
            property_name="Test",
            property_type="Boutique Hotel",
            city="Bangkok",
            country="Thailand",
            website="https://test.com",
            linkedin_company="https://linkedin.com/company/test",
            decision_maker="John",
            decision_maker_title="Manager",
            decision_maker_linkedin="",
            email="john@test.com",
            phone="",
            num_locations=3
        )
        
        score_single = self.engine.score_lead(lead_single).priority_score
        score_multi = self.engine.score_lead(lead_multi).priority_score
        
        assert score_multi > score_single
    
    def test_decision_maker_title_boost(self):
        """Test that founder/owner titles get scoring boost"""
        lead_base = LeadData(
            company_name="Test",
            property_name="Test",
            property_type="Boutique Hotel",
            city="Bangkok",
            country="Thailand",
            website="https://test.com",
            linkedin_company="",
            decision_maker="John",
            decision_maker_title="Manager",
            decision_maker_linkedin="",
            email="john@test.com",
            phone="",
            num_locations=1
        )
        
        lead_founder = LeadData(
            company_name="Test Founder",
            property_name="Test",
            property_type="Boutique Hotel",
            city="Bangkok",
            country="Thailand",
            website="https://test.com",
            linkedin_company="",
            decision_maker="John",
            decision_maker_title="Founder",
            decision_maker_linkedin="",
            email="john@test.com",
            phone="",
            num_locations=1
        )
        
        score_base = self.engine.score_lead(lead_base).priority_score
        score_founder = self.engine.score_lead(lead_founder).priority_score
        
        assert score_founder >= score_base
