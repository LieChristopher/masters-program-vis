import streamlit as st
import json
from pathlib import Path

st.set_page_config(page_title="AI Master's Assessment", page_icon="🎓", layout="wide")

# Load university data from JSON
@st.cache_data
def load_university_data():
    """Load university data from JSON file"""
    json_path = Path(__file__).parent / "university_data.json"
    with open(json_path, 'r') as f:
        return json.load(f)

# Load data
try:
    DATA = load_university_data()
    UNIVERSITIES = DATA['universities']
    SCHOLARSHIPS = DATA['scholarships']
    SCHOLARSHIP_AVAILABILITY = DATA['scholarship_availability']
    PATHS = DATA['paths']
    OPTIMAL_COMBINATIONS = DATA['optimal_combinations']
    DECISION_TREE = DATA['decision_tree']
    ACTION_ITEMS = DATA['action_items']
    WARNINGS = DATA['warnings']
except FileNotFoundError:
    st.error("⚠️ university_data.json not found. Please ensure the file exists in the same directory.")
    st.stop()
except json.JSONDecodeError:
    st.error("⚠️ Error reading university_data.json. Please check the file format.")
    st.stop()

def check_condition(condition, profile):
    """Check if a condition matches the profile"""
    for key, value in condition.items():
        if key not in profile:
            continue
        
        if isinstance(value, dict):
            # Handle comparison operators
            if 'lt' in value and profile[key] >= value['lt']:
                return False
            if 'gt' in value and profile[key] <= value['gt']:
                return False
            if 'eq' in value and profile[key] != value['eq']:
                return False
        elif isinstance(value, list):
            # Check if profile value is in list
            if profile[key] not in value:
                return False
        else:
            # Direct comparison
            if profile[key] != value:
                return False
    
    return True

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

def recommend_scholarships(career_location, can_return, work_hours, gpa, can_self_fund):
    recommendations = []
    
    if career_location == "Indonesia" or can_return:
        recommendations.append({
            "name": "LPDP",
            "priority": "🔴 HIGHEST",
            "path": "A (Indonesia Career)",
            "funding": "Full",
            "success_rate": "High for Indonesians",
            "constraint": "Must return to Indonesia 2+ years",
            "action": "Apply immediately - check lpdp.kemenkeu.go.id"
        })
        
        recommendations.append({
            "name": "Australia Awards",
            "priority": "🟡 HIGH",
            "path": "A (Indonesia Career)",
            "funding": "Full",
            "success_rate": "High for Indonesians",
            "constraint": "Must return to Indonesia",
            "action": "Applications open - australiaawardsindonesia.org"
        })
        
        if work_hours >= 2800:
            recommendations.append({
                "name": "Chevening",
                "priority": "🟡 HIGH",
                "path": "A (Indonesia Career)",
                "funding": "Full",
                "success_rate": "Medium",
                "constraint": "Must return to Indonesia 2+ years",
                "action": "Applications NOW OPEN - chevening.org/scholarship/indonesia"
            })
    
    if career_location == "International" or career_location == "Flexible":
        recommendations.append({
            "name": "Erasmus Mundus EMAI",
            "priority": "🔴 HIGHEST",
            "path": "B (International Career)",
            "funding": "Full (€1,400/month)",
            "success_rate": "Medium (15 scholarships)",
            "constraint": "None - EU career possible",
            "action": "Applications OPEN for 2026-2028 cohort"
        })
        
        if gpa >= 3.7:
            recommendations.append({
                "name": "ETH Zurich ESOP",
                "priority": "🟡 HIGH",
                "path": "B (International Career)",
                "funding": "Full (CHF 12,000/semester)",
                "success_rate": "Very Low (top performers globally)",
                "constraint": "None - Switzerland career possible",
                "action": "Apply with ETH admission - highly competitive"
            })
        
        recommendations.append({
            "name": "Spärck AI Scholarships",
            "priority": "🟡 HIGH",
            "path": "B (International Career)",
            "funding": "Full",
            "success_rate": "Unknown (NEW 2026)",
            "constraint": "Verify return requirement",
            "action": "Imperial deadline: March 4, 2026 - URGENT"
        })
        
        recommendations.append({
            "name": "DAAD",
            "priority": "🟢 MEDIUM",
            "path": "B (International Career)",
            "funding": "Full (€992/month)",
            "success_rate": "Medium",
            "constraint": "None - Germany career possible",
            "action": "Check daad-indonesia.org"
        })
        
        if can_self_fund:
            recommendations.append({
                "name": "University Merit (USA)",
                "priority": "🟢 MEDIUM",
                "path": "B (International Career)",
                "funding": "Partial",
                "success_rate": "Medium",
                "constraint": "None - USA career possible",
                "action": "Apply to MIT/Stanford/CMU"
            })
    
    return recommendations

