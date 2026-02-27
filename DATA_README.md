# University Data - Now in JSON!

## What Changed

The university, scholarship, and salary data has been moved from hardcoded Python dictionaries to a separate **`university_data.json`** file.

## Benefits

✅ **Easy to update** - Edit JSON file without touching code
✅ **Version control** - Track data changes separately
✅ **Maintainable** - Clear structure
✅ **Expandable** - Easy to add new universities/scholarships

## File Structure

```
university_data.json
├── universities/          # University details
│   ├── MIT
│   ├── Stanford
│   ├── Oxford
│   └── ...
├── scholarships/          # Scholarship details
│   ├── LPDP
│   ├── Chevening
│   └── ...
└── scholarship_availability/  # Which scholarships available at each uni
```

## How to Add a New University

Edit `university_data.json` and add:

```json
"Your University": {
  "name": "Full University Name",
  "country": "Country",
  "city": "City",
  "tuition_per_year": 50000,
  "living_per_year": 20000,
  "duration_years": 2,
  "tier": 1,
  "salaries": {
    "Country": 100000,
    "Indonesia": 30000
  }
}
```

Then add to `scholarship_availability`:

```json
"Your University": ["LPDP", "Other Scholarship", "No Scholarship (Self-fund)"]
```

## How to Add a New Scholarship

Add to `scholarships` section:

```json
"Your Scholarship": {
  "name": "Full Scholarship Name",
  "tuition_coverage": 1.0,
  "living_coverage": 1.0,
  "flights_covered": true,
  "return_required": false,
  "return_years": 0,
  "eligible_countries": ["All"],
  "success_rate": "Medium",
  "notes": "Additional info"
}
```

## Current Data

**Universities:** 10
- MIT, Stanford, Carnegie Mellon (USA)
- Oxford, Cambridge, Imperial (UK)
- ETH Zurich (Switzerland)
- TUM Munich (Germany)
- NUS Singapore
- Erasmus Mundus EMAI (Europe)

**Scholarships:** 13
- LPDP, Chevening, Australia Awards
- Erasmus Mundus, ETH ESOP, DAAD
- Spärck AI, Knight Hennessy, Gates Cambridge
- Commonwealth, NUS Scholarship
- University Merit (Partial), Self-fund

## Usage in App

The app automatically loads data on startup:

```python
DATA = load_university_data()
UNIVERSITIES = DATA['universities']
SCHOLARSHIPS = DATA['scholarships']
SCHOLARSHIP_AVAILABILITY = DATA['scholarship_availability']
```

All calculations now reference this JSON data instead of hardcoded values.

## To Update Data

1. Edit `university_data.json`
2. Save the file
3. Refresh the Streamlit app (it will reload automatically)

That's it! No code changes needed.
