# Admin Panel Guide

**Last Updated:** 2026-03-04

---

## 🚀 Quick Start

Run the main app:
```bash
streamlit run streamlit_app.py
```

Then:
1. Scroll to the bottom of the **sidebar** (left side)
2. Check the box: **🔧 Admin Mode**
3. Select what you want to edit from the menu

---

## 📋 Features

### 1. Edit University
- Select a university from the dropdown
- Update costs, duration, rankings, salaries
- Add/update URLs (website, program page, admissions, curriculum)
- Changes save immediately to `university_data.json`

### 2. Edit Scholarship
- Select a scholarship from the dropdown
- Update coverage (tuition, living, flights)
- Set return requirements and success rate
- Add/update age limits and URLs
- Changes save immediately

### 3. Add University
- Enter university key (e.g., "MIT", "Stanford")
- Fill in basic info (name, country, city, region)
- Add costs and duration
- Creates entry with default values for other fields
- You can edit it further using "Edit University"

### 4. Add Scholarship
- Enter scholarship key (e.g., "MyScholarship")
- Fill in coverage percentages
- Set return requirements
- Creates entry with default values
- You can edit it further using "Edit Scholarship"

### 5. View JSON
- See the raw JSON data
- Download the entire `university_data.json` file
- Useful for backup or manual inspection

---

## 🔄 Common Workflows

### Update Costs (e.g., 2027 tuition increases)
1. Go to "Edit University"
2. Select university
3. Update `Tuition/year` and `Living/year`
4. Click "Save University"
5. Done! Changes appear in main app immediately

### Add New University
1. Go to "Add University"
2. Fill in basic info
3. Click "Add University"
4. Go to "Edit University" to add more details (rankings, salaries, URLs)

### Update Scholarship Deadlines
Currently, deadlines are in `university_data.json` but not editable in the UI yet. To add:
1. Go to "View JSON"
2. Download the file
3. Edit manually in a text editor
4. Upload back (or just edit the file directly)

---

## 💡 Tips

- **Validation**: The UI prevents invalid data (e.g., negative costs)
- **Real-time**: Changes save immediately to `university_data.json`
- **No backup**: Make sure to backup `university_data.json` before major edits
- **Reload**: The main app reloads automatically when you save changes

---

## 🧪 Testing

### Running Tests

```bash
python test_admin.py
```

### What Gets Tested

1. **JSON Format Validation**
   - Verifies `university_data.json` is valid JSON
   - Can be parsed without errors

2. **Load/Save Operations**
   - `load_json_data()` successfully loads all data
   - `save_json_data()` successfully saves changes
   - Data persists after save/reload cycle

3. **Data Integrity**
   - All universities have required fields
   - All scholarships have required fields
   - All scholarship_availability references are valid
   - No orphaned or missing references

4. **University Editing**
   - Can update university tuition
   - Changes persist after save/reload
   - Original data can be restored

5. **Scholarship Editing**
   - Can update scholarship coverage
   - Changes persist after save/reload
   - Original data can be restored

6. **Add/Remove Operations**
   - Can add new universities
   - Can add new scholarships
   - Can remove entries
   - Data remains consistent

### When to Run Tests

- After adding new universities/scholarships
- After bulk edits
- Before deploying changes
- After updating JSON manually

---

## 📊 Data Structure Overview

### What's Tracked Well

**University Data:**
- Core costs: Tuition, living, duration
- Salary expectations by country
- Rankings: QS, THE, CSRankings, US News
- Career attributes: Visa difficulty, PR path, AI maturity
- Program focus: Research intensity, industry connections
- Regional organization: 4 regions, 32 universities

**Scholarship Data:**
- Coverage: Tuition, living, flights
- Return requirements
- Eligible countries/regions
- Success rates
- Age limits

**Scholarship-University Mapping:**
- Availability matrix per university
- Prevents invalid combinations

### Critical Gaps (Future Work)

**Missing Eligibility Requirements:**
- GPA minimums
- Test score minimums (GRE, IELTS, TOEFL)
- Work experience requirements
- Citizenship restrictions
- Language requirements

**Missing University Admission Requirements:**
- GPA minimums
- Test score minimums
- Research background expectations
- Portfolio/project requirements

**Missing Deadlines:**
- Application deadlines
- Scholarship deadlines
- Decision dates

---

## 🔧 Troubleshooting

**"university_data.json not found"**
- Make sure you're running the admin app from the project root directory

**Changes not appearing in main app**
- Refresh the main app page (Streamlit should auto-reload)
- Check that the JSON file was saved (look at file modification time)

**JSON is corrupted**
- Restore from backup
- Or manually fix the JSON in a text editor

**Test fails with "JSON format error"**
- Check `university_data.json` for syntax errors
- Use a JSON validator: `python -m json.tool university_data.json`

**Test fails with "Missing field"**
- A university or scholarship is missing a required field
- Check the error message for which field is missing
- Add the field to the JSON

---

## 🚧 Future Enhancements

- [ ] Edit deadlines in UI
- [ ] Edit eligibility requirements
- [ ] Edit admission requirements
- [ ] Bulk import from CSV/Excel
- [ ] Undo/redo functionality
- [ ] Change history/audit log
- [ ] Add eligibility filtering
- [ ] Add admission requirements tracking
