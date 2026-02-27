# Streamlit App - Profile Save/Load Guide

**Last Updated:** 2026-02-27

---

## ✅ Features Added

The Streamlit app now has **profile save/load functionality**!

### What It Does:

1. **💾 Save Profile Button**
   - Saves all your current inputs to `my_profile.json`
   - Includes: GPA, English scores, work experience, career goals, financial info
   - Updates automatically with timestamp

2. **📂 Load Profile Button**
   - Loads your saved profile from `my_profile.json`
   - Restores all your previous inputs
   - Shows success/warning message

3. **🔄 Auto-Load on Start**
   - App automatically loads your profile when you open it
   - No need to manually load every time
   - Your settings are remembered!

---

## 🚀 How to Use

### First Time Setup:

1. **Open the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Fill in your profile:**
   - Academic info (GPA, English scores)
   - Work experience
   - Financial situation
   - Career goals

3. **Click "💾 Save Profile"**
   - Your data is saved to `my_profile.json`
   - You'll see "✅ Profile saved!" message

### Next Time:

1. **Open the app:**
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Your profile loads automatically!**
   - All your previous inputs are restored
   - No need to re-enter everything

3. **Make changes if needed:**
   - Update any fields
   - Click "💾 Save Profile" again to update

### Manual Load:

If you want to reload from file:
- Click "📂 Load Profile" button
- Useful if you edited `my_profile.json` manually

---

## 📁 Files

### my_profile.json
- **Location:** Same directory as `streamlit_app.py`
- **Format:** JSON (machine-readable)
- **Created:** Automatically when you click "Save Profile"
- **Updated:** Every time you click "Save Profile"

### What Gets Saved:

```json
{
  "profile": {
    "academic": {
      "gpa": 3.8,
      "ielts": 7.5,
      "toefl": 0
    },
    "work_experience": {
      "years": 2.0,
      "total_hours": 4000
    },
    "career_goals": {
      "location": "Flexible",
      "willing_to_return": true
    },
    "financial": {
      "can_self_fund": false,
      "budget": 0
    }
  },
  "metadata": {
    "last_updated": "2026-02-27"
  }
}
```

---

## 💡 Tips

### Editing Profile Manually:

You can edit `my_profile.json` directly:
1. Open `my_profile.json` in a text editor
2. Change values (keep JSON format valid!)
3. Save the file
4. Click "📂 Load Profile" in the app

### Multiple Profiles:

Want to save different scenarios?
1. Save your current profile
2. Copy `my_profile.json` to `my_profile_backup.json`
3. Change inputs and save again
4. Swap files to switch between profiles

### Sharing Profiles:

You can share your profile with others:
1. Copy `my_profile.json`
2. Send to someone else
3. They place it in their directory
4. App loads it automatically

---

## 🔧 Technical Details

### Profile Structure:

The app saves these fields:
- **Personal:** Name, age (if added to sidebar)
- **Academic:** GPA, IELTS, TOEFL
- **Work:** Years of experience, total hours
- **Career:** Location preference, return willingness
- **Financial:** Self-funding capability, budget

### Session State:

The app uses Streamlit's session state to:
- Store loaded profile data
- Persist across reruns
- Initialize input widgets with saved values

### Auto-Load Logic:

```python
# On app start
if 'profile' not in st.session_state:
    st.session_state['profile'] = load_profile()

# Initialize widgets
gpa = st.slider("GPA", 
    value=loaded['profile']['academic']['gpa'] if loaded else 3.5)
```

---

## ⚠️ Important Notes

### File Location:
- `my_profile.json` must be in the **same directory** as `streamlit_app.py`
- If you move the app, move the profile file too

### JSON Format:
- Must be valid JSON
- Use double quotes, not single quotes
- No trailing commas
- Validate at jsonlint.com if unsure

### Privacy:
- Profile is stored **locally** on your computer
- Not uploaded anywhere
- Keep it private (contains your personal data)

---

## 🐛 Troubleshooting

### "No saved profile found"
- You haven't saved a profile yet
- Click "💾 Save Profile" first
- Or `my_profile.json` is missing/moved

### "Error saving profile"
- Check file permissions
- Make sure directory is writable
- Close any programs that might have the file open

### Profile doesn't load
- Check JSON format is valid
- Look for error messages in the app
- Try deleting `my_profile.json` and saving fresh

### Values don't update
- Click "📂 Load Profile" to force reload
- Or refresh the page (Ctrl+R / Cmd+R)
- Check `my_profile.json` was actually updated

---

## 🎯 Next Steps

1. **Fill in your profile** in the app
2. **Click "💾 Save Profile"**
3. **Close and reopen** the app to test auto-load
4. **Update as needed** and save again

Your profile is now persistent across sessions!

---

**Version:** 1.0
**Compatible with:** Streamlit app v2.0+
