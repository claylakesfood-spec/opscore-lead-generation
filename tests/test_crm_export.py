"""
Tests for CRM export functionality
"""
import pytest
import os
import csv
from src.crm_export.csv_exporter import CSVExporter


class TestCSVExporter:
    """Test cases for CSV export"""
    
    def setup_method(self):
        """Setup for each test"""
        self.exporter = CSVExporter()
        self.test_leads = [
            {
                "company_name": "Test Hostel",
                "property_name": "Test Hostel Bangkok",
                "property_type": "Hostel Chain",
                "city": "Bangkok",
                "country": "Thailand",
                "website": "https://test.com",
                "linkedin_company": "https://linkedin.com/company/test",
                "decision_maker": "John Doe",
                "decision_maker_title": "Founder",
                "decision_maker_linkedin": "https://linkedin.com/in/johndoe",
                "email": "john@test.com",
                "phone": "+66812345678",
                "num_locations": 5,
                "priority_score": 10,
                "notes": "High priority lead"
            }
        ]
    
    def test_export_leads(self):
        """Test exporting leads to CSV"""
        filepath = self.exporter.export_leads(self.test_leads, "test_export.csv")
        
        assert os.path.exists(filepath)
        
        # Verify CSV content
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            assert len(rows) == 1
            assert rows[0]["Company"] == "Test Hostel"
        
        # Cleanup
        os.remove(filepath)
    
    def test_export_by_country(self):
        """Test exporting leads by country"""
        leads = self.test_leads + [
            {
                "company_name": "Vietnam Hostel",
                "property_name": "Vietnam Hostel Hanoi",
                "property_type": "Hostel",
                "city": "Hanoi",
                "country": "Vietnam",
                "website": "https://vietnam.com",
                "linkedin_company": "",
                "decision_maker": "Jane Smith",
                "decision_maker_title": "Manager",
                "decision_maker_linkedin": "",
                "email": "jane@vietnam.com",
                "phone": "",
                "num_locations": 1,
                "priority_score": 5,
                "notes": ""
            }
        ]
        
        exports = self.exporter.export_by_country(leads)
        
        assert "Thailand" in exports
        assert "Vietnam" in exports
        assert os.path.exists(exports["Thailand"])
        assert os.path.exists(exports["Vietnam"])
        
        # Cleanup
        for filepath in exports.values():
            if os.path.exists(filepath):
                os.remove(filepath)
