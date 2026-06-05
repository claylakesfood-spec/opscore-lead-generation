"""
HubSpot export and integration functionality
"""
from typing import List, Dict, Optional
from loguru import logger
from src.data_collection.api_handlers import HubSpotAPIHandler

logger.add("logs/hubspot_exporter.log", level="DEBUG")


class HubSpotExporter:
    """Exports and syncs lead data to HubSpot"""

    def __init__(self, api_key: Optional[str] = None):
        self.handler = HubSpotAPIHandler(api_key)

    def prepare_company(self, lead: Dict) -> Dict:
        """
        Prepare company data for HubSpot
        
        Args:
            lead: Lead dictionary
            
        Returns:
            HubSpot-formatted company properties
        """
        return {
            "name": lead.get("company_name", ""),
            "website": lead.get("website", ""),
            "notes": lead.get("notes", ""),
            "country": lead.get("country", ""),
            "city": lead.get("city", ""),
            "custom_property_type": lead.get("property_type", ""),
            "custom_locations": lead.get("num_locations", 1),
            "custom_priority_score": lead.get("priority_score", 0),
            "custom_linkedin_company": lead.get("linkedin_company", ""),
        }

    def prepare_contact(self, lead: Dict) -> Dict:
        """
        Prepare contact data for HubSpot
        
        Args:
            lead: Lead dictionary
            
        Returns:
            HubSpot-formatted contact properties
        """
        return {
            "firstname": lead.get("decision_maker", "").split()[0] if lead.get("decision_maker") else "",
            "lastname": " ".join(lead.get("decision_maker", "").split()[1:]) if lead.get("decision_maker") else "",
            "jobtitle": lead.get("decision_maker_title", ""),
            "email": lead.get("email", ""),
            "phone": lead.get("phone", ""),
            "linkedin_url": lead.get("decision_maker_linkedin", ""),
            "notes": f"Lead from {lead.get('source_url', '')}. Priority: {lead.get('priority_score', 0)}/10"
        }

    def export_lead(self, lead: Dict) -> bool:
        """
        Export lead as company and contact to HubSpot
        
        Args:
            lead: Lead dictionary
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create company
            company_data = self.prepare_company(lead)
            company_result = self.handler.create_company(company_data)
            
            if not company_result:
                logger.warning(f"Failed to create company: {lead.get('company_name')}")
                return False
            
            # Create contact
            contact_data = self.prepare_contact(lead)
            contact_result = self.handler.create_contact(contact_data)
            
            if contact_result:
                logger.info(f"Exported lead to HubSpot: {lead.get('company_name')}")
                return True
            else:
                logger.warning(f"Failed to create contact for: {lead.get('company_name')}")
                return False
                
        except Exception as e:
            logger.error(f"Error exporting lead to HubSpot: {str(e)}")
            return False

    def export_bulk(self, leads: List[Dict]) -> Dict[str, int]:
        """
        Export multiple leads to HubSpot
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            Dictionary with success/failure counts
        """
        results = {
            "successful": 0,
            "failed": 0,
            "total": len(leads)
        }
        
        try:
            companies = [self.prepare_company(lead) for lead in leads]
            company_results = self.handler.batch_create_companies(companies)
            results["successful"] = len(company_results)
            results["failed"] = len(leads) - len(company_results)
            
            logger.info(f"HubSpot export complete: {results['successful']}/{results['total']} companies created")
            
        except Exception as e:
            logger.error(f"Error in bulk HubSpot export: {str(e)}")
            results["failed"] = len(leads)
        
        return results
