# Lead Scoring Algorithm - Technical Documentation

## Overview

The lead scoring engine prioritizes potential customers on a 1-10 scale based on:
- Property type and business model
- Number of locations/operational scale
- Decision-maker position/authority
- Information completeness

## Scoring Formula

```
Final Score = Property Type Score + Multi-Location Bonus + Title Boost + Information Bonus
(Capped at 10, minimum 1)
```

## Scoring Components

### 1. Property Type Score

Base score assigned by property/business type:

| Property Type | Score | Reasoning |
|---------------|-------|----------|
| Hostel Chain | 10 | Multi-unit, high operational complexity |
| Hotel Group | 10 | Multi-unit, complex operations |
| Coworking Space | 8 | Multiple operations, facilities needs |
| Serviced Apartments | 8 | Ongoing maintenance, guest services |
| Boutique Hotel | 7 | Boutique operations, quality focus |
| Facilities Management Company | 7 | Professional target audience |
| Property Management Company | 7 | Professional target audience |
| Student Accommodation | 6 | Regular maintenance, operations |
| Event Venue | 6 | Operational complexity |
| Commercial Property | 5 | Potential facilities needs |
| Independent Hostel | 4 | Single property, limited scope |

### 2. Multi-Location Bonus

Bonus points for operating multiple properties:

| Locations | Bonus | Tier |
|-----------|-------|------|
| 5+ | +3 | Tier 1 |
| 2-4 | +1.5 | Tier 2 |
| 1 | 0 | Single Location |

**Rationale**: Companies with multiple locations have:
- Higher operational complexity
- Greater need for centralized management
- Larger maintenance budgets
- More decision-making authority at management level

### 3. Decision-Maker Title Boost

Additional points based on decision-maker role:

| Title | Boost | Authority |
|-------|-------|----------|
| Founder | +2 | Highest (strategic decisions) |
| Owner | +2 | Highest (strategic decisions) |
| Managing Director | +2 | High (company strategy) |
| Operations Director | +1.5 | High (operational decisions) |
| General Manager | +1.5 | High (property/site level) |
| Operations Manager | +1 | Medium (day-to-day ops) |
| Facilities Manager | +1 | Medium (facilities focus) |
| Property Manager | +1 | Medium (property focus) |
| Engineering Manager | +1 | Medium (maintenance) |
| Asset Manager | +1 | Medium (asset focus) |

**Rationale**: Higher-level titles indicate:
- Better buying authority
- Strategic decision-making power
- Higher likelihood of approval
- Better budget access

### 4. Information Completeness Bonus

Bonus points for complete lead data (max +2):

| Data Point | Bonus |
|------------|-------|
| Valid email | +0.5 |
| Valid phone | +0.5 |
| LinkedIn profile | +0.5 |
| Company website | +0.5 |

**Rationale**: Complete data indicates:
- Higher data quality
- Easier to reach out
- Better for follow-up
- More reliable information

## Tier Classification

### Tier 1: PRIORITY 10 (Highest)

**Score**: 10

**Characteristics**:
- Multi-property operators (5+ locations)
- Hostel or hotel chains
- Major operational complexity
- Founded or owned by decision-maker
- Complete contact information

**Outreach Strategy**:
- Immediate priority
- Senior management outreach
- Personalized approach
- Executive brief highlighting ROI

**Expected Conversion**: High (20-30%)

### Tier 2: PRIORITY 7-9

**Score**: 7-9

**Characteristics**:
- Boutique hotel groups (2-4 properties)
- Coworking operators
- Serviced apartment operators
- Operations/General Manager level contacts
- Good contact information

**Outreach Strategy**:
- Secondary priority
- Operations manager outreach
- Focus on efficiency gains
- Operational review offer

**Expected Conversion**: Medium (10-20%)

### Tier 3: PRIORITY 4-6

**Score**: 4-6

**Characteristics**:
- Independent hostels
- Small operators (2-4 locations)
- Facility/Property manager contacts
- Partial contact information

**Outreach Strategy**:
- Tertiary priority
- Facility manager outreach
- Focus on cost savings
- Practical benefits emphasis

**Expected Conversion**: Low (5-10%)

### Tier 4: PRIORITY 1-3 (Lowest)

**Score**: 1-3

**Characteristics**:
- Single-location operators
- Limited operational complexity
- Minimal decision-making authority
- Incomplete contact information

**Outreach Strategy**:
- Lower priority
- Generic outreach
- Lower-touch approach
- Minimal personalization

**Expected Conversion**: Very Low (<5%)

## Scoring Examples

### Example 1: Mad Monkey Hostels (Tier 1)

```
Company: Mad Monkey Hostels
Property Type: Hostel Chain                          +10
Locations: 5 properties                               +3
Decision Maker Title: Founder                         +2
Contact Info: Email + Phone + LinkedIn               +1.5
                                                    ------
Total Score:                                          16.5
Capped at:                                            10

Tier: PRIORITY 10 - Multi-property Operators
```

### Example 2: Slumber Party Hostels (Tier 2)

```
Company: Slumber Party Hostels
Property Type: Hostel Chain                          +10
Locations: 3 properties                               +1.5
Decision Maker Title: General Manager                 +1.5
Contact Info: Email + LinkedIn                       +1.0
                                                    ------
Total Score:                                          14.0
Capped at:                                            10
Adjusted:                                             8 (regional tier 2)

Tier: PRIORITY 7-9 - Boutique Groups
```

### Example 3: Once Again Hostel (Tier 3)

```
Company: Once Again Hostel
Property Type: Independent Hostel                    +4
Locations: 1 property                                 +0
Decision Maker Title: Manager                         +0
Contact Info: Email only                             +0.5
                                                    ------
Total Score:                                          4.5
Rounded:                                              5

Tier: PRIORITY 4-6 - Independent Operators
```

## Dynamic Adjustment Factors

The engine can be adjusted for:

1. **Geographic Multiplier**: Higher scores for target regions
   - Phase 1 countries (Thailand): 1.0x
   - Phase 2 countries: 0.9x

2. **Seasonal Adjustments**: Account for business cycles
   - Peak season (+10%)
   - Off-season (-10%)

3. **Competitive Density**: Adjust based on market saturation
   - High competition: -0.5x
   - Emerging market: +1.2x

## Implementation

The scoring engine is implemented in `src/lead_scoring/scoring_engine.py`:

```python
from src.lead_scoring.scoring_engine import LeadScoringEngine, LeadData

engine = LeadScoringEngine()
lead = LeadData(
    company_name="Mad Monkey Hostels",
    property_type="Hostel Chain",
    decision_maker_title="Founder",
    num_locations=5,
    # ... other fields
)

result = engine.score_lead(lead)
print(f"Priority Score: {result.priority_score}/10")
print(f"Tier: {result.tier}")
print(f"Reasoning: {result.reasoning}")
```

## Performance Metrics

Track scoring effectiveness:

1. **Scoring Distribution**: % of leads in each tier
   - Target: 5-10% Tier 1, 20-30% Tier 2, 30-40% Tier 3, 20-40% Tier 4

2. **Conversion by Tier**:
   - Track conversion rates per tier
   - Adjust weights based on actual results

3. **False Positives/Negatives**:
   - Monitor leads that don't convert despite high scores
   - Identify scoring adjustments needed

## Continuous Improvement

The scoring algorithm should be reviewed quarterly:

1. Analyze conversion rates by tier
2. Identify outliers and misclassifications
3. Adjust weights based on market feedback
4. Update property type scores
5. Add new decision-maker titles as needed

---

**Last Updated**: June 5, 2026
**Algorithm Version**: 1.0
