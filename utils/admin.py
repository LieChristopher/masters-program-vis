"""Admin UI for editing university_data.json"""
import streamlit as st
import json
import os
from datetime import datetime
from datetime import datetime

def load_json_data():
    """Load university_data.json"""
    with open('data/university_data.json', 'r') as f:
        return json.load(f)

def save_json_data(data):
    """Save university_data.json"""
    with open('data/university_data.json', 'w') as f:
        json.dump(data, f, indent=2)
    return True

def load_countries_data():
    """Load countries.json"""
    with open('data/countries.json', 'r') as f:
        return json.load(f)

def save_countries_data(data):
    """Save countries.json"""
    with open('data/countries.json', 'w') as f:
        json.dump(data, f, indent=2)
    return True

def load_exchange_rates_data():
    """Load exchange_rates.json"""
    with open('data/exchange_rates.json', 'r') as f:
        return json.load(f)

def save_exchange_rates_data(data):
    """Save exchange_rates.json"""
    with open('data/exchange_rates.json', 'w') as f:
        json.dump(data, f, indent=2)
    return True

def load_deadlines_data():
    """Load deadlines.json"""
    with open('data/deadlines.json', 'r') as f:
        return json.load(f)

def save_deadlines_data(data):
    """Save deadlines.json"""
    with open('data/deadlines.json', 'w') as f:
        json.dump(data, f, indent=2)
    return True

def load_eligibility_data():
    """Load eligibility.json"""
    with open('data/eligibility.json', 'r') as f:
        return json.load(f)

def save_eligibility_data(data):
    """Save eligibility.json"""
    with open('data/eligibility.json', 'w') as f:
        json.dump(data, f, indent=2)
    return True

