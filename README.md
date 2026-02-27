# AI Master's Assessment Tool - Project Summary

## 📁 Project Structure

```
Masters/
├── streamlit_app.py                    # Main Streamlit app
├── university_data.json                # Single source of truth (all data)
├── utils/
│   ├── __init__.py                     # Package marker
│   ├── assessment.py                   # Scoring & tier functions
│   └── data_loader.py                  # JSON loading
├── personal_profile.md                 # Your profile template
├── assess_profile.py                   # CLI version (optional)
└── [Documentation files]
    ├── AI_Masters_Decision_Tree.md
    ├── Research_Gaps_and_Next_Steps.md
    ├── Scholarships_for_Indonesian_Students.md
    ├── Universal_Scholarships_AI_Masters.md
    ├── University_Scholarship_Country_Matrix.md
    └── AI_Masters_References.md
```

## 🎯 Main Features

### 1. **Profile Assessment**
- Competitiveness score (0-100)
- University tier recommendation (1-3)
- Chevening eligibility check
- Recommended path (A/B/C)

### 2. **Path Recommendations**
- **Path A:** Indonesia Career (LPDP, return required)
- **Path B:** International Career (no return)
- **Path C:** Hybrid (LPDP → return → then international)

### 3. **Scholarship Recommendations**
- Prioritized by success rate
- Conditional based on profile
- Action items with deadlines

### 4. **Financial Calculator**
- Compare university-scholarship combinations
- Real-time cost breakdown
- ROI analysis

### 5. **Tabs Organization**
- 💰 Scholarships
- 🏛️ Universities  
- 📊 Comparison (sortable/filterable table with budget analysis)
- 🌳 Decision Tree (interactive Mermaid flowchart)
- 📋 Action Items (Urgent/High/Medium)
- ⚠️ Warnings
- ⭐ Top Picks

### 6. **New Features (v2.0)**
- **32 Universities** across 4 regions (North America, Europe, Asia, Asia-Pacific)
- **QS Rankings 2026** - All universities ranked (8 in Top 10, 29 in Top 100)
- **Scholarship Age Filters** - Age limit data for all scholarships
- **Career Attributes**: Salary tier, visa difficulty, AI maturity, path to PR
- **Program Focus**: Research vs industry orientation
- **Visual Comparison**: Interactive sortable table with filters
- **Budget Analysis**: Self-fund budget slider with affordability indicators
- **Decision Tree**: Mermaid flowchart that highlights your path
- **4 Regions**: North America, Europe, Asia, Asia-Pacific

## 🔧 Technical Stack

- **Frontend:** Streamlit
- **Visualizations:** Plotly, Mermaid
- **Data:** JSON (single source of truth)
- **Modules:** Python utils package
- **Caching:** Streamlit @cache_data

## 📊 Data Structure (university_data.json)

```json
{
  "universities": {...},           // Costs, duration, salaries
  "scholarships": {...},           // Coverage, requirements
  "scholarship_availability": {...}, // Which scholarships per uni
  "paths": {...},                  // A/B/C path details
  "optimal_combinations": [...],   // Top 5 recommendations
  "decision_tree": {...},          // Decision logic
  "action_items": {...},           // Conditional tasks
  "warnings": [...]                // Conditional warnings
}
```

## 🚀 How to Run

```bash
# Install dependencies
pip install streamlit

# Run the app
streamlit run streamlit_app.py
```

## 📝 How to Update Data

**Edit `university_data.json`:**