def recommend_universities(tier, career_location, can_return):
    recommendations = []
    tier_num = 1 if "Tier 1" in tier else (2 if "Tier 2" in tier else 3)
    
    if career_location == "Indonesia" or can_return:
        if tier_num <= 2:
            recommendations.append({
                "university": "MIT / Stanford / CMU",
                "scholarship": "LPDP",
                "outcome": "Return to Indonesia (2+ years)",
                "salary": "Indonesian market",
                "pros": "Elite education, fully funded, LPDP network",
                "cons": "Must return, cannot work in USA immediately"
            })
            
            recommendations.append({
                "university": "Oxford / Cambridge",
                "scholarship": "LPDP or Chevening",
                "outcome": "Return to Indonesia (2+ years)",
                "salary": "Indonesian market",
                "pros": "Prestige, 1-year program, fully funded",
                "cons": "Must return to Indonesia"
            })
        
        recommendations.append({
            "university": "NUS Singapore",
            "scholarship": "LPDP",
            "outcome": "Return to Indonesia (2+ years)",
            "salary": "Indonesian market",
            "pros": "Regional relevance, close to Indonesia",
            "cons": "Must return to Indonesia"
        })
    
    if career_location == "International" or career_location == "Flexible":
        recommendations.append({
            "university": "ETH Zurich",
            "scholarship": "ETH ESOP",
            "outcome": "Switzerland career",
            "salary": "CHF 124,000 (~$138,000)",
            "pros": "Best value, high salary, no return requirement",
            "cons": "ESOP extremely competitive"
        })
        
        recommendations.append({
            "university": "TUM Munich",
            "scholarship": "DAAD",
            "outcome": "Germany career",
            "salary": "€66,000 (~$72,000)",
            "pros": "Fully funded, 18-month job search visa",
            "cons": "Lower salary than USA/Switzerland"
        })
        
        recommendations.append({
            "university": "Oxford / Cambridge / Imperial",
            "scholarship": "Spärck AI",
            "outcome": "UK career",
            "salary": "£60,000-£120,000",
            "pros": "Prestige, 1-year program, 2-year UK visa",
            "cons": "Return requirement unclear"
        })
        
        if tier_num <= 2:
            recommendations.append({
                "university": "MIT / Stanford / CMU",
                "scholarship": "University merit",
                "outcome": "USA career",
                "salary": "$140,000-$250,000+",
                "pros": "Highest salary, OPT 36 months",
                "cons": "Partial funding, H-1B visa lottery"
            })
        
        recommendations.append({
            "university": "Erasmus Mundus EMAI",
            "scholarship": "Erasmus Mundus",
            "outcome": "EU career",
            "salary": "€59,000-€66,000",
            "pros": "Fully funded, multi-country experience",
            "cons": "Consortium universities (not single elite)"
        })
    
    return recommendations

# Main App
st.title("🎓 AI Master's Program Assessment Tool")
st.markdown("*Get personalized recommendations for scholarships and universities*")

