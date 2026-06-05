"""
CSV export functionality for lead data
"""
import csv
from typing import List, Dict
from datetime import datetime
from loguru import logger
import os

logger.add("logs/csv_exporter.log", level="DEBUG")


class CSVExporter:
    """Exports lead data to CSV format"""

    COLUMNS = [
        "Company",
        "Property",
        "Property Type",
        "City",
        "Country",
        "Website",
        "LinkedIn Company",
        "Decision Maker",
        "Title",
        "LinkedIn Profile",
        "Email",
        "Phone",
        "Locations",
        "Priority Score",
        "Notes"
    ]

    def __init__(self, output_dir: str = "data/exports"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def export_leads(self, leads: List[Dict], filename: str = None) -> str:
        """
        Export leads to CSV file
        
        Args:
            leads: List of lead dictionaries
            filename: Output filename (optional, auto-generated if not provided)
            
        Returns:
            Path to exported CSV file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"leads_export_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.COLUMNS)
                writer.writeheader()
                
                for lead in leads:
                    # Map lead data to CSV columns
                    row = {
                        "Company": lead.get("company_name", ""),
                        "Property": lead.get("property_name", ""),
                        "Property Type": lead.get("property_type", ""),
                        "City": lead.get("city", ""),
                        "Country": lead.get("country", ""),
                        "Website": lead.get("website", ""),
                        "LinkedIn Company": lead.get("linkedin_company", ""),
                        "Decision Maker": lead.get("decision_maker", ""),
                        "Title": lead.get("decision_maker_title", ""),
                        "LinkedIn Profile": lead.get("decision_maker_linkedin", ""),
                        "Email": lead.get("email", ""),
                        "Phone": lead.get("phone", ""),
                        "Locations": lead.get("num_locations", 1),
                        "Priority Score": lead.get("priority_score", 0),
                        "Notes": lead.get("notes", "")
                    }
                    writer.writerow(row)
            
            logger.info(f"Exported {len(leads)} leads to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error exporting to CSV: {str(e)}")
            raise

    def export_by_country(self, leads: List[Dict], output_dir: str = None) -> Dict[str, str]:
        """
        Export leads grouped by country
        
        Args:
            leads: List of lead dictionaries
            output_dir: Output directory (uses self.output_dir if not provided)
            
        Returns:
            Dictionary mapping country to export filepath
        """
        if not output_dir:
            output_dir = self.output_dir
        
        # Group leads by country
        leads_by_country = {}
        for lead in leads:
            country = lead.get("country", "Unknown")
            if country not in leads_by_country:
                leads_by_country[country] = []
            leads_by_country[country].append(lead)
        
        # Export each country
        exports = {}
        for country, country_leads in leads_by_country.items():
            filename = f"leads_{country.lower().replace(' ', '_')}.csv"
            filepath = self.export_leads(country_leads, filename)
            exports[country] = filepath
            logger.info(f"Exported {len(country_leads)} leads for {country}")
        
        return exports

    def export_by_priority(self, leads: List[Dict]) -> Dict[str, str]:
        """
        Export leads grouped by priority score
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            Dictionary mapping priority to export filepath
        """
        # Group leads by priority tier
        leads_by_priority = {
            "tier_1_priority_10": [],
            "tier_2_priority_7_9": [],
            "tier_3_priority_4_6": [],
            "tier_4_priority_1_3": []
        }
        
        for lead in leads:
            score = lead.get("priority_score", 0)
            if score == 10:
                leads_by_priority["tier_1_priority_10"].append(lead)
            elif 7 <= score <= 9:
                leads_by_priority["tier_2_priority_7_9"].append(lead)
            elif 4 <= score <= 6:
                leads_by_priority["tier_3_priority_4_6"].append(lead)
            else:
                leads_by_priority["tier_4_priority_1_3"].append(lead)
        
        # Export each priority tier
        exports = {}
        for tier, tier_leads in leads_by_priority.items():
            if tier_leads:
                filename = f"leads_{tier}.csv"
                filepath = self.export_leads(tier_leads, filename)
                exports[tier] = filepath
                logger.info(f"Exported {len(tier_leads)} leads for {tier}")
        
        return exports
