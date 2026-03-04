import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
import os
from datetime import datetime
from utils.data_loader import load_data
from utils.assessment import calculate_competitiveness_score, assess_university_tier, check_condition
from utils.admin import edit_university, edit_scholarship, add_university, add_scholarship, load_json_data, save_json_data

st.set_page_config(page_title="AI Master's Assessment", page_icon="🎓", layout="wide")

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
    
    # Load exchange rates
    with open('data/exchange_rates.json', 'r') as f:
        EXCHANGE_RATES = json.load(f)
    USD_TO_IDR = EXCHANGE_RATES['rates_to_idr']['USD']
    
except FileNotFoundError:
    st.error("⚠️ university_data.json not found. Please ensure the file exists in the same directory.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")
    st.stop()

def format_usd_with_idr(amount):
    """Format USD amount with IDR equivalent"""
    idr_amount = amount * USD_TO_IDR
    return f"${amount:,.0f} (≈ Rp {idr_amount:,.0f})"

def get_cost_in_idr(cost_dict):
    """Convert cost dict to IDR"""
    amount = cost_dict['amount']
    currency = cost_dict['currency']
    return amount * EXCHANGE_RATES['rates_to_idr'][currency]

def get_cost_in_usd(cost_dict):
    """Convert cost dict to USD via IDR"""
    idr = get_cost_in_idr(cost_dict)
    return idr / USD_TO_IDR

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

# Initialize admin_mode
admin_mode = False

