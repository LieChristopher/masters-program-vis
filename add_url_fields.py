#!/usr/bin/env python3
"""Add URL fields to all universities and scholarships in university_data.json"""

import json

# Load the data
with open('university_data.json', 'r') as f:
    data = json.load(f)

# Add urls field to all universities
for uni_key, uni_data in data['universities'].items():
    if 'urls' not in uni_data:
        uni_data['urls'] = {
            "website": "",
            "program_page": "",
            "admissions": "",
            "curriculum": ""
        }

# Add urls field to all scholarships
for scholarship_key, scholarship_data in data['scholarships'].items():
    if 'urls' not in scholarship_data:
        scholarship_data['urls'] = {
            "website": "",
            "application_page": "",
            "requirements": ""
        }

# Save the updated data
with open('university_data.json', 'w') as f:
    json.dump(data, f, indent=2)

print("✅ Added URL fields to all universities and scholarships")
print(f"   - {len(data['universities'])} universities updated")
print(f"   - {len(data['scholarships'])} scholarships updated")
