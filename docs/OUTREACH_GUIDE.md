# Outreach Campaign Guide

## Overview

The outreach system generates personalized messages for two channels:
1. **LinkedIn** - Direct messaging (50-100 words)
2. **Email** - Formal outreach (100-150 words)

## Message Templates

### LinkedIn Templates

Five rotating templates for variety:

**Template 1 (Connection focus)**
```
Hi {name}, I noticed you manage operations at {company}. We're helping hospitality 
operators streamline inspections and maintenance tracking. Would you be open to a 
brief call to discuss your current processes?
```

**Template 2 (Growth focused)**
```
Hi {name}, Great to see {company} expanding. We help similar operators improve 
operational efficiency through AI-powered facilities management. Worth a quick 
conversation?
```

**Template 3 (Property type focus)**
```
Hi {name}, I'm reaching out because {company} stands out in the {property_type} space. 
We help reduce manual admin in facilities management. Open to a discovery call?
```

**Template 4 (Title/Role focus)**
```
Hi {name}, Noticed your background in {title}. We work with {company} and similar 
operators to streamline maintenance and inspections. Quick call this week?
```

**Template 5 (Pain point focus)**
```
Hi {name}, Your team at {company} likely spends significant time on facilities admin. 
We can help cut that in half. Interested in learning more?
```

### Email Templates

Three comprehensive email templates:

**Template 1 (Operational Review)**
```
Hi {name},

I hope this message finds you well. I came across {company} and was impressed by your 
{property_type} operations, particularly your focus on guest experience and operational 
excellence.

OpsCore is an AI Facilities Manager platform designed specifically for hospitality 
operators like yours. We help streamline inspections, maintenance tracking, asset 
management, and operational workflows—reducing manual administration and improving 
visibility across your properties.

I'd love to offer you a complimentary operational review of your current facilities 
and maintenance processes. It's a great way to identify quick wins and optimization 
opportunities without any obligation.

Would you be open to a brief 20-minute call next week?

Best regards,
OpsCore Lead Generation Team
```

**Template 2 (Feature/Benefit)**
```
Hi {name},

We work with {company} and similar hospitality operators throughout Southeast Asia.

OpsCore helps you:
• Reduce time spent on manual inspections and reporting
• Centralize maintenance requests and tracking
• Improve asset visibility and maintenance planning
• Streamline operational workflows

Would you be interested in a free operational review? I can identify 3-5 specific 
improvements for your team.

Looking forward to connecting,
OpsCore Team
```

**Template 3 (Problem/Solution)**
```
Hello {name},

Operations management in hospitality is complex. You're likely juggling inspections, 
maintenance requests, vendor management, and multiple properties—all while keeping 
costs down.

OpsCore's AI Facilities Manager simplifies this. We help {property_type} operators 
reduce admin overhead by 40% while improving maintenance oversight and asset tracking.

I'd like to invite you to a complimentary operational consultation where we review 
your current processes and suggest specific improvements tailored to {company}.

Available for a brief call this week?

Best,
OpsCore
```

## Message Generation

### Using the Message Generator

```python
from src.outreach.message_generator import MessageGenerator

generator = MessageGenerator()

# Generate both messages for a lead
lead = {
    "decision_maker": "John Doe",
    "company_name": "Mad Monkey Hostels",
    "property_type": "Hostel Chain",
    "decision_maker_title": "Founder"
}

linkedin_msg, email_msg = generator.generate_both_messages(lead)

print("LinkedIn Message:")
print(linkedin_msg)
print("\nEmail Message:")
print(email_msg)
```

### Bulk Message Generation

```python
from src.outreach.message_generator import MessageGenerator

generator = MessageGenerator()
leads = [...]  # List of lead dictionaries

messages = generator.generate_bulk_messages(leads)

# Results: {company_name: {"linkedin": "...", "email": "...", "template_used": 0}}
```

## Personalization Variables

Available variables for message customization:

| Variable | Source | Example |
|----------|--------|----------|
| `{name}` | decision_maker (first word) | "John" |
| `{company}` | company_name | "Mad Monkey Hostels" |
| `{property_type}` | property_type (lowercase) | "hostel chain" |
| `{title}` | decision_maker_title (lowercase) | "founder" |

## Outreach Strategy by Tier

### Tier 1 (Priority 10)

**LinkedIn Approach**
- Use Template 1 or 2 (connection/growth focus)
- Personalize heavily
- Emphasize scale and expertise
- Call-to-action: "Discovery call this week?"

**Email Approach**
- Use Template 1 (operational review)
- Executive tone
- Focus on ROI and efficiency
- Offer specific review
- Follow-up: 3 days, 1 week, 2 weeks

**Timing**: Send immediately (highest priority)

### Tier 2 (Priority 7-9)

**LinkedIn Approach**
- Use Template 3 or 4 (property type/title focus)
- Moderate personalization
- Emphasize specific benefits
- Call-to-action: "Quick conversation?"

**Email Approach**
- Use Template 2 (features/benefits)
- Professional tone
- List specific benefits
- Offer review or consultation
- Follow-up: 4 days, 1 week

**Timing**: Send within 1-2 days

### Tier 3 (Priority 4-6)

**LinkedIn Approach**
- Use Template 5 (pain point focus)
- Light personalization
- Focus on immediate benefits
- Call-to-action: "Open to learning more?"