# Sidebar for inputs
with st.sidebar:
    st.header("📝 Your Profile")
    
    st.subheader("📚 Academic")
    gpa = st.slider("GPA (4.0 scale)", 2.0, 4.0, 3.5, 0.01)
    ielts = st.number_input("IELTS score (0 if not taken)", 0.0, 9.0, 0.0, 0.5)
    toefl = st.number_input("TOEFL iBT (0 if not taken)", 0, 120, 0, 5)
    
    st.subheader("💼 Work Experience")
    st.caption("Include all paid work: full-time, part-time, internships")
    
    work_years = st.number_input("Years of full-time work", 0.0, 20.0, 0.0, 0.5)
    internship_months = st.number_input("Internship months (if any)", 0, 60, 0, 1)
    part_time_years = st.number_input("Years of part-time work (if any)", 0.0, 10.0, 0.0, 0.5)
    
    # Calculate total hours
    # Full-time: 2000 hours/year
    # Internship: ~160 hours/month (assuming full-time internship)
    # Part-time: 1000 hours/year (assuming 20 hours/week)
    work_hours = int(work_years * 2000 + internship_months * 160 + part_time_years * 1000)
    
    st.info(f"**Total work hours: {work_hours:,}** (Chevening needs 2,800+)")
    
    if work_hours >= 2800:
        st.success("✅ Meets Chevening requirement!")
    elif work_hours > 0:
        needed = 2800 - work_hours
        st.warning(f"⚠️ Need {needed:,} more hours for Chevening ({needed/160:.1f} months)")
    else:
        st.info("💡 Fresh graduate? Focus on LPDP, Erasmus Mundus, DAAD")
    
    st.subheader("💻 Technical")
    st.caption("Research experience includes: thesis, research projects, lab work, papers")
    has_research = st.checkbox("Research experience in AI/ML/CS")
    st.caption("Examples: Bachelor's thesis, research assistant, independent projects")
    
    has_publications = st.checkbox("Publications or papers")
    st.caption("Examples: Conference papers, journal articles, arXiv preprints")
    
    st.subheader("💰 Financial")
    can_self_fund = st.checkbox("Can partially self-fund if needed")
    
    st.subheader("🎯 Career Goals")
    career_location = st.radio(
        "Career location preference:",
        ["Indonesia", "International", "Flexible"]
    )
    
    if career_location == "Flexible":
        can_return = st.checkbox("Willing to return to Indonesia for 2+ years?", value=True)
    else:
        can_return = career_location == "Indonesia"
    
    assess_button = st.button("🚀 Generate Assessment", type="primary")
    
    st.markdown("---")
    st.subheader("💵 Financial Calculator")
    st.caption("Compare costs of different university-scholarship combinations")
    
    # Country filter
    country_filter = st.selectbox(
        "🌍 Filter by Country",
        ["All Countries", "USA", "UK", "Switzerland", "Germany", "Singapore", "Europe (Multi-country)"]
    )

# Main content
if assess_button:
    # Store in session state so it persists
    st.session_state.assessed = True
    st.session_state.profile = {
        'gpa': gpa, 'ielts': ielts, 'toefl': toefl,
        'work_hours': work_hours, 'has_research': has_research,
        'has_publications': has_publications, 'can_self_fund': can_self_fund,
        'career_location': career_location, 'can_return': can_return
    }
    st.session_state.country_filter = country_filter

