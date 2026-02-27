"""
Profile Loader and Validator
Loads user profile from my_profile.json and validates it
"""

import json
from typing import Dict, Any, List

def load_profile(filepath: str = "my_profile.json") -> Dict[str, Any]:
    """Load profile from JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def save_profile(profile: Dict[str, Any], filepath: str = "my_profile.json"):
    """Save profile to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(profile, f, indent=2)

def validate_profile(profile: Dict[str, Any]) -> List[str]:
    """Validate profile and return list of missing/invalid fields"""
    issues = []
    
    # Check required fields
    if not profile['profile']['personal']['name']:
        issues.append("Missing: Name")
    
    if not profile['profile']['personal']['age']:
        issues.append("Missing: Age")
    
    if not profile['profile']['academic']['undergraduate']['gpa']:
        issues.append("Missing: GPA")
    
    if not profile['profile']['language']['english']['ielts'] and \
       not profile['profile']['language']['english']['toefl_ibt']:
        issues.append("Missing: English test score (IELTS or TOEFL)")
    
    # Check age limits for scholarships
    age = profile['profile']['personal']['age']
    if age and age > 35:
        issues.append("Warning: Age > 35 (LPDP mid-career and CSC not eligible)")
    
    # Check work hours for Chevening
    work_hours = profile['profile']['work_experience']['current_position']['total_hours']
    if work_hours and work_hours < 2800:
        issues.append("Warning: Work hours < 2,800 (Chevening requires 2,800+)")
    
    return issues

def calculate_competitiveness_score(profile: Dict[str, Any]) -> int:
    """Calculate competitiveness score (0-100)"""
    score = 0
    
    # GPA (30 points)
    gpa = profile['profile']['academic']['undergraduate']['gpa']
    gpa_scale = profile['profile']['academic']['undergraduate']['gpa_scale']
    if gpa:
        normalized_gpa = (gpa / gpa_scale) * 4.0
        if normalized_gpa >= 3.7:
            score += 30
        elif normalized_gpa >= 3.5:
            score += 25
        elif normalized_gpa >= 3.3:
            score += 20
        elif normalized_gpa >= 3.0:
            score += 15
        else:
            score += 10
    
    # English (20 points)
    ielts = profile['profile']['language']['english']['ielts']
    toefl = profile['profile']['language']['english']['toefl_ibt']
    if ielts:
        if ielts >= 7.5:
            score += 20
        elif ielts >= 7.0:
            score += 17
        elif ielts >= 6.5:
            score += 14
        else:
            score += 10
    elif toefl:
        if toefl >= 100:
            score += 20
        elif toefl >= 90:
            score += 17
        elif toefl >= 80:
            score += 14
        else:
            score += 10
    
    # Work Experience (20 points)
    years = profile['profile']['work_experience']['years_of_experience']
    if years >= 3:
        score += 20
    elif years >= 2:
        score += 15
    elif years >= 1:
        score += 10
    else:
        score += 5
    
    # Research/Publications (15 points)
    publications = len(profile['profile']['academic']['achievements']['publications'])
    if publications >= 3:
        score += 15
    elif publications >= 2:
        score += 12
    elif publications >= 1:
        score += 8
    else:
        score += 0
    
    # Awards/Achievements (15 points)
    awards = len(profile['profile']['academic']['achievements']['awards'])
    deans_list = profile['profile']['academic']['achievements']['deans_list']
    if awards >= 2 or deans_list:
        score += 15
    elif awards >= 1:
        score += 10
    else:
        score += 5
    
    return min(score, 100)

def recommend_tier(score: int) -> int:
    """Recommend university tier based on score"""
    if score >= 80:
        return 1  # Tier 1: MIT, Stanford, Oxford, etc.
    elif score >= 60:
        return 2  # Tier 2: Good universities
    else:
        return 3  # Tier 3: Safety options

def recommend_path(profile: Dict[str, Any]) -> str:
    """Recommend path (A/B/C) based on profile"""
    willing_to_return = profile['profile']['career_goals']['willing_to_return_indonesia']
    scholarship_priority = profile['profile']['financial']['scholarship_priority']
    budget = profile['profile']['financial']['self_funding_budget_usd']
    
    if scholarship_priority == "must_have_full" and willing_to_return:
        return "A"  # LPDP path
    elif budget > 100000 or scholarship_priority == "can_self_fund":
        return "B"  # International career, self-funded
    else:
        return "C"  # Flexible, apply to both

def get_profile_summary(profile: Dict[str, Any]) -> str:
    """Generate profile summary"""
    score = calculate_competitiveness_score(profile)
    tier = recommend_tier(score)
    path = recommend_path(profile)
    
    summary = f"""
PROFILE SUMMARY
===============

Personal:
  Name: {profile['profile']['personal']['name'] or 'Not provided'}
  Age: {profile['profile']['personal']['age'] or 'Not provided'}
  
Academic:
  GPA: {profile['profile']['academic']['undergraduate']['gpa'] or 'Not provided'}
  University: {profile['profile']['academic']['undergraduate']['university'] or 'Not provided'}
  
English:
  IELTS: {profile['profile']['language']['english']['ielts'] or 'Not provided'}
  TOEFL: {profile['profile']['language']['english']['toefl_ibt'] or 'Not provided'}
  
Work Experience:
  Years: {profile['profile']['work_experience']['years_of_experience']}
  Level: {profile['profile']['work_experience']['career_level']}

ASSESSMENT
==========

Competitiveness Score: {score}/100
Recommended Tier: {tier}
Recommended Path: {path}

Tier {tier} Universities:
"""
    
    if tier == 1:
        summary += "  - MIT, Stanford, Oxford, Cambridge, ETH, Tsinghua, Peking, etc."
    elif tier == 2:
        summary += "  - Imperial, UCL, Toronto, Melbourne, SJTU, Zhejiang, etc."
    else:
        summary += "  - Aalto, Erasmus Mundus, SUSTech, etc."
    
    return summary

if __name__ == "__main__":
    # Example usage
    try:
        profile = load_profile()
        
        # Validate
        issues = validate_profile(profile)
        if issues:
            print("⚠️  Profile Issues:")
            for issue in issues:
                print(f"  - {issue}")
            print()
        
        # Show summary
        print(get_profile_summary(profile))
        
    except FileNotFoundError:
        print("❌ Profile file not found. Please fill in my_profile.json")
    except json.JSONDecodeError:
        print("❌ Invalid JSON format in profile file")
