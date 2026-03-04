"""
Assessment and scoring functions
"""

def convert_to_usd(amount, currency, exchange_rates):
    """Convert any currency to USD"""
    if currency == 'USD':
        return amount
    
    rates = exchange_rates.get('rates', {})
    rate = rates.get(currency, 1)
    
    if rate == 0:
        return amount
    
    return amount / rate

def get_cost_usd(uni_data, exchange_rates):
    """Get total cost in USD"""
    tuition = uni_data['tuition_per_year']
    living = uni_data['living_per_year']
    
    tuition_usd = convert_to_usd(tuition['amount'], tuition['currency'], exchange_rates)
    living_usd = convert_to_usd(living['amount'], living['currency'], exchange_rates)
    
    total_per_year = tuition_usd + living_usd
    total_cost = total_per_year * uni_data['duration_years']
    
    return total_cost

def calculate_tier_from_rankings(uni_data):
    """Calculate tier from QS, THE, CSRankings average"""
    qs = uni_data.get('qs_ranking_2026')
    the = uni_data.get('the_ranking_2026')
    cs = uni_data.get('csrankings_ai_2026')
    
    # Filter out None values
    rankings = [r for r in [qs, the, cs] if r is not None]
    
    if not rankings:
        return 3  # Default to Tier 3 if no rankings
    
    avg_ranking = sum(rankings) / len(rankings)
    
    if avg_ranking < 20:
        return 1
    elif avg_ranking < 50:
        return 2
    else:
        return 3

def get_tier(uni_data):
    """Get tier with override support"""
    if uni_data.get('tier_override') is not None:
        return uni_data['tier_override']
    return calculate_tier_from_rankings(uni_data)

def is_tier_overridden(uni_data):
    """Check if tier is overridden"""
    return uni_data.get('tier_override') is not None

def get_salary_usdˀ(uni_data, countries_data, exchange_rates):
    """Calculate Indonesian salary in Rp from USD salary"""
    country = uni_data.get('country')
    if country not in uni_data.get('salaries', {}):
        return None
    
    usd_salary = uni_data['salaries'][country]
    
    if country == 'Indonesia':
        return usd_salary  # Already in Rp
    
    if 'rates_to_idr' not in exchange_rates:
        return None
    
    exchange_rate = exchange_rates['rates_to_idr'].get('USD', 16000)
    return int(usd_salary * exchange_rate)

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