if 'assessed' in st.session_state and st.session_state.assessed:
    profile = st.session_state.profile
    # Calculate metrics
    score = calculate_competitiveness_score(
        profile['gpa'], profile['ielts'], profile['toefl'], 
        profile['work_hours'], profile['has_research'], profile['has_publications']
    )
    tier, universities = assess_university_tier(
        profile['gpa'], profile['ielts'], profile['toefl'], profile['has_research']
    )
    chevening_eligible = profile['work_hours'] >= 2800
    
    # Display results
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Competitiveness Score", f"{score}/100")
        if score >= 80:
            st.success("⭐ EXCELLENT")
        elif score >= 65:
            st.info("⭐ STRONG")
        elif score >= 50:
            st.warning("⭐ GOOD")
        else:
            st.error("⚠️ DEVELOPING")
    
    with col2:
        st.metric("University Tier", tier.split()[0] + " " + tier.split()[1])
        st.caption(", ".join(universities[:3]))
    
    with col3:
        if chevening_eligible:
            st.metric("Chevening", "✅ Eligible")
            st.caption(f"{profile['work_hours']:,} hours")
        else:
            needed = 2800 - profile['work_hours']
            st.metric("Chevening", "❌ Not Yet")
            st.caption(f"Need {needed:,}h more")
    
    # Path Recommendation
    st.header("🛤️ Recommended Path")
    
    # Determine recommended path from JSON
    recommended_path = None
    for path_key, path_data in PATHS.items():
        if 'recommended_if' in path_data:
            rec_if = path_data['recommended_if']
            if profile['career_location'] == rec_if.get('career_location') or \
               (profile['can_return'] == rec_if.get('can_return') and 'can_return' in rec_if):
                recommended_path = path_data
                break
    
    if not recommended_path:
        # Default to hybrid if flexible
        recommended_path = PATHS['C'] if profile['career_location'] == "Flexible" else PATHS['A']
    
    # Display path recommendation
    if recommended_path == PATHS['A']:
        st.success(f"✅ {recommended_path['name']}")
    elif recommended_path == PATHS['B']:
        st.info(f"✅ {recommended_path['name']}")
    else:
        st.warning(f"✅ {recommended_path['name']}")
    
    st.markdown(f"**{recommended_path['description']}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**✅ Pros:**")
        for pro in recommended_path['pros']:
            st.markdown(f"- {pro}")
    
    with col2:
        st.markdown("**⚠️ Cons:**")
        for con in recommended_path['cons']:
            st.markdown(f"- {con}")
    
    st.markdown(f"**Best for:** {', '.join(recommended_path['best_for'])}")
    st.markdown(f"**Focus scholarships:** {', '.join(recommended_path['scholarships'])}")
    
    # Scholarships
    st.header("💰 Recommended Scholarships")
    scholarships = recommend_scholarships(
        profile['career_location'], profile['can_return'], profile['work_hours'], 
        profile['gpa'], profile['can_self_fund']
    )
    
    for i, schol in enumerate(scholarships, 1):
        with st.expander(f"{i}. {schol['name']} - {schol['priority']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Path:** {schol['path']}")
                st.markdown(f"**Funding:** {schol['funding']}")
                st.markdown(f"**Success Rate:** {schol['success_rate']}")
            with col2:
                st.markdown(f"**Constraint:** {schol['constraint']}")
                st.markdown(f"**Action:** {schol['action']}")
    
    # Universities
    st.header("🏛️ Recommended University-Scholarship Combinations")
    unis = recommend_universities(tier, profile['career_location'], profile['can_return'])
    
    for i, uni in enumerate(unis, 1):
        with st.expander(f"{i}. {uni['university']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Scholarship:** {uni['scholarship']}")
                st.markdown(f"**Outcome:** {uni['outcome']}")
                st.markdown(f"**Expected Salary:** {uni['salary']}")
            with col2:
                st.markdown(f"**✅ Pros:** {uni['pros']}")
                st.markdown(f"**⚠️ Cons:** {uni['cons']}")
    
    # Action Items
    st.header("📋 Immediate Action Items")
    
    # Get action items from JSON based on profile
    for priority_level in ['urgent', 'high', 'medium']:
        for item in ACTION_ITEMS[priority_level]:
            if check_condition(item['condition'], profile):
                st.markdown(f"{item['priority']} {item['action']}")
    
    # Warnings
    st.header("⚠️ Important Warnings")
    
    # Get warnings from JSON based on profile
    for warning in WARNINGS:
        if check_condition(warning['condition'], profile):
            st.warning(f"**{warning['title']}:** {warning['message']}")
    
    st.success("✅ Assessment Complete! Good luck with your applications! 🚀")
    
    # Show optimal combinations from JSON
    st.header("⭐ Top Recommended Combinations")
    st.markdown("Based on research and analysis, here are the best university-scholarship combinations:")
    
    for combo in OPTIMAL_COMBINATIONS:
        with st.expander(f"{'⭐' * combo['rating']} {combo['university']} + {combo['scholarship']} → {combo['outcome']}"):
            st.markdown(f"**Path:** {combo['path']}")
            st.markdown(f"**Total Cost:** ${combo['total_cost']:,}")
            st.markdown(f"**Notes:** {combo['notes']}")

