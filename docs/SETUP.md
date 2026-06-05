# OpsCore Lead Generation Engine - Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git
- Virtual environment manager (venv or conda)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/claylakesfood-spec/opscore-lead-generation.git
cd opscore-lead-generation
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=sqlite:///./opscore_leads.db

# External APIs
LINKEDIN_API_KEY=your_linkedin_api_key
AIRTABLE_API_KEY=your_airtable_api_key
AIRTABLE_BASE_ID=your_airtable_base_id
HUBSPOT_API_KEY=your_hubspot_api_key

# Application
DEBUG=True
```

## API Configuration

### LinkedIn API

1. Create a LinkedIn Developer account at https://www.linkedin.com/developers
2. Create a new app
3. Get your API credentials (API Key, Secret Key)
4. Add to `.env` file

### Airtable Integration

1. Sign up for Airtable at https://airtable.com
2. Create a new base for "OpsCore Leads"
3. Get your API key from https://airtable.com/account/tokens
4. Get your base ID from the Airtable URL
5. Add to `.env` file

### HubSpot Integration

1. Create HubSpot account at https://www.hubspot.com
2. Generate private app token from Settings > Integrations > Private Apps
3. Add to `.env` file

## Database Setup

### Initialize Database

```bash
python -c "from database.models import Base, engine; Base.metadata.create_all(engine)"
```

### Database Models

The system uses the following tables:
- `companies`: Company and property information
- `decision_makers`: Decision-maker contact information
- `outreach_messages`: Generated and sent messages
- `contact_history`: Contact status and responses

## Running the Application

### Start Dashboard

```bash
streamlit run dashboard/app.py
```

The dashboard will be available at `http://localhost:8501`

### Run Lead Generation Workflow

```bash
python -c "from src.automation.workflow_orchestrator import LeadGenerationWorkflow; workflow = LeadGenerationWorkflow(); workflow.run_complete_workflow(['hostel', 'hotel'], ['Thailand', 'Vietnam'], ['csv', 'airtable', 'hubspot'])"
```

## Data Collection

### Sources

The system collects data from:

1. **Company Websites**: Direct scraping of publicly available information
2. **LinkedIn**: Company pages and decision-maker profiles (requires API access)
3. **Business Directories**: Crunchbase, Builtwith, Hunter, etc.
4. **Industry Publications**: News articles and announcements

### Data Privacy

⚠️ **Important**: Only collect publicly available information. Do not:
- Scrape private/non-public data
- Violate website terms of service
- Use unauthorized data access methods
- Harvest email addresses from non-public sources

## Project Structure

```
opscore-lead-generation/
├── config/
│   ├── settings.py          # Configuration and constants
│   └── __init__.py
├── src/
│   ├── data_collection/     # Web scraping and API integrations
│   ├── lead_scoring/        # Lead prioritization engine
│   ├── crm_export/          # CSV, Airtable, HubSpot exports
│   ├── outreach/            # Message generation and templates
│   └── automation/          # Workflow orchestration
├── database/
│   ├── models.py            # SQLAlchemy models
│   └── __init__.py
├── dashboard/
│   ├── app.py               # Streamlit dashboard
│   └── __init__.py
├── data/
│   ├── leads/               # Lead data (CSV/JSON)
│   ├── templates/           # Message templates
│   └── exports/             # Exported files
├── tests/
│   ├── test_scoring.py
│   ├── test_crm_export.py
│   └── __init__.py
├── logs/                    # Application logs
├── requirements.txt         # Python dependencies
├── .gitignore
└── README.md
```

## Troubleshooting

### Import Errors

If you get import errors, ensure:
1. Virtual environment is activated
2. All dependencies are installed: `pip install -r requirements.txt`
3. Python path is correct: `export PYTHONPATH="${PYTHONPATH}:$(pwd)"`

### API Connection Issues

1. Verify API keys are correct in `.env` file
2. Check API rate limits
3. Ensure network connectivity
4. Review API documentation for authentication requirements

### Database Errors

1. Delete existing database and reinitialize: `rm opscore_leads.db`
2. Run: `python -c "from database.models import Base, engine; Base.metadata.create_all(engine)"`
3. Check database file permissions

## Next Steps

1. Configure all API keys in `.env`
2. Initialize the database
3. Start the dashboard
4. Begin lead discovery workflow
5. Monitor progress through dashboard
6. Export leads to CRM systems

## Support

For issues or questions:
1. Check the documentation files in `/docs`
2. Review logs in `/logs` directory
3. Consult API provider documentation
4. Contact OpsCore team

---

**Last Updated**: June 5, 2026
**Version**: 1.0.0
