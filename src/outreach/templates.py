"""
Outreach message templates for LinkedIn and Email
"""

LINKEDIN_TEMPLATES = [
    "Hi {name}, I noticed you manage operations at {company}. We're helping hospitality operators streamline inspections and maintenance tracking. Would you be open to a brief call to discuss your current processes?",
    "Hi {name}, Great to see {company} expanding. We help similar operators improve operational efficiency through AI-powered facilities management. Worth a quick conversation?",
    "Hi {name}, I'm reaching out because {company} stands out in the {property_type} space. We help reduce manual admin in facilities management. Open to a discovery call?",
    "Hi {name}, Noticed your background in {title}. We work with {company} and similar operators to streamline maintenance and inspections. Quick call this week?",
    "Hi {name}, Your team at {company} likely spends significant time on facilities admin. We can help cut that in half. Interested in learning more?"
]

EMAIL_TEMPLATES = [
    """Hi {name},

I hope this message finds you well. I came across {company} and was impressed by your {property_type} operations, particularly your focus on guest experience and operational excellence.

OpsCore is an AI Facilities Manager platform designed specifically for hospitality operators like yours. We help streamline inspections, maintenance tracking, asset management, and operational workflows—reducing manual administration and improving visibility across your properties.

I'd love to offer you a complimentary operational review of your current facilities and maintenance processes. It's a great way to identify quick wins and optimization opportunities without any obligation.

Would you be open to a brief 20-minute call next week?

Best regards,
OpsCore Lead Generation Team""",
    
    """Hi {name},

We work with {company} and similar hospitality operators throughout Southeast Asia.

OpsCore helps you:
• Reduce time spent on manual inspections and reporting
• Centralize maintenance requests and tracking
• Improve asset visibility and maintenance planning
• Streamline operational workflows

Would you be interested in a free operational review? I can identify 3-5 specific improvements for your team.

Looking forward to connecting,
OpsCore Team""",
    
    """Hello {name},

Operations management in hospitality is complex. You're likely juggling inspections, maintenance requests, vendor management, and multiple properties—all while keeping costs down.

OpsCore's AI Facilities Manager simplifies this. We help {property_type} operators reduce admin overhead by 40% while improving maintenance oversight and asset tracking.

I'd like to invite you to a complimentary operational consultation where we review your current processes and suggest specific improvements tailored to {company}.

Available for a brief call this week?

Best,
OpsCore"""
]

def get_linkedin_template(index: int = 0) -> str:
    """Get LinkedIn message template by index"""
    return LINKEDIN_TEMPLATES[index % len(LINKEDIN_TEMPLATES)]

def get_email_template(index: int = 0) -> str:
    """Get email template by index"""
    return EMAIL_TEMPLATES[index % len(EMAIL_TEMPLATES)]