# Financial Calculator (always visible in sidebar after assessment)
with st.sidebar:
    if 'assessed' in st.session_state and st.session_state.assessed:
        st.markdown("---")
        # Let user select specific combinations
        
        # University options by country
        universities_by_country = {
            "All Countries": ["MIT", "Stanford", "Carnegie Mellon", "Oxford", "Cambridge", "Imperial", 
                             "ETH Zurich", "TUM Munich", "NUS Singapore", "Erasmus Mundus EMAI"],
            "USA": ["MIT", "Stanford", "Carnegie Mellon"],
            "UK": ["Oxford", "Cambridge", "Imperial"],
            "Switzerland": ["ETH Zurich"],
            "Germany": ["TUM Munich"],
            "Singapore": ["NUS Singapore"],
            "Europe (Multi-country)": ["Erasmus Mundus EMAI", "ETH Zurich", "TUM Munich"]
        }
        
        # Get country filter from session state or use default
        if 'country_filter' not in st.session_state:
            st.session_state.country_filter = "All Countries"
        
        # Filter universities based on country
        available_unis = universities_by_country[st.session_state.country_filter]
        
        selected_uni = st.selectbox(
            "🏛️ Select University",
            available_unis
        )
        
        scholarship_options = {
            "MIT": ["LPDP", "No Scholarship (Self-fund)", "University Merit (Partial)"],
            "Stanford": ["LPDP", "Knight Hennessy", "No Scholarship (Self-fund)"],
            "Carnegie Mellon": ["LPDP", "University Merit (Partial)", "No Scholarship (Self-fund)"],
            "Oxford": ["LPDP", "Chevening", "Spärck AI", "Commonwealth", "No Scholarship (Self-fund)"],
            "Cambridge": ["LPDP", "Chevening", "Gates Cambridge", "Commonwealth", "No Scholarship (Self-fund)"],
            "Imperial": ["LPDP", "Chevening", "Spärck AI", "Commonwealth", "No Scholarship (Self-fund)"],
            "ETH Zurich": ["LPDP", "ETH ESOP", "No Scholarship (Self-fund)"],
            "TUM Munich": ["LPDP", "DAAD", "No Scholarship (Self-fund)"],
            "NUS Singapore": ["LPDP", "NUS Scholarship", "No Scholarship (Self-fund)"],
            "Erasmus Mundus EMAI": ["Erasmus Mundus", "No Scholarship (Self-fund)"]
        }
        
        selected_scholarship = st.selectbox(
            "💰 Select Scholarship",
            scholarship_options[selected_uni]
        )

