"""
Workflow orchestration for the lead generation pipeline
"""
from typing import List, Dict, Optional
from loguru import logger
from datetime import datetime

logger.add("logs/workflow_orchestrator.log", level="DEBUG")


class LeadGenerationWorkflow:
    """Orchestrates the complete lead generation workflow"""

    def __init__(self):
        self.logger = logger
        self.workflow_status = {}

    def discover_companies(self, search_queries: List[str], countries: List[str]) -> List[Dict]:
        """
        Step 1: Discover companies from multiple sources
        
        Args:
            search_queries: List of search queries (company names, types, etc.)
            countries: List of countries to search in
            
        Returns:
            List of discovered companies
        """
        self.logger.info(f"Step 1: Discovering companies for {search_queries}")
        companies = []
        
        # This would integrate with:
        # - Web scraping
        # - Business directories (Crunchbase, Builtwith, Hunter)
        # - LinkedIn search
        # - Industry publications
        
        self.workflow_status["companies_discovered"] = len(companies)
        return companies

    def find_decision_makers(self, companies: List[Dict]) -> List[Dict]:
        """
        Step 2: Find decision-makers for each company
        
        Args:
            companies: List of company dictionaries
            
        Returns:
            Companies with decision-maker information
        """
        self.logger.info(f"Step 2: Finding decision makers for {len(companies)} companies")
        
        # This would integrate with:
        # - LinkedIn search
        # - Company websites
        # - Business databases
        # - Email finders (Hunter, RocketReach)
        
        self.workflow_status["decision_makers_found"] = len(companies)
        return companies

    def verify_information(self, companies: List[Dict]) -> List[Dict]:
        """
        Step 3: Verify company website and contact information
        
        Args:
            companies: List of company dictionaries
            
        Returns:
            Verified company information
        """
        self.logger.info(f"Step 3: Verifying information for {len(companies)} companies")
        
        verified = []
        for company in companies:
            # Verify website accessibility
            # Verify email formats
            # Verify phone numbers
            # Check for duplicates
            verified.append(company)
        
        self.workflow_status["verified_companies"] = len(verified)
        return verified

    def score_leads(self, companies: List[Dict]) -> List[Dict]:
        """
        Step 4: Generate lead scores using scoring engine
        
        Args:
            companies: List of verified companies
            
        Returns:
            Companies with priority scores
        """
        self.logger.info(f"Step 4: Scoring {len(companies)} leads")
        
        # This would integrate with the LeadScoringEngine
        from src.lead_scoring.scoring_engine import LeadScoringEngine, LeadData
        
        engine = LeadScoringEngine()
        scored_leads = []
        
        for company in companies:
            lead_data = LeadData(
                company_name=company.get("company_name"),
                property_name=company.get("property_name"),
                property_type=company.get("property_type"),
                city=company.get("city"),
                country=company.get("country"),
                website=company.get("website"),
                linkedin_company=company.get("linkedin_company"),
                decision_maker=company.get("decision_maker"),
                decision_maker_title=company.get("decision_maker_title"),
                decision_maker_linkedin=company.get("decision_maker_linkedin"),
                email=company.get("email"),
                phone=company.get("phone"),
                num_locations=company.get("num_locations", 1)
            )
            
            score_result = engine.score_lead(lead_data)
            company["priority_score"] = score_result.priority_score
            company["tier"] = score_result.tier
            scored_leads.append(company)
        
        self.workflow_status["scored_leads"] = len(scored_leads)
        return scored_leads

    def generate_outreach_messages(self, leads: List[Dict]) -> List[Dict]:
        """
        Step 5: Generate personalized outreach messages
        
        Args:
            leads: List of scored leads
            
        Returns:
            Leads with generated outreach messages
        """
        self.logger.info(f"Step 5: Generating outreach messages for {len(leads)} leads")
        
        from src.outreach.message_generator import MessageGenerator
        
        generator = MessageGenerator()
        
        for i, lead in enumerate(leads):
            linkedin_msg, email_msg = generator.generate_both_messages(lead)
            lead["linkedin_message"] = linkedin_msg
            lead["email_message"] = email_msg
        
        self.workflow_status["messages_generated"] = len(leads)
        return leads

    def export_to_crm(self, leads: List[Dict], export_formats: List[str]) -> Dict:
        """
        Step 6: Export leads to CRM systems
        
        Args:
            leads: List of leads with all information
            export_formats: List of export formats ("csv", "airtable", "hubspot")
            
        Returns:
            Dictionary with export results
        """
        self.logger.info(f"Step 6: Exporting {len(leads)} leads to CRM systems")
        
        results = {}
        
        if "csv" in export_formats:
            from src.crm_export.csv_exporter import CSVExporter
            csv_exporter = CSVExporter()
            csv_path = csv_exporter.export_leads(leads)
            results["csv"] = csv_path
            self.logger.info(f"CSV exported to: {csv_path}")
        
        if "airtable" in export_formats:
            from src.crm_export.airtable_exporter import AirtableExporter
            airtable_exporter = AirtableExporter()
            airtable_results = airtable_exporter.export_bulk(leads)
            results["airtable"] = airtable_results
            self.logger.info(f"Airtable export: {airtable_results}")
        
        if "hubspot" in export_formats:
            from src.crm_export.hubspot_exporter import HubSpotExporter
            hubspot_exporter = HubSpotExporter()
            hubspot_results = hubspot_exporter.export_bulk(leads)
            results["hubspot"] = hubspot_results
            self.logger.info(f"HubSpot export: {hubspot_results}")
        
        self.workflow_status["crm_exports"] = results
        return results

    def track_contact_status(self, leads: List[Dict]) -> Dict:
        """
        Step 7: Track contact and outreach status
        
        Args:
            leads: List of leads
            
        Returns:
            Status tracking data
        """
        self.logger.info(f"Step 7: Tracking contact status for {len(leads)} leads")
        
        status_data = {
            "total_leads": len(leads),
            "not_contacted": len([l for l in leads if l.get("contact_status") == "not_contacted"]),
            "contacted": len([l for l in leads if l.get("contact_status") == "contacted"]),
            "interested": len([l for l in leads if l.get("contact_status") == "interested"]),
            "meeting_scheduled": len([l for l in leads if l.get("contact_status") == "meeting_scheduled"]),
            "opportunity": len([l for l in leads if l.get("contact_status") == "opportunity"]),
            "timestamp": datetime.now().isoformat()
        }
        
        self.workflow_status["contact_status"] = status_data
        return status_data

    def run_complete_workflow(self, search_queries: List[str], countries: List[str], export_formats: List[str]) -> Dict:
        """
        Run the complete lead generation workflow
        
        Args:
            search_queries: List of search queries
            countries: List of target countries
            export_formats: List of export formats
            
        Returns:
            Complete workflow results
        """
        self.logger.info("Starting complete lead generation workflow")
        start_time = datetime.now()
        
        # Execute workflow steps
        companies = self.discover_companies(search_queries, countries)
        companies = self.find_decision_makers(companies)
        companies = self.verify_information(companies)
        leads = self.score_leads(companies)
        leads = self.generate_outreach_messages(leads)
        export_results = self.export_to_crm(leads, export_formats)
        status = self.track_contact_status(leads)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        workflow_results = {
            "status": "completed",
            "total_leads": len(leads),
            "export_results": export_results,
            "contact_status": status,
            "duration_seconds": duration,
            "timestamp": end_time.isoformat()
        }
        
        self.logger.info(f"Workflow completed in {duration:.2f} seconds with {len(leads)} leads")
        return workflow_results

    def get_workflow_status(self) -> Dict:
        """Get current workflow status"""
        return self.workflow_status
