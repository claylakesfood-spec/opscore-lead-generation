"""
Airtable export and integration functionality
"""
from typing import List, Dict, Optional
from loguru import logger
from src.data_collection.api_handlers import AirtableAPIHandler

logger.add("logs/airtable_exporter.log", level="DEBUG")


class AirtableExporter:
    """Exports and syncs lead data to Airtable"""

    def __init__(self, api_key: Optional[str] = None, base_id: Optional[str] = None, table_name: str = "Leads"):
        self.handler = AirtableAPIHandler(api_key, base_id)
        self.table_name = table_name

    def prepare_record(self, lead: Dict) -> Dict:
        """
        Prepare lead data for Airtable format
        
        Args:
            lead: Lead dictionary
            
        Returns:
            Airtable-formatted record
        """
        return {
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
            "Notes": lead.get("notes", ""),
            "Source URL": lead.get("source_url", ""),
            "Status": "New"
        }

    def export_single_lead(self, lead: Dict) -> Optional[Dict]:
        """
        Export single lead to Airtable
        
        Args:
            lead: Lead dictionary
            
        Returns:
            Created record or None if failed
        """
        try:
            record = self.prepare_record(lead)
            result = self.handler.create_record(self.table_name, record)
            logger.info(f"Exported lead to Airtable: {lead.get('company_name')}")
            return result
        except Exception as e:
            logger.error(f"Error exporting lead to Airtable: {str(e)}")
            return None

    def export_bulk(self, leads: List[Dict], batch_size: int = 10) -> List[Dict]:
        """
        Export multiple leads to Airtable in batches
        
        Args:
            leads: List of lead dictionaries
            batch_size: Number of records per batch
            
        Returns:
            List of created records
        """
        results = []
        total = len(leads)
        
        for i in range(0, total, batch_size):
            batch = leads[i:i + batch_size]
            prepared_records = [self.prepare_record(lead) for lead in batch]
            
            try:
                batch_results = self.handler.batch_create(self.table_name, prepared_records)
                results.extend(batch_results)
                logger.info(f"Batch {i // batch_size + 1}: Exported {len(batch_results)} leads")
            except Exception as e:
                logger.error(f"Error exporting batch {i // batch_size + 1}: {str(e)}")
        
        logger.info(f"Completed Airtable export: {len(results)}/{total} leads")
        return results