# Financial Calculator Results (in main area)
if 'assessed' in st.session_state and st.session_state.assessed:
    st.header("💵 Financial Calculator")
    st.markdown(f"**Selected Path:** {selected_uni} + {selected_scholarship}")
    
    # Cost data
    costs = {
        "MIT": {"tuition": 55000, "living": 25000, "duration": 2, "city": "Boston"},
        "Stanford": {"tuition": 60000, "living": 30000, "duration": 2, "city": "San Francisco"},
        "Carnegie Mellon": {"tuition": 50000, "living": 20000, "duration": 1.5, "city": "Pittsburgh"},
        "Oxford": {"tuition": 45000, "living": 20000, "duration": 1, "city": "Oxford"},
        "Cambridge": {"tuition": 45000, "living": 20000, "duration": 1, "city": "Cambridge"},
        "Imperial": {"tuition": 45000, "living": 25000, "duration": 1, "city": "London"},
        "ETH Zurich": {"tuition": 1500, "living": 22000, "duration": 2, "city": "Zurich"},
        "TUM Munich": {"tuition": 12000, "living": 15000, "duration": 2, "city": "Munich"},
        "NUS Singapore": {"tuition": 40000, "living": 15000, "duration": 1.5, "city": "Singapore"},
        "Erasmus Mundus EMAI": {"tuition": 0, "living": 18000, "duration": 2, "city": "Multiple EU"}
    }
    
    # Scholarship coverage
    scholarship_coverage = {
        "LPDP": {"tuition": 1.0, "living": 1.0, "flights": True, "return_required": True},
        "Chevening": {"tuition": 1.0, "living": 1.0, "flights": True, "return_required": True},
        "Australia Awards": {"tuition": 1.0, "living": 1.0, "flights": True, "return_required": True},
        "Erasmus Mundus": {"tuition": 1.0, "living": 1.0, "flights": True, "return_required": False},
        "ETH ESOP": {"tuition": 1.0, "living": 1.0, "flights": False, "return_required": False},
        "DAAD": {"tuition": 1.0, "living": 0.8, "flights": True, "return_required": False},
        "Spärck AI": {"tuition": 1.0, "living": 1.0, "flights": True, "return_required": "Unknown"},
        "Knight Hennessy": {"tuition": 1.0, "living": 1.0, "flights": True, "return_required": False},
        "Gates Cambridge": {"tuition": 1.0, "living": 1.0, "flights": True, "return_required": False},
        "Commonwealth": {"tuition": 1.0, "living": 1.0, "flights": True, "return_required": True},
        "NUS Scholarship": {"tuition": 0.5, "living": 0.3, "flights": False, "return_required": "Maybe"},
        "University Merit (Partial)": {"tuition": 0.5, "living": 0.0, "flights": False, "return_required": False},
        "No Scholarship (Self-fund)": {"tuition": 0.0, "living": 0.0, "flights": False, "return_required": False}
    }
    
    # Post-graduation salaries
    salaries = {
        "MIT": {"USA": 180000, "Indonesia": 30000},
        "Stanford": {"USA": 200000, "Indonesia": 30000},
        "Carnegie Mellon": {"USA": 170000, "Indonesia": 30000},
        "Oxford": {"UK": 80000, "Indonesia": 30000},
        "Cambridge": {"UK": 80000, "Indonesia": 30000},
        "Imperial": {"UK": 75000, "Indonesia": 30000},
        "ETH Zurich": {"Switzerland": 138000, "Indonesia": 30000},
        "TUM Munich": {"Germany": 72000, "Indonesia": 30000},
        "NUS Singapore": {"Singapore": 70000, "Indonesia": 30000},
        "Erasmus Mundus EMAI": {"EU": 65000, "Indonesia": 30000}
    }
    
    # Calculate costs
    uni_cost = costs[selected_uni]
    schol_cov = scholarship_coverage[selected_scholarship]
    
    total_tuition = uni_cost["tuition"] * uni_cost["duration"]
    total_living = uni_cost["living"] * uni_cost["duration"]
    flights = 2000 if schol_cov["flights"] else 2000  # Always need flights
    
    tuition_covered = total_tuition * schol_cov["tuition"]
    living_covered = total_living * schol_cov["living"]
    flights_covered = flights if schol_cov["flights"] else 0
    
    total_cost = total_tuition + total_living + flights
    total_covered = tuition_covered + living_covered + flights_covered
    out_of_pocket = total_cost - total_covered
    
    # Display results
    st.subheader("📊 Cost Breakdown")
    st.caption(f"Program duration: {uni_cost['duration']} years in {uni_cost['city']}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cost", f"${total_cost:,.0f}")
        st.caption(f"{uni_cost['duration']} years")
    
    with col2:
        st.metric("Scholarship Covers", f"${total_covered:,.0f}")
        st.caption(f"{(total_covered/total_cost*100):.0f}% covered")
    
    with col3:
        st.metric("Your Cost", f"${out_of_pocket:,.0f}")
        if out_of_pocket == 0:
            st.caption("✅ Fully funded!")
        else:
            st.caption(f"⚠️ Need to pay")
    
    with col4:
        return_req = schol_cov["return_required"]
        if return_req == True:
            st.metric("Return Required", "Yes")
            st.caption("2+ years Indonesia")
        elif return_req == False:
            st.metric("Return Required", "No")
            st.caption("✅ Free to work anywhere")
        else:
            st.metric("Return Required", "Unknown")
            st.caption("⚠️ Verify")
    
    # Detailed breakdown
    with st.expander("📋 Detailed Cost Breakdown"):
        breakdown_data = {
            "Item": ["Tuition", "Living Expenses", "Flights", "Total"],
            "Total Cost": [f"${total_tuition:,.0f}", f"${total_living:,.0f}", f"${flights:,.0f}", f"${total_cost:,.0f}"],
            "Scholarship Covers": [f"${tuition_covered:,.0f}", f"${living_covered:,.0f}", f"${flights_covered:,.0f}", f"${total_covered:,.0f}"],
            "You Pay": [f"${total_tuition-tuition_covered:,.0f}", f"${total_living-living_covered:,.0f}", f"${flights-flights_covered:,.0f}", f"${out_of_pocket:,.0f}"]
        }
        st.table(breakdown_data)
    
    # ROI Analysis
    st.subheader("💰 Return on Investment (ROI) Analysis")
    
    # Determine career location based on scholarship
    if schol_cov["return_required"] == True:
        career_location_calc = "Indonesia"
        years_indonesia = 2
    else:
        career_location_calc = st.radio(
            "Where will you work after graduation?",
            list(salaries[selected_uni].keys()),
            horizontal=True
        )
        years_indonesia = 0
    
    # Calculate ROI
    if schol_cov["return_required"] == True:
        # Must work in Indonesia for 2+ years
        indonesia_salary = salaries[selected_uni]["Indonesia"]
        indonesia_earnings = indonesia_salary * years_indonesia
        
        # Then can work internationally
        intl_location = list(salaries[selected_uni].keys())[0]
        intl_salary = salaries[selected_uni][intl_location]
        
        st.info(f"**Scenario: LPDP Path (Return Required)**")
        st.markdown(f"""
        - Years 1-2: Study at {selected_uni} (Cost: ${out_of_pocket:,.0f})
        - Years 3-4: Work in Indonesia (Earn: ${indonesia_earnings:,.0f} @ ${indonesia_salary:,.0f}/year)
        - Year 5+: Work in {intl_location} (Earn: ${intl_salary:,.0f}/year)
        """)
        
        # Calculate break-even
        net_cost = out_of_pocket - indonesia_earnings
        if net_cost > 0:
            years_to_breakeven = net_cost / intl_salary
            st.success(f"✅ Break-even in Year {2 + years_indonesia + years_to_breakeven:.1f} (after {years_to_breakeven:.1f} years in {intl_location})")
        else:
            st.success(f"✅ Already profitable after Indonesia commitment! Net gain: ${-net_cost:,.0f}")
        
        # 10-year projection
        years_intl = 10 - uni_cost["duration"] - years_indonesia
        total_earnings_10y = indonesia_earnings + (intl_salary * years_intl)
        net_10y = total_earnings_10y - out_of_pocket
        
        st.metric("10-Year Net Gain", f"${net_10y:,.0f}")
        st.caption(f"Total earnings: ${total_earnings_10y:,.0f} - Cost: ${out_of_pocket:,.0f}")
        
    else:
        # Can work anywhere immediately
        salary = salaries[selected_uni][career_location_calc]
        
        st.info(f"**Scenario: International Career Path**")
        st.markdown(f"""
        - Years 1-{uni_cost['duration']:.1f}: Study at {selected_uni} (Cost: ${out_of_pocket:,.0f})
        - Year {uni_cost['duration']+1:.0f}+: Work in {career_location_calc} (Earn: ${salary:,.0f}/year)
        """)
        
        # Calculate break-even
        if out_of_pocket > 0:
            years_to_breakeven = out_of_pocket / salary
            st.success(f"✅ Break-even in Year {uni_cost['duration'] + years_to_breakeven:.1f} (after {years_to_breakeven:.1f} years working)")
        else:
            st.success(f"✅ Fully funded! Start earning immediately after graduation")
        
        # 10-year projection
        years_working = 10 - uni_cost["duration"]
        total_earnings_10y = salary * years_working
        net_10y = total_earnings_10y - out_of_pocket
        
        st.metric("10-Year Net Gain", f"${net_10y:,.0f}")
        st.caption(f"Total earnings: ${total_earnings_10y:,.0f} - Cost: ${out_of_pocket:,.0f}")
    
    # Comparison with alternative
    st.subheader("📊 Compare with Alternative Path")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Your Selected Path:**")
        st.markdown(f"- {selected_uni} + {selected_scholarship}")
        st.markdown(f"- Out of pocket: ${out_of_pocket:,.0f}")
        st.markdown(f"- 10-year net: ${net_10y:,.0f}")
    
    with col2:
        # Show best alternative
        if schol_cov["return_required"] == True:
            st.markdown(f"**Alternative: International Career (No Return)**")
            st.markdown(f"- ETH Zurich + ETH ESOP")
            st.markdown(f"- Out of pocket: $2,000 (flights only)")
            st.markdown(f"- 10-year net: ~$1,100,000")
            st.markdown(f"- ⚠️ But ESOP very competitive")
        else:
            st.markdown(f"**Alternative: LPDP Path (Return Required)**")
            st.markdown(f"- {selected_uni} + LPDP")
            st.markdown(f"- Out of pocket: $0")
            st.markdown(f"- Must return to Indonesia 2+ years")
            st.markdown(f"- Can pursue international after")

