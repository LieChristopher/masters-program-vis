"""
Assessment and scoring functions
"""

def assess_university_tier(gpa, ielts, toefl, has_research):
    ielts_score = ielts if ielts > 0 else (toefl / 120 * 9) if toefl > 0 else 0
    
    if gpa >= 3.7 and ielts_score >= 7.5 and has_research:
        return "Tier 1 (Elite)", ["MIT", "Stanford", "CMU", "Oxford", "Cambridge", "ETH Zurich"]
    elif gpa >= 3.5 and ielts_score >= 7.0:
        return "Tier 1-2 (Elite to Excellent)", ["Imperial", "NUS", "TUM", "Oxford", "Cambridge", "ETH Zurich"]
    elif gpa >= 3.3 and ielts_score >= 6.5:
        return "Tier 2-3 (Excellent to Very Good)", ["TUM", "NUS", "Edinburgh", "Imperial"]
    else:
        return "Tier 3 (Very Good)", ["TUM", "Edinburgh", "Other strong programs"]

def calculate_competitiveness_score(gpa, ielts, toefl, work_hours, has_research, has_publications):
    score = 0
    
    if gpa >= 3.7:
        score += 30
    elif gpa >= 3.5:
        score += 25
    elif gpa >= 3.3:
        score += 20
    else:
        score += 15
    
    ielts_score = ielts if ielts > 0 else (toefl / 120 * 9) if toefl > 0 else 0
    if ielts_score >= 7.5:
        score += 20
    elif ielts_score >= 7.0:
        score += 15
    elif ielts_score >= 6.5:
        score += 10
    else:
        score += 5
    
    if work_hours >= 2800:
        score += 20
    elif work_hours >= 1400:
        score += 15
    elif work_hours > 0:
        score += 10
    
    if has_research:
        score += 15
    
    if has_publications:
        score += 15
    
    return score

def check_condition(condition, profile):
    if not condition:
        return True
    
    for key, value in condition.items():
        if key not in profile:
            continue
        
        if isinstance(value, dict):
            if 'lt' in value and profile[key] >= value['lt']:
                return False
            if 'gt' in value and profile[key] <= value['gt']:
                return False
        elif isinstance(value, list):
            if profile[key] not in value:
                return False
        else:
            if profile[key] != value:
                return False
    
    return True