**Email Approach**
- Use Template 3 (problem/solution)
- Friendly tone
- Focus on cost savings
- Offer quick consultation
- Follow-up: 1 week

**Timing**: Send within 3-5 days

### Tier 4 (Priority 1-3)

**LinkedIn Approach**
- Use generic template
- Minimal personalization
- Focus on general value
- Call-to-action: "Interested?"

**Email Approach**
- Use standard template
- Formal tone
- General benefits
- Follow-up: 2 weeks

**Timing**: Send within 1-2 weeks

## Campaign Workflows

### LinkedIn Campaign

1. **Connection Request**
   - Day 0: Send connection request with brief message
   - Message: "Hi {name}, I'd like to connect and share how OpsCore helps companies like {company}."

2. **Initial Message**
   - Day 1-3: Send main outreach message (use templates)
   - Include specific company reference
   - Clear call-to-action

3. **Follow-up**
   - Day 7: Check if viewed/liked
   - Day 14: Send reminder message if no response
   - Day 21: Final attempt or mark as "no response"

### Email Campaign

1. **Initial Email**
   - Day 0: Send personalized email
   - Subject: "Operational Review for {company}" or "OpsCore - Quick Question"
   - Include all personalization

2. **Follow-up #1**
   - Day 3: "Just checking in..."
   - Shorter message
   - Reference initial email

3. **Follow-up #2**
   - Day 7: Different angle
   - New value proposition
   - Different template/message

4. **Final Follow-up**
   - Day 14: Last attempt
   - "Wanted to make sure you got this..."
   - Include link to calendar

## Subject Lines

### Email Subject Lines

For different tiers:

**Tier 1**
- "Quick question about {company}'s operations"
- "Operational insights for {company}"
- "{name}, let's discuss your facilities management"

**Tier 2**
- "Free operational review for {company}?"
- "Help reduce admin at {company}"
- "Operations efficiency for {property_type}"

**Tier 3**
- "Cost savings opportunity for {company}"
- "Simplify your facilities management"
- "Quick suggestion for {company}"

**Tier 4**
- "Would {company} benefit from this?"
- "Operations software for hostels"
- "Facilities management made simple"

## Response Tracking

### Status Flow

```
Not Contacted
    ↓
Message Sent
    ↓
├─ Viewed/Opened
├─ Replied (Interested/Not Interested)
├─ No Response (after final follow-up)
│
└─→ Interested
    ├─ Meeting Scheduled
    │  └─→ Opportunity Created
    └─ Not Interested (moved to inactive)
```

### Tracking Implementation

```python
from database.models import ContactHistory
from datetime import datetime

# Log outreach
contact = ContactHistory(
    company_id=company_id,
    contact_type="email",
    status="contacted",
    response="Opened email - no reply yet",
    created_at=datetime.now()
)
session.add(contact)
session.commit()
```

## Best Practices

### Do's ✅

1. **Personalize every message** - Use company/person-specific details
2. **Be concise** - Respect their time
3. **Offer value** - Lead with benefits, not features
4. **Clear CTA** - Make next step obvious
5. **Follow up** - 3-4 touches in sequence
6. **Time appropriately** - Business hours, weekdays
7. **Segment campaigns** - Different approach per tier
8. **Track responses** - Monitor open rates, replies
9. **A/B test** - Test templates and timing
10. **Respect opt-outs** - Honor unsubscribe requests

### Don'ts ❌

1. ❌ Generic copy-paste messages
2. ❌ Overly long emails
3. ❌ Multiple CTAs (confuses recipient)
4. ❌ Spammy language ("Act now!", "Limited time")
5. ❌ Misleading subject lines
6. ❌ No clear value proposition
7. ❌ Aggressive follow-ups
8. ❌ Wrong contact person
9. ❌ Typos or grammatical errors
10. ❌ No unsubscribe option

## Metrics to Track

1. **Delivery Rate** - % of messages sent successfully
2. **Open Rate** - % of emails opened (email only)
3. **Reply Rate** - % of recipients who replied
4. **Click Rate** - % who clicked links (email only)
5. **Meeting Rate** - % who scheduled meetings
6. **Conversion Rate** - % who became opportunities/customers
7. **Response Time** - Average time to first response
8. **Message Effectiveness** - Template performance

## Example Campaign Results

```
Initial List: 100 leads
Tier 1 (10 leads):
  - Sent: 10
  - Opened: 9 (90%)
  - Replied: 4 (40%)
  - Interested: 3 (30%)
  - Meetings: 2 (20%)

Tier 2 (25 leads):
  - Sent: 25
  - Opened: 18 (72%)
  - Replied: 5 (20%)
  - Interested: 3 (12%)
  - Meetings: 1 (4%)

Tier 3 (35 leads):
  - Sent: 35
  - Opened: 15 (43%)
  - Replied: 2 (6%)
  - Interested: 1 (3%)
  - Meetings: 0 (0%)

Tier 4 (30 leads):
  - Sent: 30
  - Opened: 6 (20%)
  - Replied: 0 (0%)
  - Interested: 0 (0%)
  - Meetings: 0 (0%)

TOTAL RESULTS:
- Overall open rate: 48%
- Overall reply rate: 11%
- Total meetings: 3
- Conversion rate: 3% → Opportunity
```

---

**Last Updated**: June 5, 2026
**Version**: 1.0.0
