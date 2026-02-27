# Profile System - User Guide

## 📁 Files

1. **my_profile.md** - Human-readable profile template (fill this in!)
2. **my_profile.json** - Machine-readable profile data
3. **profile_loader.py** - Python utility to load and validate profile

---

## 🚀 Quick Start

### Step 1: Fill in Your Profile

Open `my_profile.md` and fill in your information. This is the main file you'll edit.

**Required Fields:**
- Name
- Age
- GPA
- English test score (IELTS or TOEFL)
- Career goals
- Financial situation

**Optional but Recommended:**
- Work experience
- Research interests
- Target universities
- Language skills

### Step 2: Update JSON (Optional)

If you want to use the programmatic features, also update `my_profile.json` with the same information.

### Step 3: Validate Your Profile

Run the validator to check for issues:

```bash
python3 profile_loader.py
```

This will show:
- Missing required fields
- Competitiveness score (0-100)
- Recommended university tier (1/2/3)
- Recommended path (A/B/C)

---

## 📊 Scoring System

### Competitiveness Score (0-100)

**Components:**
- **GPA (30 points)**
  - 3.7+: 30 points
  - 3.5-3.69: 25 points
  - 3.3-3.49: 20 points
  - 3.0-3.29: 15 points

- **English (20 points)**
  - IELTS 7.5+: 20 points
  - IELTS 7.0-7.4: 17 points
  - IELTS 6.5-6.9: 14 points
  - (or equivalent TOEFL)

- **Work Experience (20 points)**
  - 3+ years: 20 points
  - 2-3 years: 15 points
  - 1-2 years: 10 points
  - <1 year: 5 points

- **Research/Publications (15 points)**
  - 3+ publications: 15 points
  - 2 publications: 12 points
  - 1 publication: 8 points

- **Awards (15 points)**
  - 2+ awards or Dean's List: 15 points
  - 1 award: 10 points
  - None: 5 points

### Tier Recommendations

- **Score 80-100:** Tier 1 (MIT, Stanford, Oxford, Tsinghua, etc.)
- **Score 60-79:** Tier 2 (Imperial, Toronto, Melbourne, SJTU, etc.)
- **Score 0-59:** Tier 3 (Aalto, Erasmus Mundus, etc.)

### Path Recommendations

- **Path A (Indonesia Career):** Must have full scholarship + willing to return
- **Path B (International Career):** Can self-fund or no return requirement
- **Path C (Flexible):** Apply to both, decide later

---

## ⚠️ Important Checks

### Age Limits
- **LPDP:** Max 35 years (mid-career), no limit for fresh graduates
- **CSC:** Max 35 years
- **Others:** No age limit

### Work Hours
- **Chevening:** Requires 2,800+ work hours

### English Requirements
- **Most universities:** IELTS 6.5+ or TOEFL 90+
- **Top universities:** IELTS 7.0+ or TOEFL 100+

---

## 🎯 Using Your Profile with the App

### In Streamlit App

The app can load your profile automatically:

```python
import profile_loader

# Load profile
profile = profile_loader.load_profile()

# Get assessment
score = profile_loader.calculate_competitiveness_score(profile)
tier = profile_loader.recommend_tier(score)
path = profile_loader.recommend_path(profile)

# Filter universities by tier
recommended_unis = [u for u in universities if u['tier'] == tier]
```

### Manual Assessment

1. Fill in `my_profile.md`
2. Run `python3 profile_loader.py`
3. Note your score and tier
4. Use the Streamlit app to filter universities by your tier
5. Check scholarship eligibility based on your age and work hours

---

## 📝 Profile Fields Explained

### Career Paths

**Path A (Indonesia Career):**
- Take LPDP or similar scholarship
- Return to Indonesia for 2+ years
- Build career in Indonesia
- Best for: Government, academia, local companies

**Path B (International Career):**
- No return requirement
- Stay abroad after graduation
- Pursue PR/citizenship
- Best for: Tech companies, research, startups

**Path C (Flexible):**
- Apply to both types of scholarships
- Decide after getting offers
- Keep options open
- Best for: Undecided students

### Priority Factors (1-5 scale)

Rate each factor from 1 (lowest) to 5 (highest):

- **Salary:** How important is high salary?
- **PR/Immigration:** How important is easy PR path?
- **Cost:** How important is low cost?
- **Proximity to Indonesia:** How important is being close to home?
- **Research Quality:** How important is top research?
- **Work-Life Balance:** How important is quality of life?

---

## 🔄 Updating Your Profile

### When to Update

- After getting new test scores
- After gaining work experience
- After publishing research
- After receiving awards
- When priorities change

### How to Update

1. Edit `my_profile.md` (human-readable)
2. Update `my_profile.json` (if using programmatic features)
3. Run `python3 profile_loader.py` to see new assessment
4. Update `last_updated` date in metadata

---

## 💡 Tips

### Improving Your Score

**To reach Tier 1 (80+):**
- GPA 3.7+ (30 points)
- IELTS 7.5+ (20 points)
- 3+ years work experience (20 points)
- 2+ publications (12 points)
- Awards/Dean's List (15 points)

**To reach Tier 2 (60+):**
- GPA 3.5+ (25 points)
- IELTS 7.0+ (17 points)
- 2+ years work experience (15 points)
- 1+ publication (8 points)
- Some awards (10 points)

### Scholarship Strategy

**High Score (80+):**
- Apply to competitive scholarships (Chevening, Gates Cambridge, Vanier)
- Target Tier 1 universities
- Focus on research-based programs

**Medium Score (60-79):**
- Apply to LPDP, DAAD, Erasmus Mundus
- Target Tier 2 universities
- Mix of research and coursework programs

**Lower Score (<60):**
- Focus on LPDP (highest success rate)
- Target Tier 3 universities
- Consider improving profile before applying

---

## 📞 Support

If you have questions about filling in your profile:

1. Check the examples in `my_profile.md`
2. Review the scoring system above
3. Run the validator to see what's missing
4. Consult the main README.md for university/scholarship info

---

**Last Updated:** 2026-02-27
**Version:** 1.0
