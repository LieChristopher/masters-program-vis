import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os
from datetime import datetime
from streamlit_mermaid import st_mermaid
from utils.data_loader import load_data
from utils.assessment import calculate_competitiveness_score, assess_university_tier, check_condition

st.set_page_config(page_title="AI Master's Assessment", page_icon="🎓", layout="wide")

# Profile management functions
def load_profile():
    """Load profile from my_profile.json"""
    try:
        if os.path.exists('my_profile.json'):
            with open('my_profile.json', 'r') as f:
                return json.load(f)
    except:
        pass
    return None

def save_profile(profile_data):
    """Save profile to my_profile.json"""
    try:
        profile_data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
        with open('my_profile.json', 'w') as f:
            json.dump(profile_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving profile: {e}")
        return False

# Load data
try:
    DATA = load_data()
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
except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")
    st.stop()

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
    
    # Profile Load/Save Section
    st.subheader("💾 Profile Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📂 Load Profile", use_container_width=True):
            loaded_profile = load_profile()
            if loaded_profile:
                # Store the full nested structure for form initialization
                st.session_state['profile'] = loaded_profile
                # Also create flat structure for assessment if it exists
                if 'profile' in loaded_profile:
                    p = loaded_profile['profile']
                    st.session_state.profile = {
                        'gpa': p.get('academic', {}).get('undergraduate', {}).get('gpa', 3.5),
                        'ielts': p.get('language', {}).get('english', {}).get('ielts', 0.0),
                        'toefl': p.get('language', {}).get('english', {}).get('toefl_ibt', 0),
                        'work_hours': p.get('work_experience', {}).get('total_hours', 0),
                        'has_research': p.get('research', {}).get('has_research_experience', False),
                        'has_publications': p.get('research', {}).get('has_publications', False),
                        'can_self_fund': p.get('financial', {}).get('can_self_fund', False),
                        'self_fund_budget': p.get('financial', {}).get('self_funding_budget_usd', 0),
                        'career_location': p.get('career_goals', {}).get('primary_path', 'Flexible'),
                        'can_return': p.get('career_goals', {}).get('willing_to_return_indonesia', True)
                    }
                    st.session_state.assessed = True
                st.success("✅ Profile loaded!")
                st.rerun()
            else:
                st.warning("No saved profile found")
    
    with col2:
        if st.button("💾 Save Profile", use_container_width=True):
            # Create profile from current inputs
            profile_data = {
                "profile": {
                    "personal": {
                        "name": st.session_state.get('name', ''),
                        "age": st.session_state.get('age', None),
                        "nationality": "Indonesian",
                        "current_location": ""
                    },
                    "academic": {
                        "undergraduate": {
                            "gpa": st.session_state.get('gpa', 3.5),
                            "gpa_scale": 4.0
                        }
                    },
                    "language": {
                        "english": {
                            "ielts": st.session_state.get('ielts', 0.0),
                            "toefl_ibt": st.session_state.get('toefl', 0)
                        }
                    },
                    "work_experience": {
                        "years_of_experience": st.session_state.get('work_years', 0.0),
                        "total_hours": st.session_state.get('work_hours', 0)
                    },
                    "career_goals": {
                        "primary_path": st.session_state.get('career_location', 'flexible'),
                        "willing_to_return_indonesia": st.session_state.get('can_return', True)
                    },
                    "financial": {
                        "self_funding_budget_usd": st.session_state.get('self_fund_budget', 0),
                        "can_self_fund": st.session_state.get('can_self_fund', False)
                    }
                },
                "metadata": {
                    "version": "1.0",
                    "created_date": datetime.now().strftime('%Y-%m-%d'),
                    "last_updated": datetime.now().strftime('%Y-%m-%d')
                }
            }
            if save_profile(profile_data):
                st.success("✅ Profile saved!")
    
    st.divider()
    
    # Load profile data if exists
    if 'profile' not in st.session_state:
        st.session_state['profile'] = load_profile()
    
    # Initialize from loaded profile if available
    loaded = st.session_state.get('profile')
    
    st.subheader("📚 Academic")
    gpa = st.slider("GPA (4.0 scale)", 2.0, 4.0, 
                    loaded.get('profile', {}).get('academic', {}).get('undergraduate', {}).get('gpa', 3.5) if loaded else 3.5,
                    0.1, key='gpa', help="Your undergraduate GPA converted to 4.0 scale")
    ielts = st.number_input("IELTS score (0 if not taken)", 0.0, 9.0,
                            loaded.get('profile', {}).get('language', {}).get('english', {}).get('ielts', 0.0) if loaded else 0.0,
                            0.5, key='ielts', help="Overall band score. Most programs need 6.5-7.5")
    toefl = st.number_input("TOEFL iBT (0 if not taken)", 0, 120,
                            loaded.get('profile', {}).get('language', {}).get('english', {}).get('toefl_ibt', 0) if loaded else 0,
                            5, key='toefl', help="Total score. Most programs need 90-100")
    
    st.subheader("💼 Work Experience")
    st.caption("Include all paid work: full-time, part-time, internships")
    
    work_years = st.number_input("Years of full-time work", min_value=0.0, max_value=20.0,
                                 value=loaded.get('profile', {}).get('work_experience', {}).get('years_of_experience', 0.0) if loaded else 0.0,
                                 step=0.5, key='work_years', help="Full-time employment (2000 hours/year)")
    internship_months = st.number_input("Internship months (if any)", 0, 60, 0, 1, key='internship_months',
                                       help="Paid internships (160 hours/month)")
    part_time_years = st.number_input("Years of part-time work (if any)", 0.0, 10.0, 0.0, 0.5, key='part_time_years',
                                     help="Part-time jobs (1000 hours/year)")
    
    work_hours = int(work_years * 2000 + internship_months * 160 + part_time_years * 1000)
    st.session_state['work_hours'] = work_hours
    
    st.info(f"**Total work hours: {work_hours:,}** (Chevening needs 2,800+)")
    
    if work_hours >= 2800:
        st.success("✅ Meets Chevening requirement!")
    elif work_hours > 0:
        needed = 2800 - work_hours
        st.warning(f"⚠️ Need {needed:,} more hours ({needed/160:.1f} months)")
    else:
        st.info("💡 Fresh graduate? Focus on LPDP, Erasmus Mundus, DAAD")
    
    st.subheader("💻 Technical")
    st.caption("Research: thesis, projects, lab work")
    has_research = st.checkbox("Research experience in AI/ML/CS", help="Bachelor's thesis, research projects, lab work, or publications")
    
    has_publications = st.checkbox("Publications or papers", help="Conference papers, journal articles, preprints, or technical reports")
    
    st.subheader("💰 Financial")
    can_self_fund = st.checkbox("Can partially self-fund if needed", 
                                value=loaded.get('profile', {}).get('financial', {}).get('can_self_fund', False) if loaded else False,
                                key='can_self_fund',
                                help="Can you contribute your own money if scholarships don't cover everything?")
    
    if can_self_fund:
        self_fund_budget = st.slider(
            "How much can you contribute? (USD)",
            min_value=0,
            max_value=200000,
            value=loaded.get('profile', {}).get('financial', {}).get('self_funding_budget_usd', 50000) if loaded and loaded.get('profile', {}).get('financial', {}).get('can_self_fund') else 50000,
            step=10000,
            key='self_fund_budget',
            help="Total amount you can contribute for the entire program (tuition + living + flights)"
        )
        st.caption(f"💵 Budget: ${self_fund_budget:,}")
    else:
        self_fund_budget = 0
        st.session_state['self_fund_budget'] = 0
    
    st.subheader("🎯 Career Goals")
    career_location = st.radio(
        "Career location preference:",
        ["Indonesia", "International", "Flexible"],
        index=["Indonesia", "International", "Flexible"].index(
            loaded.get('profile', {}).get('career_goals', {}).get('primary_path', 'Flexible') if loaded and loaded.get('profile', {}).get('career_goals', {}).get('primary_path') in ["Indonesia", "International", "Flexible"] else "Flexible"
        ) if loaded else 2,
        key='career_location',
        help="Where do you want to work after graduation? This affects scholarship and university recommendations."
    )
    
    if career_location == "Flexible":
        can_return = st.checkbox("Willing to return to Indonesia for 2+ years?",
                                value=loaded.get('profile', {}).get('career_goals', {}).get('willing_to_return_indonesia', True) if loaded else True,
                                key='can_return',
                                help="LPDP and similar scholarships require you to return to Indonesia for 2+ years after graduation")
    else:
        can_return = career_location == "Indonesia"
        st.session_state['can_return'] = can_return
    
    assess_button = st.button("🚀 Generate Assessment", type="primary")
    
    st.markdown("---")
    st.subheader("💵 Financial Calculator")
    st.info("""
    **What is this?** Calculate the exact cost of any university-scholarship combination.
    
    **How to use:**
    1. Complete your profile above
    2. Click "Generate Assessment"
    3. Select a university and scholarship below
    4. See detailed cost breakdown in the main area
    """)
    
    region_filter = st.selectbox(
        "🌍 Filter by Region",
        ["All Regions", "North America", "Europe", "Asia", "Middle East"],
        help="Narrow down universities by geographic region"
    )
    
    if region_filter != "All Regions":
        country_filter = st.selectbox(
            "🏙️ Filter by Country/City",
            ["All"] + list(set([v.get('city', v['country']) for v in UNIVERSITIES.values() if v.get('region') == region_filter]))
        )
    else:
        country_filter = "All"

# Main content
if assess_button:
    st.session_state.assessed = True
    st.session_state.profile = {
        'gpa': gpa, 'ielts': ielts, 'toefl': toefl,
        'work_hours': work_hours, 'has_research': has_research,
        'has_publications': has_publications, 'can_self_fund': can_self_fund,
        'self_fund_budget': self_fund_budget if can_self_fund else 0,
        'career_location': career_location, 'can_return': can_return
    }
    st.session_state.region_filter = region_filter
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
    
    # Determine recommended path
    recommended_path = None
    recommended_path_key = None
    for path_key, path_data in PATHS.items():
        if 'recommended_if' in path_data:
            rec_if = path_data['recommended_if']
            if profile['career_location'] == rec_if.get('career_location') or \
               (profile['can_return'] == rec_if.get('can_return') and 'can_return' in rec_if):
                recommended_path = path_data
                recommended_path_key = path_key
                break
    
    if not recommended_path:
        recommended_path_key = 'C' if profile['career_location'] == "Flexible" else 'A'
        recommended_path = PATHS[recommended_path_key]
    
    # ============================================================================
    # TOP SECTION: KEY METRICS & RECOMMENDED PATH
    # ============================================================================
    
    st.title("🎯 Your AI Master's Assessment")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Competitiveness", f"{score}/100")
        if score >= 80:
            st.success("⭐ EXCELLENT")
        elif score >= 65:
            st.info("⭐ STRONG")
        elif score >= 50:
            st.warning("⭐ GOOD")
        else:
            st.error("⚠️ DEVELOPING")
    
    with col2:
        st.metric("Target Tier", tier.split()[0] + " " + tier.split()[1])
        st.caption(", ".join(universities[:2]))
    
    with col3:
        if chevening_eligible:
            st.metric("Chevening", "✅ Eligible")
            st.caption(f"{profile['work_hours']:,} hours")
        else:
            needed = 2800 - profile['work_hours']
            st.metric("Chevening", "❌ Not Yet")
            st.caption(f"Need {needed:,}h")
    
    with col4:
        st.metric("Recommended Path", f"PATH {recommended_path_key}")
        st.caption(recommended_path['name'].split('(')[0].strip())
    
    # Recommended Path Highlight
    st.markdown("---")
    
    if recommended_path_key == 'A':
        st.success(f"### ✅ {recommended_path['name']}")
    elif recommended_path_key == 'B':
        st.info(f"### ✅ {recommended_path['name']}")
    else:
        st.warning(f"### ✅ {recommended_path['name']}")
    
    st.markdown(f"**{recommended_path['description']}**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**✅ Pros:**")
        for pro in recommended_path['pros'][:3]:
            st.markdown(f"- {pro}")
    with col2:
        st.markdown("**⚠️ Cons:**")
        for con in recommended_path['cons'][:3]:
            st.markdown(f"- {con}")
    with col3:
        st.markdown("**🎯 Best For:**")
        for item in recommended_path['best_for']:
            st.markdown(f"- {item}")
    
    st.markdown(f"**Focus Scholarships:** {', '.join(recommended_path['scholarships'])}")
    
    # ============================================================================
    # TABS: DETAILED INFORMATION
    # ============================================================================
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "💰 Scholarships", 
        "🏛️ Universities", 
        "📊 Comparison",
        "🌳 Decision Tree",
        "📋 Action Items",
        "⚠️ Warnings",
        "⭐ Top Picks"
    ])
    
    # TAB 1: SCHOLARSHIPS
    with tab1:
        st.header("💰 Recommended Scholarships")
        scholarships = recommend_scholarships(
            profile['career_location'], profile['can_return'], profile['work_hours'], 
            profile['gpa'], profile['can_self_fund']
        )
        
        for i, schol in enumerate(scholarships, 1):
            with st.expander(f"{i}. {schol['name']} - {schol['priority']}", expanded=(i<=3)):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Path:** {schol['path']}")
                    st.markdown(f"**Funding:** {schol['funding']}")
                    st.markdown(f"**Success Rate:** {schol['success_rate']}")
                with col2:
                    st.markdown(f"**Constraint:** {schol['constraint']}")
                    st.markdown(f"**Action:** {schol['action']}")
    
    # TAB 2: UNIVERSITIES
    with tab2:
        st.header("🏛️ Recommended University-Scholarship Combinations")
        
        # Add region filter
        col1, col2 = st.columns([1, 3])
        with col1:
            view_region = st.selectbox("Filter by region:", ["All", "North America", "Europe", "China", "Asia-Pacific"])
        
        unis = recommend_universities(tier, profile['career_location'], profile['can_return'])
        
        for i, uni in enumerate(unis, 1):
            with st.expander(f"{i}. {uni['university']}", expanded=(i<=3)):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Scholarship:** {uni['scholarship']}")
                    st.markdown(f"**Outcome:** {uni['outcome']}")
                    st.markdown(f"**Expected Salary:** {uni['salary']}")
                with col2:
                    st.markdown(f"**✅ Pros:** {uni['pros']}")
                    st.markdown(f"**⚠️ Cons:** {uni['cons']}")
        
        # Add detailed university comparison table
        st.markdown("---")
        st.subheader("📊 Detailed University Comparison")
        
        # Filter universities by region if selected
        filtered_unis = UNIVERSITIES
        if view_region != "All":
            filtered_unis = {k: v for k, v in UNIVERSITIES.items() if v.get('region') == view_region}
        
        # Create comparison table
        comparison_data = []
        for uni_key, uni_data in filtered_unis.items():
            career_attrs = uni_data.get('career_attributes', {})
            program_focus = uni_data.get('program_focus', {})
            
            # Get salary for relevant country
            salary_country = uni_data['country']
            if salary_country == "Europe":
                salary_country = "EU"
            salary = uni_data['salaries'].get(salary_country, uni_data['salaries'].get(list(uni_data['salaries'].keys())[0]))
            
            comparison_data.append({
                "University": uni_data['name'],
                "Region": uni_data.get('region', 'N/A'),
                "City": uni_data['city'],
                "Tier": uni_data['tier'],
                "Duration": f"{uni_data['duration_years']}y",
                "Total Cost": f"${(uni_data['tuition_per_year'] + uni_data['living_per_year']) * uni_data['duration_years']:,.0f}",
                "Salary": f"${salary:,.0f}",
                "Research": program_focus.get('research_intensity', 'N/A'),
                "Industry": program_focus.get('industry_connections', 'N/A'),
                "Visa": career_attrs.get('visa_difficulty', 'N/A'),
                "Best For": program_focus.get('best_for', 'N/A')
            })
        
        st.dataframe(comparison_data, width='stretch')
        
        # Add career attributes legend
        with st.expander("ℹ️ Career Attributes Explained"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Research Intensity:**
                - Very High: Heavy thesis, publications expected
                - High: Significant research component
                - Medium: Balanced research and coursework
                - Low: Primarily coursework-based
                """)
                st.markdown("""
                **Industry Connections:**
                - Excellent: Strong partnerships, many internships
                - Strong: Good industry ties
                - Moderate: Some industry engagement
                - Limited: Primarily academic focus
                """)
                st.markdown("""
                **Visa Difficulty:**
                - Easy: Clear path, 3-5 years to PR
                - Medium: Possible but requires effort
                - Hard: Difficult, long timeline
                - Very Hard: H-1B lottery or near impossible
                """)
            with col2:
                st.markdown("""
                **Program Best For:**
                - PhD pipeline: Strong research, publications
                - Industry: Applied skills, internships
                - Flexible: Both research and industry options
                """)
                st.markdown("""
                **Thesis Requirement:**
                - Required: Must complete research thesis
                - Optional: Choose thesis or capstone/project
                - Capstone: Industry project instead of thesis
                """)
                st.markdown("""
                **Choosing Research vs Industry:**
                - Want PhD? → Choose "Very High" or "High" research
                - Want job immediately? → Choose "Excellent" industry connections
                - Unsure? → Choose programs with "Optional" thesis
                """)
        
        # China city comparison if viewing China
        if view_region == "China" or view_region == "All":
            st.markdown("---")
            st.subheader("🇨🇳 China: City-Level Comparison")
            
            china_unis = {k: v for k, v in UNIVERSITIES.items() if v.get('region') == 'China'}
            
            china_comparison = []
            for uni_key, uni_data in china_unis.items():
                city_details = uni_data.get('city_details', {})
                china_comparison.append({
                    "University": uni_data['name'],
                    "City": uni_data['city'],
                    "City Tier": uni_data.get('city_tier', 'N/A'),
                    "Living Cost/Year": f"${uni_data['living_per_year']:,.0f}",
                    "AI Salary": f"${uni_data['salaries'].get('China', 0):,.0f}",
                    "Top Companies": ", ".join(city_details.get('companies', [])[:2]) if city_details else "N/A",
                    "Key Advantage": city_details.get('pros', ['N/A'])[0] if city_details else "N/A"
                })
            
            st.dataframe(china_comparison, width='stretch')
            
            st.info("""
            💡 **China City Tiers:**
            - **Tier 1** (Beijing, Shanghai, Shenzhen): Most expensive, best jobs, most competitive
            - **New Tier 1** (Hangzhou, Nanjing): 30-40% cheaper, strong tech hubs, good quality of life
            - **Tier 2** (Xi'an, Hefei): Most affordable, emerging opportunities
            
            **Zhejiang University in Hangzhou** offers the best value: Top AI program (tied #3 with CMU) at 30% lower cost than Beijing.
            """)
    
    # TAB 3: VISUAL COMPARISON
    with tab3:
        st.header("📊 University Comparison")
        st.markdown("**Compare all universities side-by-side** - Click column headers to sort")
        
        # Prepare comparison data
        comparison_data = []
        for uni_key, uni_data in UNIVERSITIES.items():
            career_attrs = uni_data.get('career_attributes', {})
            program_focus = uni_data.get('program_focus', {})
            
            # Get salary
            salary_country = uni_data['country']
            if salary_country == "Europe":
                salary_country = "EU"
            salary = uni_data['salaries'].get(salary_country, uni_data['salaries'].get(list(uni_data['salaries'].keys())[0]))
            
            # Calculate metrics
            total_cost = (uni_data['tuition_per_year'] + uni_data['living_per_year']) * uni_data['duration_years']
            roi = salary - total_cost
            num_scholarships = len(SCHOLARSHIP_AVAILABILITY.get(uni_key, []))
            
            # Check affordability if user has budget
            affordable = "N/A"
            if 'assessed' in st.session_state and st.session_state.assessed:
                budget = st.session_state.profile.get('self_fund_budget', 0)
                if budget > 0:
                    if total_cost <= budget:
                        affordable = "✅ Fully Affordable"
                    elif total_cost <= budget * 1.5:
                        affordable = "⚠️ Stretch Budget"
                    else:
                        affordable = "❌ Over Budget"
                else:
                    affordable = "Need Scholarship"
            
            comparison_data.append({
                "University": uni_data['name'],
                "Region": uni_data.get('region', 'N/A'),
                "Tier": uni_data['tier'],
                "Cost": total_cost,
                "Affordable": affordable,
                "Salary": salary,
                "ROI": roi,
                "Duration": f"{uni_data['duration_years']}y",
                "Scholarships": num_scholarships,
                "Research": program_focus.get('research_intensity', 'N/A'),
                "Industry": program_focus.get('industry_connections', 'N/A'),
                "Visa": career_attrs.get('visa_difficulty', 'N/A'),
                "Best For": program_focus.get('best_for', 'N/A')
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        
        # Add filters
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            region_filter = st.multiselect("Filter by Region", options=sorted(df_comparison['Region'].unique().tolist()))
        with col2:
            tier_filter = st.multiselect("Filter by Tier", options=[1, 2, 3])
        with col3:
            research_filter = st.multiselect("Filter by Research", options=sorted(df_comparison['Research'].unique().tolist()))
        with col4:
            visa_filter = st.multiselect("Filter by Visa", options=sorted(df_comparison['Visa'].unique().tolist()))
        
        # Apply filters
        filtered_df = df_comparison.copy()
        if region_filter:
            filtered_df = filtered_df[filtered_df['Region'].isin(region_filter)]
        if tier_filter:
            filtered_df = filtered_df[filtered_df['Tier'].isin(tier_filter)]
        if research_filter:
            filtered_df = filtered_df[filtered_df['Research'].isin(research_filter)]
        if visa_filter:
            filtered_df = filtered_df[filtered_df['Visa'].isin(visa_filter)]
        
        # Format for display
        display_df = filtered_df.copy()
        display_df['Cost'] = display_df['Cost'].apply(lambda x: f"${x:,.0f}")
        display_df['Salary'] = display_df['Salary'].apply(lambda x: f"${x:,.0f}")
        display_df['ROI'] = display_df['ROI'].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(
            display_df,
            width='stretch',
            hide_index=True,
            height=600
        )
        
        st.markdown("---")
        
        # Budget-based insights
        if 'assessed' in st.session_state and st.session_state.assessed:
            budget = st.session_state.profile.get('self_fund_budget', 0)
            if budget > 0:
                st.subheader(f"💵 Budget Analysis (Your Budget: ${budget:,})")
                
                affordable_unis = df_comparison[df_comparison['Cost'] <= budget]
                stretch_unis = df_comparison[(df_comparison['Cost'] > budget) & (df_comparison['Cost'] <= budget * 1.5)]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Fully Affordable", len(affordable_unis))
                    if len(affordable_unis) > 0:
                        st.caption("Within your budget")
                        for _, row in affordable_unis.nsmallest(3, 'Cost').iterrows():
                            st.write(f"✅ {row['University']} (${row['Cost']:,.0f})")
                
                with col2:
                    st.metric("Stretch Budget", len(stretch_unis))
                    if len(stretch_unis) > 0:
                        st.caption("Up to 50% over budget")
                        for _, row in stretch_unis.nsmallest(3, 'Cost').iterrows():
                            st.write(f"⚠️ {row['University']} (${row['Cost']:,.0f})")
                
                with col3:
                    over_budget = len(df_comparison) - len(affordable_unis) - len(stretch_unis)
                    st.metric("Over Budget", over_budget)
                    st.caption("Need scholarships")
                
                if len(affordable_unis) > 0:
                    st.success(f"💡 **Good news!** You can afford {len(affordable_unis)} universities without scholarships. Consider applying to scholarship programs to reduce costs further.")
                elif len(stretch_unis) > 0:
                    st.warning(f"⚠️ **Stretch budget:** {len(stretch_unis)} universities are within 50% of your budget. You'll need partial scholarships or additional funding.")
                else:
                    st.error(f"❌ **Scholarships required:** All universities exceed your budget. Focus on fully-funded scholarships like LPDP, Erasmus Mundus, or DAAD.")
        
        st.markdown("---")
        
        # Quick insights
        st.subheader("🎯 Quick Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 💰 Best Value")
            best_value = df_comparison.nsmallest(3, 'Cost')
            for _, row in best_value.iterrows():
                if row['Tier'] == 1:
                    st.success(f"**{row['University']}** - Tier {row['Tier']}, ${row['Cost']:,.0f}")
                else:
                    st.info(f"**{row['University']}** - Tier {row['Tier']}, ${row['Cost']:,.0f}")
        
        with col2:
            st.markdown("### 💵 Highest ROI")
            best_roi = df_comparison.nlargest(3, 'ROI')
            for _, row in best_roi.iterrows():
                st.success(f"**{row['University']}** - ${row['ROI']:,.0f}")
        
        with col3:
            st.markdown("### ✅ Easiest Visa")
            easy_visa = df_comparison[df_comparison['Visa'] == 'Easy']
            if len(easy_visa) > 0:
                for _, row in easy_visa.iterrows():
                    st.success(f"**{row['University']}** - {row['Region']}, ${row['Salary']:,.0f}")
            else:
                medium_visa = df_comparison[df_comparison['Visa'] == 'Medium'].nlargest(3, 'Salary')
                for _, row in medium_visa.iterrows():
                    st.info(f"**{row['University']}** - Medium visa, ${row['Salary']:,.0f}")
        
        st.markdown("---")
        
        # Decision helper
        st.subheader("🤔 Decision Helper")
        
        decision_col1, decision_col2 = st.columns(2)
        
        with decision_col1:
            st.markdown("### If you want...")
            
            st.markdown("**🎓 PhD Pipeline:**")
            phd_unis = df_comparison[df_comparison['Research'].isin(['Very High', 'High'])].nlargest(3, 'Tier')
            for _, row in phd_unis.iterrows():
                st.write(f"• {row['University']} ({row['Research']} research)")
            
            st.markdown("**💼 Job Immediately:**")
            job_unis = df_comparison[df_comparison['Industry'] == 'Excellent'].nlargest(3, 'Salary')
            for _, row in job_unis.iterrows():
                st.write(f"• {row['University']} (${row['Salary']:,.0f} salary)")
            
            st.markdown("**💰 Best Value:**")
            value_unis = df_comparison[df_comparison['Tier'] == 1].nsmallest(3, 'Cost')
            for _, row in value_unis.iterrows():
                st.write(f"• {row['University']} (${row['Cost']:,.0f} total)")
        
        with decision_col2:
            st.markdown("### Consider...")
            
            st.markdown("**🌍 Easy Immigration:**")
            easy_unis = df_comparison[df_comparison['Visa'].isin(['Easy', 'Medium'])].nlargest(3, 'Salary')
            for _, row in easy_unis.iterrows():
                st.write(f"• {row['University']} ({row['Visa']} visa, ${row['Salary']:,.0f})")
            
            st.markdown("**🔬 Hybrid (PhD or Industry):**")
            hybrid_unis = df_comparison[
                (df_comparison['Research'].isin(['High', 'Very High'])) & 
                (df_comparison['Industry'].isin(['Excellent', 'Strong']))
            ].head(3)
            for _, row in hybrid_unis.iterrows():
                st.write(f"• {row['University']} ({row['Research']} research, {row['Industry']} industry)")
            
            st.markdown("**💵 Highest Salary:**")
            salary_unis = df_comparison.nlargest(3, 'Salary')
            for _, row in salary_unis.iterrows():
                st.write(f"• {row['University']} (${row['Salary']:,.0f}, {row['Visa']} visa)")
        
        st.info("""
        💡 **How to use this comparison:**
        1. **Use filters** above to narrow down by region, tier, research focus, or visa difficulty
        2. **Click column headers** to sort by any metric (cost, salary, ROI, etc.)
        3. **Check Quick Insights** for top picks in each category
        4. **Use Decision Helper** to match universities to your goals
        5. **Shortlist 3-5 universities** then deep dive in other tabs
        """)
    
    # TAB 4: DECISION TREE
    with tab4:
        st.header("🌳 Decision Tree - Your Path Highlighted")
        st.markdown("**The flowchart below highlights your recommended path based on your profile**")
        
        if 'assessed' in st.session_state and st.session_state.assessed:
            profile = st.session_state.profile
            
            # Determine user's path through the tree
            career_loc = profile['career_location']
            can_return = profile['can_return']
            can_self_fund = profile['can_self_fund']
            
            # Determine which nodes to highlight
            if career_loc == "Indonesia" and can_return:
                path_nodes = ["start", "indonesia", "can_return_yes", "path_a"]
                path_result = "PATH A"
            elif career_loc == "Indonesia" and not can_return:
                path_nodes = ["start", "indonesia", "can_return_no", "path_b_europe"]
                path_result = "PATH B"
            elif career_loc == "International" and can_self_fund:
                path_nodes = ["start", "international", "can_fund_yes", "path_b_usa"]
                path_result = "PATH B (USA)"
            elif career_loc == "International" and not can_self_fund:
                path_nodes = ["start", "international", "can_fund_no", "path_b_europe"]
                path_result = "PATH B (Europe)"
            elif career_loc == "Flexible" and can_return:
                path_nodes = ["start", "flexible", "willing_return_yes", "path_c"]
                path_result = "PATH C"
            else:  # Flexible but not willing to return
                path_nodes = ["start", "flexible", "willing_return_no", "path_b_europe"]
                path_result = "PATH B"
            
            # Debug logging
            st.write(f"DEBUG: career_loc={career_loc}, can_return={can_return}, can_self_fund={can_self_fund}")
            st.write(f"DEBUG: path_nodes={path_nodes}")
            st.write(f"DEBUG: path_result={path_result}")
            
            # Create Mermaid flowchart with highlighted path
            highlighted_nodes = ','.join(path_nodes)
            
            mermaid_chart = """graph TD
    A[Start: Career Location?] --> B[Indonesia]
    A --> C[International]
    A --> D[Flexible]
    
    B --> E{Can Return?}
    C --> F{Can Self-Fund?}
    D --> G{Willing to Return?}
    
    E -->|Yes| H[PATH A: LPDP]
    E -->|No| I[PATH B: Erasmus]
    
    F -->|Yes| J[PATH B: USA]
    F -->|No| I
    
    G -->|Yes| K[PATH C: Hybrid]
    G -->|No| I
    
    classDef highlight fill:#90EE90,stroke:#006400,stroke-width:3px
"""
            
            # Add highlighting based on path
            if path_result == "PATH A":
                mermaid_chart += "\n    class A,B,E,H highlight"
            elif path_result == "PATH B (USA)":
                mermaid_chart += "\n    class A,C,F,J highlight"
            elif path_result == "PATH B (Europe)" or path_result == "PATH B":
                if career_loc == "Indonesia":
                    mermaid_chart += "\n    class A,B,E,I highlight"
                else:
                    mermaid_chart += "\n    class A,C,F,I highlight"
            elif path_result == "PATH C":
                mermaid_chart += "\n    class A,D,G,K highlight"
            
            st_mermaid(mermaid_chart, height=600)
            
            st.success(f"### ✅ Your Recommended Path: {path_result}")
            
            # Show path details
            if path_result == "PATH A":
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**📋 Action Plan:**")
                    st.markdown("1. Apply for **LPDP** (highest success rate)")
                    st.markdown("2. Apply for **Australia Awards**")
                    if profile['work_hours'] >= 2800:
                        st.markdown("3. Apply for **Chevening** (you meet work hours!)")
                    st.markdown("4. Choose any top university")
                    st.markdown("5. Return to Indonesia for 2+ years")
                with col2:
                    st.markdown("**🎯 Best Universities:**")
                    st.markdown("- MIT, Stanford, Oxford, Cambridge")
                    st.markdown("- Tsinghua, Peking (China)")
                    st.markdown("- ETH Zurich")
                    st.markdown("\n**Expected Outcome:**")
                    st.markdown("- Fully funded education")
                    st.markdown("- Indonesian salary: ~$30k/year")
            
            elif "PATH B" in path_result:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**📋 Action Plan:**")
                    if "USA" in path_result:
                        st.markdown("1. Apply for **Erasmus Mundus EMAI**")
                        st.markdown("2. Apply for **ETH ESOP** (if GPA 3.7+)")
                        st.markdown("3. Apply to MIT/Stanford/CMU")
                        st.markdown("4. Consider partial self-funding")
                    else:
                        st.markdown("1. Apply for **Erasmus Mundus EMAI**")
                        st.markdown("2. Apply for **ETH ESOP** (if GPA 3.7+)")
                        st.markdown("3. Apply for **DAAD** (Germany)")
                        st.markdown("4. Apply for **Spärck AI** (UK)")
                with col2:
                    st.markdown("**🎯 Best Universities:**")
                    if "USA" in path_result:
                        st.markdown("- MIT, Stanford, CMU ($140k-250k)")
                        st.markdown("- ETH Zurich ($138k)")
                        st.markdown("- Imperial, Oxford (£75k-120k)")
                    else:
                        st.markdown("- ETH Zurich ($138k, best value)")
                        st.markdown("- TUM Munich (€72k, easy visa)")
                        st.markdown("- Erasmus EMAI (fully funded)")
                        st.markdown("- NUS Singapore ($70k, easy visa)")
            
            elif path_result == "PATH C":
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**📋 Action Plan:**")
                    st.markdown("1. Apply for **LPDP** (Path A)")
                    st.markdown("2. Apply for **Erasmus Mundus** (Path B)")
                    st.markdown("3. Apply for **ETH ESOP** (Path B)")
                    st.markdown("4. Apply for **DAAD** (Path B)")
                    st.markdown("5. Decide based on offers received")
                with col2:
                    st.markdown("**🎯 Strategy:**")
                    st.markdown("- Maximize chances with both paths")
                    st.markdown("- If LPDP: Return 2 years, then reassess")
                    st.markdown("- If Path B: International career immediately")
                    st.markdown("- Keep options open until decision time")
        
        else:
            st.info("👈 **Complete your profile assessment** in the sidebar to see your personalized decision tree with highlighted path!")
            
            # Show generic flowchart
            st.markdown("**Generic Decision Tree (complete profile for personalized version):**")
            
            generic_chart = """graph TD
    A[Start: Career Location?] --> B[Indonesia]
    A --> C[International]
    A --> D[Flexible]
    
    B --> E{Can Return?}
    C --> F{Can Self-Fund?}
    D --> G{Willing to Return?}
    
    E -->|Yes| H[PATH A: LPDP]
    E -->|No| I[PATH B: Erasmus]
    
    F -->|Yes| J[PATH B: USA]
    F -->|No| I
    
    G -->|Yes| K[PATH C: Hybrid]
    G -->|No| I
"""
            
            st_mermaid(generic_chart, height=500)
        
        st.markdown("---")
        st.subheader("📊 Path Comparison")
        
        path_comparison = pd.DataFrame([
            {
                "Path": "A - Indonesia Career",
                "Scholarships": "LPDP, Australia Awards, Chevening",
                "Success Rate": "High",
                "Funding": "Full",
                "Return Required": "Yes (2+ years)",
                "Best For": "Indonesia career, fully funded priority"
            },
            {
                "Path": "B - International Career",
                "Scholarships": "Erasmus Mundus, ETH ESOP, DAAD, Spärck AI",
                "Success Rate": "Medium",
                "Funding": "Full or Partial",
                "Return Required": "No",
                "Best For": "International career, high salary priority"
            },
            {
                "Path": "C - Hybrid",
                "Scholarships": "LPDP (then decide later)",
                "Success Rate": "High",
                "Funding": "Full",
                "Return Required": "Yes (2+ years, then free)",
                "Best For": "Flexible, minimize risk, keep options open"
            }
        ])
        
        st.dataframe(path_comparison, use_container_width=True, hide_index=True)
    
    # TAB 5: ACTION ITEMS
    with tab5:
        st.header("📋 Immediate Action Items")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("🔴 URGENT")
            for item in ACTION_ITEMS['urgent']:
                if check_condition(item['condition'], profile):
                    st.markdown(f"- {item['action']}")
        
        with col2:
            st.subheader("🟡 HIGH")
            for item in ACTION_ITEMS['high']:
                if check_condition(item['condition'], profile):
                    st.markdown(f"- {item['action']}")
        
        with col3:
            st.subheader("🟢 MEDIUM")
            for item in ACTION_ITEMS['medium']:
                if check_condition(item['condition'], profile):
                    st.markdown(f"- {item['action']}")
    
    # TAB 6: WARNINGS
    with tab6:
        st.header("⚠️ Important Warnings")
        
        warnings_found = False
        for warning in WARNINGS:
            if check_condition(warning['condition'], profile):
                st.warning(f"**{warning['title']}:** {warning['message']}")
                warnings_found = True
        
        if not warnings_found:
            st.success("✅ No major warnings! Your profile looks good.")
    
    # TAB 7: TOP PICKS
    with tab7:
        st.header("⭐ Top Recommended Combinations")
        st.markdown("Based on research and analysis:")
        
        for combo in OPTIMAL_COMBINATIONS:
            with st.expander(f"{'⭐' * combo['rating']} {combo['university']} + {combo['scholarship']}", expanded=True):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Outcome:** {combo['outcome']}")
                    st.markdown(f"**Path:** {combo['path']}")
                    st.markdown(f"**Notes:** {combo['notes']}")
                with col2:
                    st.metric("Total Cost", f"${combo['total_cost']:,}")
                    st.caption(f"Rating: {'⭐' * combo['rating']}")
    
    st.success("✅ Assessment Complete! Good luck! 🚀")

# Financial Calculator (in sidebar after assessment)
with st.sidebar:
    if 'assessed' in st.session_state and st.session_state.assessed:
        st.markdown("---")
        
        # Filter universities by region
        if 'region_filter' not in st.session_state:
            st.session_state.region_filter = "All Regions"
        
        if st.session_state.region_filter == "All Regions":
            available_unis = list(UNIVERSITIES.keys())
        else:
            available_unis = [k for k, v in UNIVERSITIES.items() if v.get('region') == st.session_state.region_filter]
        
        # Further filter by country/city if selected
        if st.session_state.country_filter != "All":
            available_unis = [k for k in available_unis if UNIVERSITIES[k].get('city') == st.session_state.country_filter or UNIVERSITIES[k].get('country') == st.session_state.country_filter]
        
        selected_uni = st.selectbox(
            "🏛️ Select University",
            available_unis,
            help="Choose a university to see its costs and details"
        )
        
        selected_scholarship = st.selectbox(
            "💰 Select Scholarship",
            SCHOLARSHIP_AVAILABILITY[selected_uni],
            help="Choose a scholarship to see how much it covers. 'No Scholarship' = full self-funding"
        )

# Financial Calculator Results (in main area)
if 'assessed' in st.session_state and st.session_state.assessed:
    st.markdown("---")
    st.header("💵 Financial Calculator")
    st.markdown(f"**Selected:** {selected_uni} + {selected_scholarship}")
    
    # Get data from JSON
    uni_data = UNIVERSITIES[selected_uni]
    schol_data = SCHOLARSHIPS[selected_scholarship]
    
    # Calculate costs
    total_tuition = uni_data["tuition_per_year"] * uni_data["duration_years"]
    total_living = uni_data["living_per_year"] * uni_data["duration_years"]
    flights = 2000
    
    tuition_covered = total_tuition * schol_data["tuition_coverage"]
    living_covered = total_living * schol_data["living_coverage"]
    flights_covered = flights if schol_data["flights_covered"] else 0
    
    total_cost = total_tuition + total_living + flights
    total_covered = tuition_covered + living_covered + flights_covered
    out_of_pocket = total_cost - total_covered
    
    # Display results
    st.subheader("📊 Cost Breakdown")
    st.caption(f"Program: {uni_data['duration_years']} years in {uni_data['city']}, {uni_data.get('region', uni_data['country'])}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Cost", f"${total_cost:,.0f}")
    
    with col2:
        st.metric("Scholarship Covers", f"${total_covered:,.0f}")
        st.caption(f"{(total_covered/total_cost*100):.0f}%")
    
    with col3:
        st.metric("Your Cost", f"${out_of_pocket:,.0f}")
        if out_of_pocket == 0:
            st.caption("✅ Fully funded!")
        else:
            st.caption("⚠️ Need to pay")
    
    with col4:
        return_req = schol_data["return_required"]
        if return_req == True:
            st.metric("Return Required", "Yes")
            st.caption(f"{schol_data['return_years']}+ years")
        elif return_req == False:
            st.metric("Return Required", "No")
            st.caption("✅ Free to work")
        else:
            st.metric("Return Required", str(return_req))
            st.caption("⚠️ Verify")
    
    # Detailed breakdown
    with st.expander("📋 Detailed Cost Breakdown"):
        breakdown_data = {
            "Item": ["Tuition", "Living", "Flights", "Total"],
            "Total": [f"${total_tuition:,.0f}", f"${total_living:,.0f}", f"${flights:,.0f}", f"${total_cost:,.0f}"],
            "Covered": [f"${tuition_covered:,.0f}", f"${living_covered:,.0f}", f"${flights_covered:,.0f}", f"${total_covered:,.0f}"],
            "You Pay": [f"${total_tuition-tuition_covered:,.0f}", f"${total_living-living_covered:,.0f}", f"${flights-flights_covered:,.0f}", f"${out_of_pocket:,.0f}"]
        }
        st.table(breakdown_data)
    
    # Career attributes for selected university
    if 'career_attributes' in uni_data:
        st.markdown("---")
        st.subheader("💼 Career Outlook")
        
        career_attrs = uni_data['career_attributes']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Salary Tier", career_attrs.get('salary_tier', 'N/A'))
            # Get actual salary
            salary_country = uni_data['country']
            if salary_country == "Europe":
                salary_country = "EU"
            salary = uni_data['salaries'].get(salary_country, uni_data['salaries'].get(list(uni_data['salaries'].keys())[0]))
            st.caption(f"~${salary:,.0f}/year")
        
        with col2:
            visa_diff = career_attrs.get('visa_difficulty', 'N/A')
            st.metric("Visa Difficulty", visa_diff)
            if visa_diff == "Easy":
                st.caption("✅ Clear path")
            elif visa_diff == "Very Hard":
                st.caption("⚠️ Challenging")
            else:
                st.caption("⚠️ Moderate")
        
        with col3:
            st.metric("AI Maturity", career_attrs.get('ai_maturity', 'N/A'))
            st.caption("Industry strength")
        
        with col4:
            st.metric("Path to PR", career_attrs.get('path_to_pr', 'N/A').split('(')[0].strip())
            st.caption(career_attrs.get('work_language', 'N/A'))
    
    # Program focus for selected university
    if 'program_focus' in uni_data:
        st.markdown("---")
        st.subheader("🎓 Program Focus")
        
        program_focus = uni_data['program_focus']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            research_int = program_focus.get('research_intensity', 'N/A')
            st.metric("Research Intensity", research_int)
            if research_int in ["Very High", "High"]:
                st.caption("✅ Good for PhD")
            else:
                st.caption("⚠️ More coursework")
        
        with col2:
            industry_conn = program_focus.get('industry_connections', 'N/A')
            st.metric("Industry Connections", industry_conn)
            if industry_conn in ["Excellent", "Strong"]:
                st.caption("✅ Good for jobs")
            else:
                st.caption("⚠️ Limited internships")
        
        with col3:
            st.metric("Thesis", program_focus.get('thesis_requirement', 'N/A').split('(')[0].strip())
            st.caption(program_focus.get('internship_opportunities', 'N/A') + " internships")
        
        st.info(f"**Best For:** {program_focus.get('best_for', 'N/A')}")
        
        # China-specific city details
        if uni_data.get('region') == 'China' and 'city_details' in uni_data:
            st.markdown("---")
            st.subheader(f"🇨🇳 {uni_data['city']} Details")
            
            city_details = uni_data['city_details']
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**🏢 Top Companies:**")
                for company in city_details.get('companies', []):
                    st.markdown(f"- {company}")
                
                st.markdown("**✅ Advantages:**")
                for pro in city_details.get('pros', []):
                    st.markdown(f"- {pro}")
            
            with col2:
                st.markdown("**⚠️ Considerations:**")
                for con in city_details.get('cons', []):
                    st.markdown(f"- {con}")
                
                st.info(f"**City Tier:** {uni_data.get('city_tier', 'N/A')}")


else:
    st.info("👈 Fill in your profile in the sidebar and click 'Generate Assessment'")
    
    st.markdown("""
    ## What This Tool Does
    
    - **Competitiveness Score** (0-100) based on your profile
    - **Target University Tier** you can realistically apply to
    - **Recommended Path** (A: Indonesia, B: International, C: Hybrid)
    - **Scholarship Rankings** prioritized by success rate
    - **University Combinations** optimized for your goals
    - **Action Items** with urgency levels
    - **Financial Calculator** to compare costs
    
    ## Key Decision
    
    **Where do you want to build your career?**
    
    - **Indonesia:** LPDP is best (fully funded, must return 2+ years)
    - **International:** Erasmus Mundus, ETH ESOP, Spärck AI, DAAD
    - **Flexible:** Apply to both and decide later
    """)