else:
    st.info("👈 Fill in your profile in the sidebar and click 'Generate Assessment' to get personalized recommendations.")
    
    # Show some info
    st.markdown("""
    ## What This Tool Does
    
    This assessment tool analyzes your profile and provides:
    
    - **Competitiveness Score** (0-100) based on GPA, test scores, experience
    - **Target University Tier** (1-3) you can realistically apply to
    - **Recommended Path** (A: Indonesia, B: International, C: Hybrid)
    - **Scholarship Rankings** prioritized by success rate and fit
    - **University-Scholarship Combinations** optimized for your goals
    - **Action Items** with urgency levels
    - **Warnings** about potential issues
    
    ## Key Decisions
    
    The most important decision is: **Where do you want to build your career?**
    
    - **Indonesia:** LPDP is your best option (fully funded, high success rate, but must return 2+ years)
    - **International:** Focus on Erasmus Mundus, ETH ESOP, Spärck AI, DAAD (no return requirement)
    - **Flexible:** Apply to both and decide when you receive offers
    
    ## Work Experience Note
    
    **Chevening requires 2,800 work hours minimum** (roughly 1.4 years full-time)
    
    What counts:
    - ✅ Full-time work (2,000 hours/year)
    - ✅ Part-time work (pro-rated)
    - ✅ **Internships** (paid internships count!)
    - ✅ Freelance/consulting work
    - ❌ Unpaid volunteer work (doesn't count for Chevening)
    
    If you don't have 2,800 hours yet, focus on: **LPDP, Erasmus Mundus, DAAD, Australia Awards**
    
    ## Research Experience Note
    
    **Research experience includes:**
    - ✅ **Bachelor's thesis** (especially if AI/ML/CS related)
    - ✅ Research assistant positions
    - ✅ Independent research projects
    - ✅ Lab work or research internships
    - ✅ Capstone projects with research component
    - ✅ Kaggle competitions or similar
    
    **Publications include:**
    - ✅ Conference papers (peer-reviewed)
    - ✅ Journal articles
    - ✅ Workshop papers
    - ✅ arXiv preprints
    - ✅ Technical reports
    
    Even if unpublished, a strong thesis or research project counts as research experience!
    """)