def edit_university(data):
    """Edit university data"""
    st.subheader("✏️ Edit University")
    
    # Show table of all universities
    with st.expander("📊 View All Universities", expanded=False):
        import pandas as pd
        uni_list = []
        for key, uni in data['universities'].items():
            uni_list.append({
                "Key": key,
                "Name": uni['name'],
                "Country": uni['country'],
                "City": uni['city'],
                "Tier": uni['tier'],
                "Tuition": f"{uni['tuition_per_year']['currency']} {uni['tuition_per_year']['amount']:,}",
                "Duration": f"{uni['duration_years']}y"
            })
        st.dataframe(pd.DataFrame(uni_list), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    uni_name = st.selectbox("Select University:", list(data['universities'].keys()))
    uni = data['universities'][uni_name]
    
    col1, col2 = st.columns(2)
    with col1:
        col_tuition1, col_tuition2 = st.columns([3, 1])
        with col_tuition1:
            uni['tuition_per_year']['amount'] = st.number_input(
                "Tuition/year:", 
                value=uni['tuition_per_year']['amount'], 
                min_value=0,
                step=1000,
                key="tuition_amount"
            )
        with col_tuition2:
            uni['tuition_per_year']['currency'] = st.text_input(
                "Currency",
                value=uni['tuition_per_year']['currency'],
                max_chars=3,
                key="tuition_currency"
            )
        
        col_living1, col_living2 = st.columns([3, 1])
        with col_living1:
            uni['living_per_year']['amount'] = st.number_input(
                "Living/year:", 
                value=uni['living_per_year']['amount'], 
                min_value=0,
                step=1000,
                key="living_amount"
            )
        with col_living2:
            uni['living_per_year']['currency'] = st.text_input(
                "Currency",
                value=uni['living_per_year']['currency'],
                max_chars=3,
                key="living_currency"
            )
        uni['duration_years'] = st.number_input(
            "Duration (years):", 
            value=float(uni['duration_years']), 
            min_value=0.5,
            step=0.5
        )
        uni['tier'] = st.selectbox("Tier:", [1, 2, 3], index=uni['tier']-1)
        uni['tier_override'] = st.selectbox(
            "Tier Override (None = calculated):",
            [None, 1, 2, 3],
            index=[None, 1, 2, 3].index(uni.get('tier_override'))
        )
        if uni['tier_override'] is not None:
            uni['tier_override_reason'] = st.text_input(
                "Override Reason:",
                value=uni.get('tier_override_reason', '')
            )
        uni['admission_rate'] = st.slider(
            "Admission Rate:", 
            0.0, 1.0, 
            value=uni.get('admission_rate', 0.1),
            step=0.01
        )
        uni['enrollment'] = st.number_input(
            "Enrollment (students):", 
            value=uni.get('enrollment', 200),
            min_value=0,
            step=10
        )
        uni['human_validated'] = st.checkbox(
            "Human Validated",
            value=uni.get('human_validated', False)
        )
        last_updated_date = st.date_input(
            "Last Updated",
            value=None
        )
        if last_updated_date:
            uni['last_updated'] = last_updated_date.isoformat()
        else:
            uni['last_updated'] = uni.get('last_updated', '')
    
    with col2:
        uni['qs_ranking_2026'] = st.number_input(
            "QS Ranking 2026:", 
            value=int(uni['qs_ranking_2026']) if uni['qs_ranking_2026'] else 0,
            min_value=0,
            step=1
        )
        uni['the_ranking_2026'] = st.number_input(
            "THE Ranking 2026:", 
            value=int(uni['the_ranking_2026']) if uni['the_ranking_2026'] else 0,
            min_value=0,
            step=1
        )
        uni['csrankings_ai_2026'] = st.number_input(
            "CSRankings AI 2026:", 
            value=int(uni['csrankings_ai_2026']) if uni['csrankings_ai_2026'] else 0,
            min_value=0,
            step=1
        )
    
    st.write("**Salaries by Country:**")
    for country in uni['salaries']:
        uni['salaries'][country] = st.number_input(
            f"{country} salary ($):",
            value=uni['salaries'][country],
            min_value=0,
            step=1000,
            key=f"salary_{country}"
        )
    
    st.write("**URLs:**")
    col1, col2 = st.columns(2)
    with col1:
        uni['urls']['website'] = st.text_input("Website:", value=uni['urls'].get('website', ''), key="url_website")
        uni['urls']['program_page'] = st.text_input("Program Page:", value=uni['urls'].get('program_page', ''), key="url_program")
    with col2:
        uni['urls']['admissions'] = st.text_input("Admissions:", value=uni['urls'].get('admissions', ''), key="url_admissions")
        uni['urls']['curriculum'] = st.text_input("Curriculum:", value=uni['urls'].get('curriculum', ''), key="url_curriculum")
    
    if st.button("💾 Save University", key="save_uni"):
        save_json_data(data)
        st.success(f"✅ {uni_name} updated!")
        st.rerun()

def edit_scholarship(data):
    """Edit scholarship data"""
    st.subheader("✏️ Edit Scholarship")
    
    # Show table of all scholarships
    with st.expander("📊 View All Scholarships", expanded=False):
        import pandas as pd
        schol_list = []
        for key, schol in data['scholarships'].items():
            schol_list.append({
                "Key": key,
                "Name": schol['name'],
                "Tuition": f"{schol['tuition_coverage']*100:.0f}%",
                "Living": f"{schol['living_coverage']*100:.0f}%",
                "Flights": "✅" if schol['flights_covered'] else "❌",
                "Return": "Yes" if schol['return_required'] else "No"
            })
        st.dataframe(pd.DataFrame(schol_list), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    schol_name = st.selectbox("Select Scholarship:", list(data['scholarships'].keys()))
    schol = data['scholarships'][schol_name]
    
    col1, col2 = st.columns(2)
    with col1:
        schol['tuition_coverage'] = st.slider(
            "Tuition Coverage:", 
            0.0, 1.0, 
            value=schol['tuition_coverage'],
            step=0.1
        )
        schol['living_coverage'] = st.slider(
            "Living Coverage:", 
            0.0, 1.0, 
            value=schol['living_coverage'],
            step=0.1
        )
        schol['flights_covered'] = st.checkbox(
            "Flights Covered:", 
            value=schol['flights_covered']
        )
    
    with col2:
        schol['return_required'] = st.checkbox(
            "Return Required:", 
            value=schol['return_required']
        )
        if schol['return_required']:
            schol['return_years'] = st.number_input(
                "Return Years:", 
                value=schol['return_years'],
                min_value=0,
                step=1
            )
        schol['success_rate'] = st.selectbox(
            "Success Rate:",
            ["Very Low", "Low", "Medium", "High", "Very High"],
            index=["Very Low", "Low", "Medium", "High", "Very High"].index(schol['success_rate'])
        )
    
    st.write("**Age Limits:**")
    col1, col2 = st.columns(2)
    with col1:
        age_min = schol['age_limit'].get('min_age')
        schol['age_limit']['min_age'] = st.number_input(
            "Min Age:", 
            value=age_min if age_min else 0,
            min_value=0,
            key="age_min"
        ) or None
    with col2:
        age_max = schol['age_limit'].get('max_age')
        schol['age_limit']['max_age'] = st.number_input(
            "Max Age:", 
            value=age_max if age_max else 0,
            min_value=0,
            key="age_max"
        ) or None
    
    schol['age_limit']['notes'] = st.text_area(
        "Age Notes:",
        value=schol['age_limit'].get('notes', ''),
        key="age_notes"
    )
    
    st.write("**Validation:**")
    schol['human_validated'] = st.checkbox(
        "Human Validated",
        value=schol.get('human_validated', False),
        key="schol_validated"
    )
    
    st.write("**URLs:**")
    col1, col2 = st.columns(2)
    with col1:
        schol['urls']['website'] = st.text_input("Website:", value=schol['urls'].get('website', ''), key="schol_url_website")
        schol['urls']['application_page'] = st.text_input("Application Page:", value=schol['urls'].get('application_page', ''), key="schol_url_app")
    with col2:
        schol['urls']['requirements'] = st.text_input("Requirements:", value=schol['urls'].get('requirements', ''), key="schol_url_req")
    
    if st.button("💾 Save Scholarship", key="save_schol"):
        save_json_data(data)
        st.success(f"✅ {schol_name} updated!")
        st.rerun()

def add_university(data):
    """Add new university"""
    st.subheader("➕ Add University")
    
    uni_key = st.text_input("University Key (e.g., 'MIT'):")
    if uni_key and uni_key not in data['universities']:
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name:")
            country = st.text_input("Country:")
            city = st.text_input("City:")
            region = st.selectbox("Region:", ["North America", "Europe", "Asia", "Asia-Pacific"])
        with col2:
            tuition = st.number_input("Tuition/year ($):", min_value=0, step=1000)
            living = st.number_input("Living/year ($):", min_value=0, step=1000)
            duration = st.number_input("Duration (years):", min_value=0.5, step=0.5)
            tier = st.selectbox("Tier:", [1, 2, 3])
        
        if st.button("➕ Add University"):
            data['universities'][uni_key] = {
                "name": name,
                "country": country,
                "region": region,
                "city": city,
                "tuition_per_year": tuition,
                "living_per_year": living,
                "duration_years": duration,
                "tier": tier,
                "urls": {"website": "", "program_page": "", "admissions": "", "curriculum": ""},
                "salaries": {"Country": 0},
                "career_attributes": {
                    "salary_tier": "Medium",
                    "visa_difficulty": "Medium",
                    "ai_maturity": "Tier 2",
                    "path_to_pr": "Medium",
                    "work_language": "English"
                },
                "program_focus": {
                    "research_intensity": "Medium",
                    "industry_connections": "Moderate",
                    "thesis_requirement": "Optional",
                    "internship_opportunities": "Good",
                    "best_for": ""
                },
                "qs_ranking_2026": None,
                "the_ranking_2026": None,
                "csrankings_ai_2026": None,
                "us_news_cs_2026": None
            }
            data['scholarship_availability'][uni_key] = ["No Scholarship (Self-fund)"]
            save_json_data(data)
            st.success(f"✅ {name} added!")
            st.rerun()

def add_scholarship(data):
    """Add new scholarship"""
    st.subheader("➕ Add Scholarship")
    
    schol_key = st.text_input("Scholarship Key (e.g., 'MyScholarship'):")
    if schol_key and schol_key not in data['scholarships']:
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name:")
            tuition_cov = st.slider("Tuition Coverage:", 0.0, 1.0, 0.5, step=0.1)
            living_cov = st.slider("Living Coverage:", 0.0, 1.0, 0.5, step=0.1)
        with col2:
            flights = st.checkbox("Flights Covered:")
            return_req = st.checkbox("Return Required:")
            return_years = st.number_input("Return Years:", min_value=0, step=1) if return_req else 0
            success_rate = st.selectbox("Success Rate:", ["Very Low", "Low", "Medium", "High", "Very High"])
        
        if st.button("➕ Add Scholarship"):
            data['scholarships'][schol_key] = {
                "name": name,
                "tuition_coverage": tuition_cov,
                "living_coverage": living_cov,
                "flights_covered": flights,
                "return_required": return_req,
                "return_years": return_years,
                "eligible_countries": ["All"],
                "eligible_regions": ["All"],
                "success_rate": success_rate,
                "notes": "",
                "age_limit": {"min_age": None, "max_age": None, "notes": ""},
                "urls": {"website": "", "application_page": "", "requirements": ""}
            }
            save_json_data(data)
            st.success(f"✅ {name} added!")
            st.rerun()

def edit_exchange_rates(data):
    """Edit exchange rates"""
    st.subheader("✏️ Edit Exchange Rates")
    
    st.write("**Rates to IDR:**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        for currency in list(data['rates_to_idr'].keys())[:6]:
            data['rates_to_idr'][currency] = st.number_input(
                f"{currency} to IDR:",
                value=data['rates_to_idr'][currency],
                min_value=0,
                step=100,
                key=f"rate_{currency}"
            )
    
    with col2:
        for currency in list(data['rates_to_idr'].keys())[6:]:
            data['rates_to_idr'][currency] = st.number_input(
                f"{currency} to IDR:",
                value=data['rates_to_idr'][currency],
                min_value=0,
                step=100,
                key=f"rate_{currency}"
            )
    
    data['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
    
    if st.button("💾 Save Exchange Rates", key="save_rates"):
        save_exchange_rates_data(data)
        st.success("✅ Exchange rates updated!")
        st.rerun()

def edit_deadlines(data):
    """Edit scholarship and university deadlines"""
    st.subheader("✏️ Edit Deadlines")
    
    deadline_type = st.radio("Edit:", ["Scholarships", "Universities"])
    
    if deadline_type == "Scholarships":
        schol_name = st.selectbox("Select Scholarship:", list(data['scholarships'].keys()))
        schol = data['scholarships'][schol_name]
        
        col1, col2 = st.columns(2)
        with col1:
            schol['application_open'] = st.text_input("Application Open:", value=schol.get('application_open', ''), key="schol_app_open")
            schol['application_close'] = st.text_input("Application Close:", value=schol.get('application_close', ''), key="schol_app_close")
        with col2:
            schol['notification_date'] = st.text_input("Notification Date:", value=schol.get('notification_date', ''), key="schol_notif")
            schol['enrollment_date'] = st.text_input("Enrollment Date:", value=schol.get('enrollment_date', ''), key="schol_enroll")
        
        schol['notes'] = st.text_area("Notes:", value=schol.get('notes', ''), key="schol_notes")
        
        if st.button("💾 Save Scholarship Deadlines", key="save_schol_deadlines"):
            save_deadlines_data(data)
            st.success(f"✅ {schol_name} deadlines updated!")
            st.rerun()
    
    else:  # Universities
        uni_name = st.selectbox("Select University:", list(data['universities'].keys()))
        uni = data['universities'][uni_name]
        
        col1, col2 = st.columns(2)
        with col1:
            uni['application_open'] = st.text_input("Application Open:", value=uni.get('application_open', ''), key="uni_app_open")
            uni['application_close'] = st.text_input("Application Close:", value=uni.get('application_close', ''), key="uni_app_close")
        with col2:
            uni['decision_date'] = st.text_input("Decision Date:", value=uni.get('decision_date', ''), key="uni_decision")
            uni['enrollment_deadline'] = st.text_input("Enrollment Deadline:", value=uni.get('enrollment_deadline', ''), key="uni_enroll")
        
        uni['notes'] = st.text_area("Notes:", value=uni.get('notes', ''), key="uni_notes")
        
        if st.button("💾 Save University Deadlines", key="save_uni_deadlines"):
            save_deadlines_data(data)
            st.success(f"✅ {uni_name} deadlines updated!")
            st.rerun()

def edit_eligibility(data):
    """Edit scholarship and university eligibility requirements"""
    st.subheader("✏️ Edit Eligibility Requirements")
    
    eligibility_type = st.radio("Edit:", ["Scholarships", "Universities"])
    
    if eligibility_type == "Scholarships":
        schol_name = st.selectbox("Select Scholarship:", list(data['scholarships'].keys()))
        schol = data['scholarships'][schol_name]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            schol['gpa_min'] = st.number_input("GPA Min:", value=schol.get('gpa_min') or 0.0, min_value=0.0, max_value=4.0, step=0.1, key="schol_gpa")
            schol['ielts_min'] = st.number_input("IELTS Min:", value=schol.get('ielts_min') or 0.0, min_value=0.0, max_value=9.0, step=0.5, key="schol_ielts")
        with col2:
            schol['gre_min'] = st.number_input("GRE Min:", value=schol.get('gre_min') or 0, min_value=0, step=10, key="schol_gre")
            schol['toefl_min'] = st.number_input("TOEFL Min:", value=schol.get('toefl_min') or 0, min_value=0, step=5, key="schol_toefl")
        with col3:
            schol['work_experience_years_min'] = st.number_input("Work Exp Min (years):", value=schol.get('work_experience_years_min') or 0, min_value=0, step=1, key="schol_work_min")
            schol['work_experience_years_max'] = st.number_input("Work Exp Max (years):", value=schol.get('work_experience_years_max') or 0, min_value=0, step=1, key="schol_work_max")
        
        schol['notes'] = st.text_area("Notes:", value=schol.get('notes', ''), key="schol_elig_notes")
        
        if st.button("💾 Save Scholarship Eligibility", key="save_schol_elig"):
            save_eligibility_data(data)
            st.success(f"✅ {schol_name} eligibility updated!")
            st.rerun()
    
    else:  # Universities
        uni_name = st.selectbox("Select University:", list(data['universities'].keys()))
        uni = data['universities'][uni_name]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            uni['gpa_min'] = st.number_input("GPA Min:", value=uni.get('gpa_min') or 0.0, min_value=0.0, max_value=4.0, step=0.1, key="uni_gpa")
            uni['ielts_min'] = st.number_input("IELTS Min:", value=uni.get('ielts_min') or 0.0, min_value=0.0, max_value=9.0, step=0.5, key="uni_ielts")
        with col2:
            uni['gre_min'] = st.number_input("GRE Min:", value=uni.get('gre_min') or 0, min_value=0, step=10, key="uni_gre")
            uni['toefl_min'] = st.number_input("TOEFL Min:", value=uni.get('toefl_min') or 0, min_value=0, step=5, key="uni_toefl")
        with col3:
            uni['work_experience_years_min'] = st.number_input("Work Exp Min (years):", value=uni.get('work_experience_years_min') or 0, min_value=0, step=1, key="uni_work")
        
        uni['notes'] = st.text_area("Notes:", value=uni.get('notes', ''), key="uni_elig_notes")
        
        if st.button("💾 Save University Eligibility", key="save_uni_elig"):
            save_eligibility_data(data)
            st.success(f"✅ {uni_name} eligibility updated!")
            st.rerun()

def edit_country(data):
    """Edit country data"""
    st.subheader("✏️ Edit Country")
    
    country_name = st.selectbox("Select Country:", list(data.keys()))
    country = data[country_name]
    
    col1, col2 = st.columns(2)
    with col1:
        country['salary_tier'] = st.selectbox(
            "Salary Tier:",
            ["Low", "Medium", "Medium-High", "High", "Highest"],
            index=["Low", "Medium", "Medium-High", "High", "Highest"].index(country['salary_tier'])
        )
        country['visa_type'] = st.text_input("Visa Type:", value=country['visa_type'])
        country['post_study_work_visa'] = st.text_input("Post-Study Work Visa:", value=country['post_study_work_visa'])
        country['post_study_work_duration_years'] = st.number_input(
            "Post-Study Work Duration (years):",
            value=int(country['post_study_work_duration_years']),
            min_value=0,
            step=1
        )
    
    with col2:
        country['pr_eligible'] = st.checkbox("PR Eligible:", value=country['pr_eligible'])
        country['pr_timeline_years'] = st.number_input(
            "PR Timeline (years):",
            value=int(country['pr_timeline_years']),
            min_value=0,
            step=1
        )
        country['work_availability'] = st.selectbox(
            "Work Availability:",
            ["Low", "Medium", "High"],
            index=["Low", "Medium", "High"].index(country['work_availability'])
        )
        country['human_validated'] = st.checkbox(
            "Human Validated",
            value=country.get('human_validated', False),
            key="country_validated"
        )
    
    if st.button("💾 Save Country", key="save_country"):
        save_countries_data(data)
        st.success(f"✅ {country_name} updated!")
        st.rerun()

def admin_panel():
    """Main admin panel"""
    st.set_page_config(page_title="Admin - Data Editor", layout="wide")
    
    st.title("🔧 Admin Panel - Data Editor")
    
    # Load data
    data = load_json_data()
    
    # Navigation
    admin_section = st.sidebar.radio(
        "Admin Menu:",
        ["Edit University", "Edit Scholarship", "Add University", "Add Scholarship", "View JSON"]
    )
    
    if admin_section == "Edit University":
        edit_university(data)
    elif admin_section == "Edit Scholarship":
        edit_scholarship(data)
    elif admin_section == "Add University":
        add_university(data)
    elif admin_section == "Add Scholarship":
        add_scholarship(data)
    elif admin_section == "View JSON":
        st.subheader("📄 Raw JSON Data")
        st.json(data)
        if st.button("📥 Download JSON"):
            st.download_button(
                label="Download university_data.json",
                data=json.dumps(data, indent=2),
                file_name="university_data.json",
                mime="application/json"
            )
