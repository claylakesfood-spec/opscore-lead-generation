"""
Personalized message generator for outreach
"""
from typing import Dict, Tuple
from loguru import logger
from src.outreach.templates import get_linkedin_template, get_email_template

logger.add("logs/message_generator.log", level="DEBUG")


class MessageGenerator:
    """Generates personalized outreach messages"""

    def __init__(self):
        self.logger = logger

    def generate_linkedin_message(self, lead: Dict, template_index: int = 0) -> str:
        """
        Generate personalized LinkedIn message
        
        Args:
            lead: Lead dictionary with company and contact info
            template_index: Which template to use
            
        Returns:
            Personalized message (50-100 words)
        """
        try:
            template = get_linkedin_template(template_index)
            
            message = template.format(
                name=lead.get("decision_maker", "there").split()[0],
                company=lead.get("company_name", "your company"),
                property_type=lead.get("property_type", "hospitality").lower(),
                title=lead.get("decision_maker_title", "operations").lower()
            )
            
            # Verify word count (50-100 words)
            word_count = len(message.split())
            if word_count < 50 or word_count > 100:
                self.logger.warning(f"LinkedIn message word count: {word_count} (target 50-100)")
            
            self.logger.info(f"Generated LinkedIn message for {lead.get('company_name')}")
            return message
            
        except Exception as e:
            self.logger.error(f"Error generating LinkedIn message: {str(e)}")
            return "Hi, I'd like to discuss how we can help streamline your operations."

    def generate_email_message(self, lead: Dict, template_index: int = 0) -> str:
        """
        Generate personalized email message
        
        Args:
            lead: Lead dictionary with company and contact info
            template_index: Which template to use
            
        Returns:
            Personalized message (100-150 words)
        """
        try:
            template = get_email_template(template_index)
            
            message = template.format(
                name=lead.get("decision_maker", "there").split()[0],
                company=lead.get("company_name", "your company"),
                property_type=lead.get("property_type", "hospitality"),
                title=lead.get("decision_maker_title", "operations")
            )
            
            # Verify word count (100-150 words)
            word_count = len(message.split())
            if word_count < 100 or word_count > 150:
                self.logger.warning(f"Email message word count: {word_count} (target 100-150)")
            
            self.logger.info(f"Generated email message for {lead.get('company_name')}")
            return message
            
        except Exception as e:
            self.logger.error(f"Error generating email message: {str(e)}")
            return "We help hospitality operators streamline operations. Would you be interested in learning more?"

    def generate_both_messages(self, lead: Dict) -> Tuple[str, str]:
        """
        Generate both LinkedIn and email messages
        
        Args:
            lead: Lead dictionary
            
        Returns:
            Tuple of (linkedin_message, email_message)
        """
        linkedin_msg = self.generate_linkedin_message(lead)
        email_msg = self.generate_email_message(lead)
        return linkedin_msg, email_msg

    def generate_bulk_messages(self, leads: list) -> Dict:
        """
        Generate messages for multiple leads
        
        Args:
            leads: List of lead dictionaries
            
        Returns:
            Dictionary with generated messages
        """
        results = {}
        
        for i, lead in enumerate(leads):
            template_index = i % 3  # Rotate through templates
            linkedin_msg, email_msg = self.generate_both_messages(lead)
            
            results[lead.get("company_name")] = {
                "linkedin": linkedin_msg,
                "email": email_msg,
                "template_used": template_index
            }
        
        self.logger.info(f"Generated messages for {len(leads)} leads")
        return results