### Add a University:
```json
"Your University": {
  "name": "Full Name",
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

### Add a Scholarship:
```json
"Your Scholarship": {
  "name": "Full Name",
  "tuition_coverage": 1.0,
  "living_coverage": 1.0,
  "flights_covered": true,
  "return_required": false,
  "return_years": 0,
  "eligible_countries": ["All"],
  "success_rate": "Medium",
  "notes": "Details here"
}
```

### Update Costs/Salaries:
Just edit the numbers in the JSON file. The app will reload automatically.

## 🎓 Key Insights

### For Indonesian Students:

**Best Fully-Funded Options:**
1. **LPDP** - Highest success rate, must return 2+ years
2. **Erasmus Mundus EMAI** - 15 scholarships, no return requirement
3. **ETH ESOP** - Best value (CHF 124k salary), very competitive
4. **DAAD** - Germany, good success rate
5. **Chevening** - UK, requires 2,800 work hours
6. **CSC** - Chinese Government Scholarship, full funding
7. **Swedish Institute** - Sweden, medium success rate
8. **Australia Awards** - Australia, must return 2+ years
9. **Vanier Canada** - Canada, extremely competitive

**Salary Expectations:**
- USA: $140k-$250k (highest)
- Switzerland: CHF 124k (~$138k)
- UK: £60k-£120k (~$75k-$150k)
- Australia: AUD 130-140k (~$87-94k)
- Canada: CAD 71-115k (~$53-86k)
- Germany: €66k (~$72k)
- Netherlands: €56k (~$62k)
- Sweden: SEK 650k (~$65k)
- Denmark: DKK 585k (~$78k)
- Finland: €60k (~$66k)
- China: $62k-75k (varies by city)
- Singapore: $70k
- Indonesia: ~$30k

**Best Value Universities:**
- **RWTH Aachen** - Tier 2, $25k total cost, €72k salary, almost free tuition
- **ETH Zurich** - Tier 1, $47k total cost, $138k salary
- **EPFL** - Tier 1, $47k total cost, $138k salary, French Switzerland
- **University of Alberta** - Tier 2, $62k total cost, CAD 71k salary, Amii (Sutton's lab)
- **Zhejiang University (Hangzhou)** - Tier 1, $45k total cost, $62k salary, 30% cheaper than Beijing
- **TUM Munich** - Tier 2, $54k total cost, €72k salary, easy visa

**Critical Decision:**
- Want international career immediately? → Path B (Erasmus, ETH ESOP, DAAD)
- Willing to return 2+ years? → Path A (LPDP - highest success rate)
- Flexible? → Path C (Apply to both, decide later)

## 🔄 Maintenance

### To Update:
1. **Costs/Salaries:** Edit `university_data.json`
2. **Recommendations:** Edit `paths` section in JSON
3. **Action Items:** Edit `action_items` section in JSON
4. **Warnings:** Edit `warnings` section in JSON

### To Add Features:
1. **New assessment logic:** Edit `utils/assessment.py`
2. **New data source:** Edit `utils/data_loader.py`
3. **New UI components:** Edit `streamlit_app.py`

## 📚 Documentation Files

- **Decision Tree:** Step-by-step path selection
- **Scholarship Guide:** Detailed scholarship information
- **University Matrix:** 3D comparison (uni × scholarship × country)
- **Research Gaps:** What information to gather
- **References:** All sources with URLs

## ✅ Completed Features

- ✅ Profile assessment with scoring
- ✅ Path recommendations (A/B/C)
- ✅ Scholarship recommendations
- ✅ University recommendations
- ✅ Financial calculator with ROI
- ✅ Self-fund budget slider with affordability analysis
- ✅ Action items (conditional)
- ✅ Warnings (conditional)
- ✅ Top picks from research
- ✅ Tabs for organization
- ✅ Region filter (North America, Europe, Asia)
- ✅ Interactive comparison table with filters
- ✅ Decision tree with Mermaid flowchart
- ✅ Career attributes (salary, visa, AI maturity, PR path)
- ✅ Program focus (research vs industry)
- ✅ 32 universities (USA, Canada, UK, Europe, China, Singapore, Australia)
- ✅ 18 scholarships
- ✅ JSON as single source of truth
- ✅ Modular code structure
- ✅ Session state persistence
- ✅ Helpful hints on all inputs

## 🗺️ Roadmap

### ✅ Phase 1: Tool Development (COMPLETE)
- ✅ 32 universities across 4 regions
- ✅ 18 scholarships with eligibility rules
- ✅ Profile assessment with scoring
- ✅ Path recommendations (A/B/C)
- ✅ Financial calculator with ROI
- ✅ Save/load profiles
- ✅ Interactive comparison tables
- ✅ Decision tree visualization

### 🔄 Phase 2: Research & Data Collection (CURRENT)
**Priority: Make the tool actionable**

**Immediate (This Week):**
- [ ] Fill in university URLs (program pages, admissions, curriculum)
- [ ] Fill in scholarship URLs (application pages, requirements)
- [ ] Test the tool end-to-end
- [ ] Input your actual profile and validate recommendations

**Short Term (Next 2 Weeks):**
- [ ] Verify all tuition/living costs are current (2025-2026)
- [ ] Add scholarship application deadlines
- [ ] Validate salary data by country/city
- [ ] Refine assessment scoring if needed
- [ ] Check scholarship age limits and eligibility rules

**Medium Term (Next Month):**
- [ ] Research missing scholarship details
- [ ] Add program-specific requirements (GRE, portfolio, etc.)
- [ ] Validate visa difficulty ratings
- [ ] Update QS rankings when 2027 is released

### 🎯 Phase 3: Application Execution (When Ready)
**Use the tool to:**
1. Get your competitiveness score and tier
2. Identify eligible scholarships (sorted by success rate)
3. Shortlist universities by tier + scholarship availability
4. Calculate total costs and ROI
5. Create action plan with deadlines
6. Track application progress

**Application Strategy:**
- Start with highest success rate scholarships (LPDP, DAAD, Erasmus)
- Apply to 3-5 scholarships (diversify)
- Target 5-8 universities across 2-3 tiers
- Prepare documents early (CV, SOP, recommendations)
- Track deadlines in spreadsheet

### 🚀 Phase 4: Optional Enhancements (If Time Permits)
- [ ] Export assessment results to PDF
- [ ] Add deadline calendar view
- [ ] Compare multiple profiles side-by-side
- [ ] Add more universities (KAIST, HKU, Berkeley, etc.)
- [ ] Integration with scholarship websites
- [ ] Email reminders for deadlines
- [ ] Application document checklist

## 🎓 How to Use This Tool

### For Research Phase:
1. Run `streamlit run streamlit_app.py`
2. Input your profile (even if incomplete)
3. See which tier you're competitive for
4. Explore universities and scholarships in tabs
5. Use comparison table to filter by region/budget
6. Update `university_data.json` as you find new info

### For Decision Making:
1. Input your complete profile
2. Review your competitiveness score
3. Check recommended path (A/B/C)
4. Review eligible scholarships (sorted by success rate)
5. Use financial calculator to compare options
6. Check action items for next steps
7. Save your profile for later

### For Application Tracking:
1. Load your saved profile
2. Check action items tab for deadlines
3. Update scholarship data as you apply
4. Use comparison table to track applications
5. Adjust self-fund budget as needed

## 📞 Support

All data is in `university_data.json` - edit that file to update anything!

The app automatically reloads when you save changes.

---

**Last Updated:** 2026-02-27
**Version:** 1.0
**Status:** ✅ Production Ready
