# CRM Integration Guide

## Overview

The OpsCore Lead Generation Engine supports integration with three major CRM platforms:

1. **CSV Export** - Universal format
2. **Airtable** - Collaborative database
3. **HubSpot** - Full-featured CRM

## CSV Export

### Usage

```python
from src.crm_export.csv_exporter import CSVExporter

exporter = CSVExporter(output_dir="data/exports")

# Export all leads
filepath = exporter.export_leads(leads_list, filename="leads_export.csv")

# Export by country
country_exports = exporter.export_by_country(leads_list)

# Export by priority
priority_exports = exporter.export_by_priority(leads_list)
```

### CSV Format

Columns in exported CSV:

```
Company,Property,Property Type,City,Country,Website,LinkedIn Company,
Decision Maker,Title,LinkedIn Profile,Email,Phone,Locations,Priority Score,Notes
```

### Example Data

```csv
Mad Monkey Hostels,Mad Monkey Bangkok,Hostel Chain,Bangkok,Thailand,https://madmonkey.com,
https://linkedin.com/company/mad-monkey,John Doe,Founder,https://linkedin.com/in/johndoe,
john@madmonkey.com,+66812345678,5,10,Multi-location operator
```

## Airtable Integration

### Setup

1. **Create Airtable Base**:
   - Sign up at https://airtable.com
   - Create new base called "OpsCore Leads"
   - Create table "Leads"

2. **Create Fields**:
   - Company (Text) - Single line
   - Property (Text) - Single line
   - Property Type (Select) - Options: Hostel Chain, Hotel Group, etc.
   - City (Text) - Single line
   - Country (Select) - Thailand, Vietnam, Bali, Cambodia, Philippines
   - Website (URL) - URL field
   - LinkedIn Company (URL) - URL field
   - Decision Maker (Text) - Single line
   - Title (Text) - Single line
   - LinkedIn Profile (URL) - URL field
   - Email (Email) - Email field
   - Phone (Phone Number) - Phone field
   - Locations (Number) - Integer
   - Priority Score (Rating) - 1-10 stars
   - Status (Select) - New, Contacted, Interested, Meeting Scheduled, Opportunity
   - Source URL (URL) - URL field
   - Notes (Text) - Long text

3. **Get API Credentials**:
   - API Key: https://airtable.com/account/tokens
   - Base ID: Found in Airtable URL (https://airtable.com/appXXXXXXXXXXXXXX)
   - Add to `.env`: `AIRTABLE_API_KEY=xxx` and `AIRTABLE_BASE_ID=xxx`

### Usage

```python
from src.crm_export.airtable_exporter import AirtableExporter

exporter = AirtableExporter(
    api_key="your_api_key",
    base_id="your_base_id",
    table_name="Leads"
)

# Export single lead
result = exporter.export_single_lead(lead_dict)

# Bulk export
results = exporter.export_bulk(leads_list, batch_size=10)
```

### Airtable Benefits

- Collaborative interface
- Real-time updates
- Easy filtering and sorting
- Customizable views
- Automation capabilities
- Webhooks for notifications

## HubSpot Integration

### Setup

1. **Create HubSpot Account**:
   - Sign up at https://www.hubspot.com
   - Create account with your email

2. **Create Private App**:
   - Go to: Settings > Integrations > Private Apps
   - Create new private app "OpsCore Leads"
   - Select required scopes:
     - `crm.objects.companies.read`
     - `crm.objects.companies.write`
     - `crm.objects.contacts.read`
     - `crm.objects.contacts.write`

3. **Get API Key**:
   - Copy access token
   - Add to `.env`: `HUBSPOT_API_KEY=xxx`

### Usage

```python
from src.crm_export.hubspot_exporter import HubSpotExporter

exporter = HubSpotExporter(api_key="your_api_key")

# Export single lead
success = exporter.export_lead(lead_dict)

# Bulk export
results = exporter.export_bulk(leads_list)
# Returns: {"successful": 50, "failed": 2, "total": 52}
```

### HubSpot Custom Properties

The system creates these custom properties:
- `custom_property_type` - Property type
- `custom_locations` - Number of locations
- `custom_priority_score` - Priority score (1-10)
- `custom_linkedin_company` - Company LinkedIn URL

## Automated Sync Workflow

### Option 1: Manual Export

```python
from src.automation.workflow_orchestrator import LeadGenerationWorkflow

workflow = LeadGenerationWorkflow()

# Run complete workflow and export
results = workflow.run_complete_workflow(
    search_queries=['hostel', 'hotel'],
    countries=['Thailand', 'Vietnam'],
    export_formats=['csv', 'airtable', 'hubspot']
)
```

### Option 2: Scheduled Sync

Use a task scheduler (cron on Linux/Mac, Task Scheduler on Windows):

```bash
# Run daily at 2 AM
0 2 * * * cd /path/to/opscore-lead-generation && python scripts/daily_sync.py
```

## Conflict Resolution

When syncing to multiple CRMs:

1. **Primary CRM**: Designate one CRM as primary (e.g., HubSpot)
2. **Last Update Wins**: Use timestamp to determine source of truth
3. **Manual Review**: Flag conflicts for manual review
4. **Duplicate Detection**: Check for existing records before creating

## Data Mapping

### Airtable Mapping

```
Lead Dictionary → Airtable Fields
company_name → Company
property_name → Property
property_type → Property Type
city → City
country → Country
website → Website
linkedin_company → LinkedIn Company
decision_maker → Decision Maker
decision_maker_title → Title
decision_maker_linkedin → LinkedIn Profile
email → Email
phone → Phone
num_locations → Locations
priority_score → Priority Score
notes → Notes
```

### HubSpot Mapping

```
Company Fields:
company_name → name
website → website
property_type → custom_property_type
num_locations → custom_locations
priority_score → custom_priority_score
linkedin_company → custom_linkedin_company

Contact Fields:
decision_maker → firstname + lastname
decision_maker_title → jobtitle
email → email
phone → phone
decision_maker_linkedin → linkedin_url
```

## Error Handling

### Common Issues

**API Rate Limits**
```python
# Solution: Implement exponential backoff
from time import sleep

max_retries = 3
for attempt in range(max_retries):
    try:
        result = exporter.export_lead(lead)
        break
    except RateLimitError:
        wait_time = 2 ** attempt  # 1, 2, 4 seconds
        sleep(wait_time)
```

**Invalid Data**
```python
# Validate before export
from config.settings import CSV_COLUMNS

required_fields = ['company_name', 'decision_maker', 'email']
for lead in leads:
    for field in required_fields:
        if not lead.get(field):
            lead[field] = "N/A"  # Default value
```

**Duplicate Handling**
```python
# Check for existing records in HubSpot
def check_duplicate(company_name):
    # Query HubSpot for company
    existing = hubspot_api.search_companies(company_name)
    return len(existing) > 0
```

## Best Practices

1. **Data Quality**
   - Validate all data before export
   - Remove duplicates
   - Standardize formats (dates, phone numbers, etc.)

2. **Incremental Exports**
   - Only export new/updated leads
   - Track last export timestamp
   - Maintain sync state

3. **Monitoring**
   - Log all exports
   - Track success/failure rates
   - Alert on errors
   - Monitor API usage

4. **Security**
   - Store API keys in `.env`, never in code
   - Use HTTPS for all API calls
   - Rotate API keys regularly
   - Audit access logs

## Testing

```bash
# Run CSV export tests
pytest tests/test_crm_export.py::TestCSVExporter -v

# Run integration tests
pytest tests/test_crm_export.py -v
```

---

**Last Updated**: June 5, 2026
**Version**: 1.0.0