# Sidebar for inputs (moved before title so we can check admin_mode)
with st.sidebar:
    st.header("📝 Your Profile")
    
    st.subheader("📚 Academic")
    gpa = st.slider("GPA (4.0 scale)", 2.0, 4.0, 3.5, 0.1, key='gpa', 
                    help="Your undergraduate GPA converted to 4.0 scale")
    ielts = st.number_input("IELTS score (0 if not taken)", 0.0, 9.0, 0.0, 0.5, key='ielts', 
                            help="Overall band score. Most programs need 6.5-7.5")
    toefl = st.number_input("TOEFL iBT (0 if not taken)", 0, 120, 0, 5, key='toefl', 
                            help="Total score. Most programs need 90-100")
    
    st.subheader("💼 Work Experience")
    st.caption("Include all paid work: full-time, part-time, internships")
    
    work_years = st.number_input("Years of full-time work", min_value=0.0, max_value=20.0, value=0.0,
                                 step=0.5, key='work_years', help="Full-time employment (2000 hours/year)")
    internship_months = st.number_input("Internship months (if any)", min_value=0, max_value=60, value=0, 
                                       step=1, key='internship_months', help="Paid internships (160 hours/month)")
    part_time_years = st.number_input("Years of part-time work (if any)", min_value=0.0, max_value=10.0, value=0.0, step=0.5, key='part_time_years',
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
    can_self_fund = st.checkbox("Can partially self-fund if needed", value=False, key='can_self_fund',
                                help="Can you contribute your own money if scholarships don't cover everything?")
    
    if can_self_fund:
        self_fund_budget = st.slider(
            "How much can you contribute? (USD)",
            min_value=0,
            max_value=200000,
            value=50000,
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
        index=2,
        key='career_location',
        help="Where do you want to work after graduation? This affects scholarship and university recommendations."
    )
    
    if career_location == "Flexible":
        can_return = st.checkbox("Willing to return to Indonesia for 2+ years?", value=True, key='can_return',
                                help="LPDP and similar scholarships require you to return to Indonesia for 2+ years after graduation")
    else:
        can_return = career_location == "Indonesia"
        st.session_state['can_return'] = can_return
    
    # Auto-update profile (no button needed)
    st.session_state.profile = {
        'gpa': gpa, 'ielts': ielts, 'toefl': toefl,
        'work_hours': work_hours, 'has_research': has_research,
        'has_publications': has_publications, 'can_self_fund': can_self_fund,
        'self_fund_budget': self_fund_budget if can_self_fund else 0,
        'career_location': career_location, 'can_return': can_return
    }
    
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
    
    # Admin mode at bottom
    st.markdown("---")
    admin_mode = st.checkbox("🔧 Admin Mode", help="Enable to edit university and scholarship data")
    
    if admin_mode:
        st.warning("⚠️ **Admin Mode Enabled**")
        admin_section = st.radio(
            "Admin Menu:",
            ["Edit University", "Edit Scholarship", "Add University", "Add Scholarship", "Edit Country", "Edit Exchange Rates", "Edit Deadlines", "Edit Eligibility"]
        )
    else:
        admin_section = None

# Main content
st.session_state.region_filter = region_filter
st.session_state.country_filter = country_filter

# Render admin UI in main area if enabled
if admin_mode:
    st.title("🔧 Admin Panel")
    
    # Load data for admin
    admin_data = load_json_data()
    
    if admin_section == "Edit University":
        edit_university(admin_data)
    elif admin_section == "Edit Scholarship":
        edit_scholarship(admin_data)
    elif admin_section == "Add University":
        add_university(admin_data)
    elif admin_section == "Add Scholarship":
        add_scholarship(admin_data)
    elif admin_section == "Edit Country":
        from utils.admin import load_countries_data, edit_country
        countries_data = load_countries_data()
        edit_country(countries_data)
    elif admin_section == "Edit Exchange Rates":
        from utils.admin import load_exchange_rates_data, edit_exchange_rates
        rates_data = load_exchange_rates_data()
        edit_exchange_rates(rates_data)
    elif admin_section == "Edit Deadlines":
        from utils.admin import load_deadlines_data, edit_deadlines
        deadlines_data = load_deadlines_data()
        edit_deadlines(deadlines_data)
    elif admin_section == "Edit Eligibility":
        from utils.admin import load_eligibility_data, edit_eligibility
        eligibility_data = load_eligibility_data()
        edit_eligibility(eligibility_data)

# Show title only if not in admin mode
elif not admin_mode:
    st.title("🎓 AI Master's Program Assessment Tool")
    st.markdown("*Get personalized recommendations for scholarships and universities*")

# Always show assessment (no button check needed)
if not admin_mode:
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
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview",
        "💰 Scholarships", 
        "🏛️ Universities", 
        "💵 Calculator"
    ])
    
    # TAB 1: OVERVIEW
    with tab1:
        st.header("📊 Your Assessment Overview")
        
        # Show top picks
        st.subheader("⭐ Top Recommendations")
        for i, combo in enumerate(OPTIMAL_COMBINATIONS[:3], 1):
            with st.expander(f"#{i}: {combo['university']} + {combo['scholarship']}", expanded=(i==1)):
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.markdown(f"**Outcome:** {combo['outcome']}")
                    st.markdown(f"**Path:** {combo['path']}")
                    st.markdown(f"**Notes:** {combo['notes']}")
                with col2:
                    st.metric("Total Cost", f"${combo['total_cost']:,}", 
                             delta=f"Rp {combo['total_cost'] * USD_TO_IDR:,.0f}")
                    st.caption(f"Rating: {'⭐' * combo['rating']}")
        
        # Show action items
        st.markdown("---")
        st.subheader("📋 Action Items")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🔴 URGENT**")
            for item in ACTION_ITEMS['urgent']:
                if check_condition(item['condition'], profile):
                    st.warning(f"**{item['action']}**")
        
        with col2:
            st.markdown("**🟡 HIGH**")
            for item in ACTION_ITEMS['high']:
                if check_condition(item['condition'], profile):
                    st.info(f"**{item['action']}**")
        
        with col3:
            st.markdown("**🟢 MEDIUM**")
            for item in ACTION_ITEMS['medium']:
                if check_condition(item['condition'], profile):
                    st.success(f"**{item['action']}**")
        
        # Show warnings
        st.markdown("---")
        st.subheader("⚠️ Important Warnings")
        
        warnings_shown = 0
        for warning in WARNINGS:
            if check_condition(warning['condition'], profile):
                st.warning(f"**{warning['title']}**\n\n{warning['message']}")
                warnings_shown += 1
        
        if warnings_shown == 0:
            st.success("✅ No warnings for your profile!")
    
    # TAB 2: SCHOLARSHIPS
    with tab2:
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
    
    # TAB 3: UNIVERSITIES
    with tab3:
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
            
            # Convert costs to USD
            tuition_usd = get_cost_in_usd(uni_data['tuition_per_year'])
            living_usd = get_cost_in_usd(uni_data['living_per_year'])
            total_cost_usd = (tuition_usd + living_usd) * uni_data['duration_years']
            
            comparison_data.append({
                "University": uni_data['name'],
                "Region": uni_data.get('region', 'N/A'),
                "City": uni_data['city'],
                "Tier": uni_data['tier'],
                "Duration": f"{uni_data['duration_years']}y",
                "Total Cost": format_usd_with_idr(total_cost_usd),
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
                living_usd = get_cost_in_usd(uni_data['living_per_year'])
                china_comparison.append({
                    "University": uni_data['name'],
                    "City": uni_data['city'],
                    "City Tier": uni_data.get('city_tier', 'N/A'),
                    "Living Cost/Year": f"${living_usd:,.0f}",
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
    
    # TAB 4: CALCULATOR
    with tab4:
        st.header("💵 Financial Calculator")
        st.markdown("**Calculate the exact cost of any university-scholarship combination**")
        
        # Get recommended university (first from user's tier)
        tier_num = 1 if "Tier 1" in tier else (2 if "Tier 2" in tier else 3)
        tier_unis = [k for k, v in UNIVERSITIES.items() if v.get('tier') == tier_num]
        default_uni = tier_unis[0] if tier_unis else list(UNIVERSITIES.keys())[0]
        
        # University selector
        calc_uni = st.selectbox(
            "🏛️ Select University",
            list(UNIVERSITIES.keys()),
            index=list(UNIVERSITIES.keys()).index(default_uni),
            key='calc_uni'
        )
        
        # Scholarship selector (prefill with highest success rate)
        available_schols = SCHOLARSHIP_AVAILABILITY.get(calc_uni, [])
        calc_schol = st.selectbox(
            "💰 Select Scholarship",
            available_schols,
            key='calc_schol'
        )
        
        st.markdown("---")
        
        # Get data
        uni_data = UNIVERSITIES[calc_uni]
        schol_data = SCHOLARSHIPS[calc_schol]
        
        # Calculate costs
        tuition_usd = get_cost_in_usd(uni_data["tuition_per_year"])
        living_usd = get_cost_in_usd(uni_data["living_per_year"])
        
        total_tuition = tuition_usd * uni_data["duration_years"]
        total_living = living_usd * uni_data["duration_years"]
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
            st.metric("Total Cost", f"${total_cost:,.0f}", 
                     delta=f"Rp {total_cost * USD_TO_IDR:,.0f}")
        
        with col2:
            st.metric("Scholarship Covers", f"${total_covered:,.0f}",
                     delta=f"Rp {total_covered * USD_TO_IDR:,.0f}")
            st.caption(f"{(total_covered/total_cost*100):.0f}%")
        
        with col3:
            st.metric("Your Cost", f"${out_of_pocket:,.0f}",
                     delta=f"Rp {out_of_pocket * USD_TO_IDR:,.0f}")
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
        
        # Budget check
        if profile['can_self_fund'] and out_of_pocket > 0:
            budget = profile['self_fund_budget']
            if out_of_pocket <= budget:
                st.success(f"✅ Within your budget! You have ${budget - out_of_pocket:,.0f} remaining.")
            else:
                st.error(f"❌ Exceeds your budget by ${out_of_pocket - budget:,.0f}")
        
        # ROI calculation
        salary_country = uni_data['country']
        if salary_country == "Europe":
            salary_country = "EU"
        salary = uni_data['salaries'].get(salary_country, uni_data['salaries'].get(list(uni_data['salaries'].keys())[0]))
        
        if out_of_pocket > 0:
            years_to_break_even = out_of_pocket / salary
            st.info(f"💡 **ROI:** {years_to_break_even:.1f} years to break even (salary: ${salary:,.0f}/year)")

