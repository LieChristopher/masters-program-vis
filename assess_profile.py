#!/usr/bin/env python3
"""
AI Master's Program Assessment Tool
Analyzes your profile and recommends optimal scholarship and university paths
"""

def get_input(prompt, default=""):
    """Get user input with optional default"""
    response = input(f"{prompt} [{default}]: ").strip()
    return response if response else default

def get_float(prompt, default=0.0):
    """Get float input"""
    while True:
        try:
            response = input(f"{prompt} [{default}]: ").strip()
            return float(response) if response else default
        except ValueError:
            print("Please enter a valid number")

def get_yes_no(prompt):
    """Get yes/no input"""
    while True:
        response = input(f"{prompt} (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        print("Please enter 'yes' or 'no'")

def assess_university_tier(gpa, ielts, toefl, has_research):
    """Determine which tier of universities the candidate can target"""
    # Convert TOEFL to IELTS equivalent roughly
    ielts_score = ielts if ielts > 0 else (toefl / 120 * 9) if toefl > 0 else 0
    
    if gpa >= 3.7 and ielts_score >= 7.5 and has_research:
        return "Tier 1 (Elite)", ["MIT", "Stanford", "CMU", "Oxford", "Cambridge", "ETH Zurich"]
    elif gpa >= 3.5 and ielts_score >= 7.0:
        return "Tier 1-2 (Elite to Excellent)", ["Imperial", "NUS", "TUM", "Oxford", "Cambridge", "ETH Zurich"]
    elif gpa >= 3.3 and ielts_score >= 6.5:
        return "Tier 2-3 (Excellent to Very Good)", ["TUM", "NUS", "Edinburgh", "Imperial"]
    else:
        return "Tier 3 (Very Good)", ["TUM", "Edinburgh", "Other strong programs"]

def assess_chevening_eligibility(work_hours):
    """Check Chevening eligibility"""
    return work_hours >= 2800

def recommend_scholarships(career_location, can_return, work_hours, gpa, can_self_fund):
    """Recommend scholarships based on profile"""
    recommendations = []
    
    # PATH A: Indonesia career (return compatible)
    if career_location == "indonesia" or can_return:
        recommendations.append({
            "name": "LPDP",
            "priority": "HIGHEST",
            "path": "A (Indonesia Career)",
            "funding": "Full",
            "success_rate": "High for Indonesians",
            "constraint": "Must return to Indonesia 2+ years",
            "action": "Apply immediately - check lpdp.kemenkeu.go.id for deadlines"
        })
        
        recommendations.append({
            "name": "Australia Awards",
            "priority": "HIGH",
            "path": "A (Indonesia Career)",
            "funding": "Full",
            "success_rate": "High for Indonesians",
            "constraint": "Must return to Indonesia",
            "action": "Applications open - australiaawardsindonesia.org"
        })
        
        if work_hours >= 2800:
            recommendations.append({
                "name": "Chevening",
                "priority": "HIGH",
                "path": "A (Indonesia Career)",
                "funding": "Full",
                "success_rate": "Medium",
                "constraint": "Must return to Indonesia 2+ years",
                "action": "Applications NOW OPEN - chevening.org/scholarship/indonesia"
            })
    
    # PATH B: International career (no return)
    if career_location == "international" or career_location == "flexible":
        recommendations.append({
            "name": "Erasmus Mundus EMAI",
            "priority": "HIGHEST",
            "path": "B (International Career)",
            "funding": "Full (€1,400/month)",
            "success_rate": "Medium (15 scholarships)",
            "constraint": "None - EU career possible",
            "action": "Applications OPEN for 2026-2028 cohort"
        })
        
        if gpa >= 3.7:
            recommendations.append({
                "name": "ETH Zurich ESOP",
                "priority": "HIGH",
                "path": "B (International Career)",
                "funding": "Full (CHF 12,000/semester)",
                "success_rate": "Very Low (top performers globally)",
                "constraint": "None - Switzerland career possible",
                "action": "Apply with ETH admission - highly competitive"
            })
        
        recommendations.append({
            "name": "Spärck AI Scholarships",
            "priority": "HIGH",
            "path": "B (International Career)",
            "funding": "Full",
            "success_rate": "Unknown (NEW 2026)",
            "constraint": "Verify return requirement",
            "action": "Imperial deadline: March 4, 2026 - URGENT"
        })
        
        recommendations.append({
            "name": "DAAD",
            "priority": "MEDIUM",
            "path": "B (International Career)",
            "funding": "Full (€992/month)",
            "success_rate": "Medium",
            "constraint": "None - Germany career possible",
            "action": "Check daad-indonesia.org for programs"
        })
        
        if can_self_fund:
            recommendations.append({
                "name": "University Merit Scholarships (USA)",
                "priority": "MEDIUM",
                "path": "B (International Career)",
                "funding": "Partial",
                "success_rate": "Medium",
                "constraint": "None - USA career possible (OPT 36 months)",
                "action": "Apply to MIT/Stanford/CMU with scholarship consideration"
            })
    
    return recommendations

def recommend_universities(tier, career_location, can_return, preferences):
    """Recommend universities based on profile and preferences"""
    recommendations = []
    
    tier_num = 1 if "Tier 1" in tier else (2 if "Tier 2" in tier else 3)
    
    # For Indonesia career (LPDP path)
    if career_location == "indonesia" or can_return:
        if tier_num <= 2:
            recommendations.append({
                "university": "MIT / Stanford / CMU",
                "scholarship": "LPDP",
                "outcome": "Return to Indonesia (2+ years required)",
                "salary": "Indonesian market (lower but debt-free)",
                "pros": "Elite education, LPDP network, fully funded",
                "cons": "Must return, cannot work in USA immediately"
            })
            
            recommendations.append({
                "university": "Oxford / Cambridge",
                "scholarship": "LPDP or Chevening",
                "outcome": "Return to Indonesia (2+ years required)",
                "salary": "Indonesian market",
                "pros": "Prestige, 1-year program, fully funded",
                "cons": "Must return to Indonesia"
            })
        
        recommendations.append({
            "university": "NUS Singapore",
            "scholarship": "LPDP",
            "outcome": "Return to Indonesia (2+ years required)",
            "salary": "Indonesian market",
            "pros": "Regional relevance, close to Indonesia, fully funded",
            "cons": "Must return to Indonesia"
        })
    
    # For international career
    if career_location == "international" or career_location == "flexible":
        if "europe" in preferences or "switzerland" in preferences:
            recommendations.append({
                "university": "ETH Zurich",
                "scholarship": "ETH ESOP (or LPDP if returning)",
                "outcome": "Switzerland career (CHF 124k ~$138k)",
                "salary": "CHF 124,000 (~$138,000)",
                "pros": "Best value, high salary, no return requirement",
                "cons": "ESOP extremely competitive"
            })
        
        if "europe" in preferences or "germany" in preferences:
            recommendations.append({
                "university": "TUM (Technical University Munich)",
                "scholarship": "DAAD",
                "outcome": "Germany career (€66k ~$72k)",
                "salary": "€66,000 (~$72,000)",
                "pros": "Fully funded, 18-month job search visa, affordable",
                "cons": "Lower salary than USA/Switzerland"
            })
        
        if "uk" in preferences:
            recommendations.append({
                "university": "Oxford / Cambridge / Imperial",
                "scholarship": "Spärck AI or Commonwealth",
                "outcome": "UK career (£60-120k ~$75-150k)",
                "salary": "£60,000-£120,000",
                "pros": "Prestige, 1-year program, 2-year UK visa",
                "cons": "Spärck AI return requirement unclear"
            })
        
        if "usa" in preferences and tier_num <= 2:
            recommendations.append({
                "university": "MIT / Stanford / CMU",
                "scholarship": "University merit or Knight Hennessy",
                "outcome": "USA career ($140-250k)",
                "salary": "$140,000-$250,000+",
                "pros": "Highest salary, OPT 36 months, elite education",
                "cons": "Partial funding likely, H-1B visa lottery"
            })
        
        recommendations.append({
            "university": "Erasmus Mundus EMAI Consortium",
            "scholarship": "Erasmus Mundus",
            "outcome": "EU career (€59-66k)",
            "salary": "€59,000-€66,000",
            "pros": "Fully funded, multi-country experience, 15 scholarships",
            "cons": "Competitive, consortium universities (not single elite)"
        })
    
    return recommendations

def calculate_competitiveness_score(gpa, ielts, toefl, work_hours, has_research, has_publications):
    """Calculate overall competitiveness score (0-100)"""
    score = 0
    
    # GPA (30 points)
    if gpa >= 3.7:
        score += 30
    elif gpa >= 3.5:
        score += 25
    elif gpa >= 3.3:
        score += 20
    else:
        score += 15
    
    # English (20 points)
    ielts_score = ielts if ielts > 0 else (toefl / 120 * 9) if toefl > 0 else 0
    if ielts_score >= 7.5:
        score += 20
    elif ielts_score >= 7.0:
        score += 15
    elif ielts_score >= 6.5:
        score += 10
    else:
        score += 5
    
    # Work experience (20 points)
    if work_hours >= 2800:
        score += 20
    elif work_hours >= 1400:
        score += 15
    elif work_hours > 0:
        score += 10
    
    # Research (15 points)
    if has_research:
        score += 15
    
    # Publications (15 points)
    if has_publications:
        score += 15
    
    return score

def print_assessment(profile):
    """Print comprehensive assessment"""
    print("\n" + "="*80)
    print("AI MASTER'S PROGRAM ASSESSMENT")
    print("="*80)
    
    # Profile Summary
    print("\n📊 YOUR PROFILE SUMMARY")
    print("-" * 80)
    print(f"GPA: {profile['gpa']:.2f}/4.0")
    print(f"IELTS: {profile['ielts'] if profile['ielts'] > 0 else 'Not taken'}")
    print(f"TOEFL: {profile['toefl'] if profile['toefl'] > 0 else 'Not taken'}")
    print(f"Work Experience: {profile['work_years']} years ({profile['work_hours']} hours)")
    print(f"Research Experience: {'Yes' if profile['has_research'] else 'No'}")
    print(f"Publications: {'Yes' if profile['has_publications'] else 'No'}")
    print(f"Career Goal: {profile['career_location'].title()}")
    print(f"Can Return to Indonesia: {'Yes' if profile['can_return'] else 'No'}")
    
    # Competitiveness Score
    score = calculate_competitiveness_score(
        profile['gpa'], profile['ielts'], profile['toefl'],
        profile['work_hours'], profile['has_research'], profile['has_publications']
    )
    print(f"\n🎯 COMPETITIVENESS SCORE: {score}/100")
    if score >= 80:
        print("   ⭐ EXCELLENT - Competitive for top-tier programs")
    elif score >= 65:
        print("   ⭐ STRONG - Competitive for excellent programs")
    elif score >= 50:
        print("   ⭐ GOOD - Competitive for very good programs")
    else:
        print("   ⚠️  DEVELOPING - Consider strengthening profile")
    
    # University Tier
    tier, universities = assess_university_tier(
        profile['gpa'], profile['ielts'], profile['toefl'], profile['has_research']
    )
    print(f"\n🎓 TARGET UNIVERSITY TIER: {tier}")
    print(f"   Recommended: {', '.join(universities)}")
    
    # Chevening Eligibility
    if assess_chevening_eligibility(profile['work_hours']):
        print("\n✅ CHEVENING ELIGIBLE (2,800+ work hours)")
    else:
        needed = 2800 - profile['work_hours']
        print(f"\n❌ NOT CHEVENING ELIGIBLE (need {needed} more hours)")
    
    # Path Recommendation
    print("\n" + "="*80)
    print("🛤️  RECOMMENDED PATH")
    print("="*80)
    
    if profile['career_location'] == 'indonesia' or profile['can_return']:
        print("\n✅ PATH A: LPDP → Top University → Return to Indonesia")
        print("   This is your BEST option:")
        print("   • Fully funded (no debt)")
        print("   • High success rate for Indonesians")
        print("   • Access to elite universities")
        print("   • Must return to Indonesia for 2+ years")
        print("   • Can pursue international career AFTER fulfilling commitment")
    elif profile['career_location'] == 'international':
        print("\n✅ PATH B: International Career (No Return Requirement)")
        print("   Focus on these scholarships:")
        print("   • Erasmus Mundus EMAI (fully funded, EU career)")
        print("   • ETH ESOP (if GPA 3.7+, Switzerland career)")
        print("   • Spärck AI (UK career, verify return requirement)")
        print("   • DAAD (Germany career)")
    else:
        print("\n✅ PATH C: HYBRID STRATEGY")
        print("   Apply to BOTH paths:")
        print("   • PATH A: LPDP (return to Indonesia)")
        print("   • PATH B: Erasmus Mundus, ETH ESOP (international)")
        print("   • Decide when you receive offers")
    
    # Scholarship Recommendations
    print("\n" + "="*80)
    print("💰 RECOMMENDED SCHOLARSHIPS (Priority Order)")
    print("="*80)
    
    scholarships = recommend_scholarships(
        profile['career_location'], profile['can_return'],
        profile['work_hours'], profile['gpa'], profile['can_self_fund']
    )
    
    for i, schol in enumerate(scholarships, 1):
        print(f"\n{i}. {schol['name']} - Priority: {schol['priority']}")
        print(f"   Path: {schol['path']}")
        print(f"   Funding: {schol['funding']}")
        print(f"   Success Rate: {schol['success_rate']}")
        print(f"   Constraint: {schol['constraint']}")
        print(f"   ➡️  ACTION: {schol['action']}")
    
    # University Recommendations
    print("\n" + "="*80)
    print("🏛️  RECOMMENDED UNIVERSITY-SCHOLARSHIP COMBINATIONS")
    print("="*80)
    
    universities = recommend_universities(
        tier, profile['career_location'], profile['can_return'],
        profile['preferences']
    )
    
    for i, uni in enumerate(universities, 1):
        print(f"\n{i}. {uni['university']}")
        print(f"   Scholarship: {uni['scholarship']}")
        print(f"   Outcome: {uni['outcome']}")
        print(f"   Expected Salary: {uni['salary']}")
        print(f"   ✅ Pros: {uni['pros']}")
        print(f"   ⚠️  Cons: {uni['cons']}")
    
    # Action Items
    print("\n" + "="*80)
    print("📋 IMMEDIATE ACTION ITEMS")
    print("="*80)
    
    actions = []
    
    if profile['ielts'] < 7.0 and profile['toefl'] < 100:
        actions.append("🔴 URGENT: Book IELTS/TOEFL test (need 7.0+ / 100+)")
    
    if profile['career_location'] == 'indonesia' or profile['can_return']:
        actions.append("🔴 URGENT: Research LPDP exact return terms (lpdp.kemenkeu.go.id)")
        actions.append("🔴 URGENT: Start LPDP application (check deadline)")
    
    if profile['career_location'] == 'international' or profile['career_location'] == 'flexible':
        actions.append("🔴 URGENT: Apply for Spärck AI (Imperial deadline: March 4, 2026)")
        actions.append("🟡 HIGH: Apply for Erasmus Mundus EMAI (applications open)")
    
    actions.append("🟡 HIGH: Identify 3-4 recommendation letter writers")
    actions.append("🟡 HIGH: Create application deadline spreadsheet")
    actions.append("🟢 MEDIUM: Connect with Indonesian students at target universities")
    actions.append("🟢 MEDIUM: Draft preliminary personal statement")
    
    for action in actions:
        print(f"   {action}")
    
    # Warnings
    print("\n" + "="*80)
    print("⚠️  IMPORTANT WARNINGS")
    print("="*80)
    
    if profile['can_return'] and profile['career_location'] == 'international':
        print("\n⚠️  CONFLICTING GOALS DETECTED:")
        print("   You want international career but are willing to return to Indonesia.")
        print("   Decision needed:")
        print("   • If you take LPDP → MUST return to Indonesia 2+ years")
        print("   • If you want immediate international career → Don't take LPDP")
        print("   • Consider HYBRID: LPDP → return 2+ years → then international")
    
    if profile['gpa'] < 3.3:
        print("\n⚠️  GPA CONCERN:")
        print("   Your GPA may limit access to top-tier programs.")
        print("   Consider: Strong personal statement, research experience, work experience")
    
    if profile['ielts'] < 6.5 and profile['toefl'] < 90:
        print("\n⚠️  ENGLISH PROFICIENCY CONCERN:")
        print("   Most programs require IELTS 6.5-7.5 or TOEFL 90-100+")
        print("   Priority: Take test soon to know your baseline")
    
    if not profile['can_self_fund'] and profile['career_location'] == 'international':
        print("\n⚠️  FUNDING CONSTRAINT:")
        print("   International career path has fewer fully-funded options")
        print("   Focus on: Erasmus Mundus, ETH ESOP, DAAD, Spärck AI")
        print("   USA programs (MIT/Stanford) may require partial self-funding")
    
    print("\n" + "="*80)
    print("✅ ASSESSMENT COMPLETE")
    print("="*80)
    print("\nNext: Review recommendations and start with URGENT action items.")
    print("Good luck with your applications! 🚀")
    print()

def main():
    """Main assessment function"""
    print("="*80)
    print("AI MASTER'S PROGRAM ASSESSMENT TOOL")
    print("="*80)
    print("\nThis tool will assess your profile and recommend optimal paths.")
    print("Please answer the following questions:\n")
    
    profile = {}
    
    # Academic
    print("📚 ACADEMIC PROFILE")
    print("-" * 80)
    profile['gpa'] = get_float("GPA (on 4.0 scale)", 3.5)
    profile['ielts'] = get_float("IELTS score (0 if not taken)", 0)
    profile['toefl'] = get_float("TOEFL iBT score (0 if not taken)", 0)
    
    # Work Experience
    print("\n💼 WORK EXPERIENCE")
    print("-" * 80)
    profile['work_years'] = get_float("Years of work experience", 0)
    profile['work_hours'] = profile['work_years'] * 2000  # Approximate
    manual_hours = input(f"Total work hours [{profile['work_hours']:.0f}] (press Enter to use calculated): ").strip()
    if manual_hours:
        profile['work_hours'] = float(manual_hours)
    
    # Technical
    print("\n💻 TECHNICAL EXPERIENCE")
    print("-" * 80)
    profile['has_research'] = get_yes_no("Do you have research experience in AI/ML?")
    profile['has_publications'] = get_yes_no("Do you have publications or papers?")
    
    # Financial
    print("\n💰 FINANCIAL SITUATION")
    print("-" * 80)
    profile['can_self_fund'] = get_yes_no("Can you partially self-fund if needed?")
    
    # Career Goals
    print("\n🎯 CAREER GOALS")
    print("-" * 80)
    print("Where do you want to build your career after graduation?")
    print("1. Indonesia (willing to return)")
    print("2. International (USA/EU/UK/Singapore)")
    print("3. Flexible/Undecided")
    
    while True:
        choice = input("Enter choice (1/2/3): ").strip()
        if choice == '1':
            profile['career_location'] = 'indonesia'
            profile['can_return'] = True
            break
        elif choice == '2':
            profile['career_location'] = 'international'
            profile['can_return'] = False
            break
        elif choice == '3':
            profile['career_location'] = 'flexible'
            profile['can_return'] = get_yes_no("Are you willing to return to Indonesia for 2+ years if needed?")
            break
        print("Please enter 1, 2, or 3")
    
    # Preferences
    print("\n🌍 REGIONAL PREFERENCES")
    print("-" * 80)
    print("Which regions interest you? (enter comma-separated: usa,uk,europe,singapore)")
    pref_input = input("Preferences: ").strip().lower()
    profile['preferences'] = pref_input.split(',') if pref_input else []
    
    # Generate Assessment
    print_assessment(profile)

if __name__ == "__main__":
    main()
