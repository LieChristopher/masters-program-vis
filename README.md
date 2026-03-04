# AI Master's Assessment Tool

**Last Updated:** 2026-03-05  
**Status:** ✅ Production Ready

A Streamlit app to help Indonesian students find and compare AI Master's programs and scholarships worldwide.

---

## 📁 Project Structure

```
Masters/
├── streamlit_app.py              # Main app (827 lines)
├── data/                         # All data files
│   ├── university_data.json      # Universities & scholarships
│   ├── exchange_rates.json       # Currency conversion rates
│   ├── countries.json            # Country metadata
│   ├── deadlines.json            # Application deadlines
│   └── eligibility.json          # Eligibility requirements
├── utils/                        # Helper modules
│   ├── data_loader.py           # JSON loading
│   ├── assessment.py            # Scoring & tier logic
│   └── admin.py                 # Admin panel
├── tests/                        # Test suite
│   ├── test_app.py              # Core logic tests
│   └── test_admin.py            # Admin tests
├── docs/                         # Documentation
│   ├── ADMIN_GUIDE.md
│   ├── Rankings_and_Sources.md
│   ├── Scholarships_for_Indonesian_Students.md
│   └── ... (4 more)
├── README.md
└── ROADMAP.md
```

---

## 🚀 Quick Start

```bash
# Install dependencies
pip install streamlit plotly pandas

# Run the app
streamlit run streamlit_app.py

# Run tests
python tests/test_app.py
python tests/test_admin.py
```

---

## 🎯 Features

### 4 Tabs:
1. **📊 Overview** - Assessment results, top picks, action items, warnings
2. **💰 Scholarships** - List with eligibility filters
3. **🏛️ Universities** - By region, with China city comparison
4. **💵 Calculator** - Standalone cost calculator with smart defaults

### Core Functions:
- **Instant Results** - Data shows immediately with prefilled defaults
- **Live Updates** - Change profile → recommendations update instantly
- **Profile Assessment** - Competitiveness score (0-100), tier recommendation
- **Path Recommendations** - Path A (LPDP), Path B (International), Path C (Hybrid)
- **Financial Calculator** - Cost breakdown with USD + IDR, budget check, ROI
- **Admin Panel** - Edit universities and scholarships with table views

---

## 📊 Data

### Coverage:
- **15 Universities** (core set, expandable to 32)
- **6 Scholarships** (LPDP, Chevening, Australia Awards, Erasmus Mundus, DAAD, No Scholarship)
- **4 Regions** (North America, Europe, Asia, Asia-Pacific)
- **10 Currencies** (USD, EUR, GBP, CHF, CAD, AUD, SGD, CNY, etc.)

### Currency System:
- **Storage:** Local currency (CHF, EUR, CNY, etc.)
- **Conversion:** Single rate table (`rates_to_idr`)
- **Display:** USD (primary) + IDR (secondary)

Example:
```
ETH Zurich: CHF 1,400/year
  → Rp 25,200,000 (CHF × 18,000)
  → $1,575 (Rp ÷ 16,000)
  → Display: "$1,575 (≈ Rp 25,200,000)"
```

---

## 📝 How to Update Data

### Edit Universities:
1. Use **Admin Panel**:
   - Scroll to bottom of sidebar
   - Check "🔧 Admin Mode" checkbox
   - Select operation from Admin Menu
2. Or edit `data/university_data.json` directly

### Currency Structure:
```json
"tuition_per_year": {
  "amount": 1400,
  "currency": "CHF"
}
```

### Update Exchange Rates:
Edit `data/exchange_rates.json`:
```json
"rates_to_idr": {
  "USD": 16000,
  "CHF": 18000,
  "EUR": 17600
}
```

---

## 🎓 Key Insights

### Best Fully-Funded Options:
1. **LPDP** - Highest success rate, must return 2+ years
2. **Erasmus Mundus EMAI** - 15 scholarships, no return
3. **DAAD** - Germany, good success rate
4. **Australia Awards** - Must return 2+ years
5. **Chevening** - UK, requires 2,800 work hours

### Best Value Universities:
- **ETH Zurich** - $47k total, $138k salary
- **TUM Munich** - $54k total, €72k salary
- **Zhejiang University** - $45k total, $62k salary

### Salary Expectations:
- USA: $140k-$250k
- Switzerland: $138k
- UK: $75k-$150k
- Germany: $72k
- China: $62k-$75k
- Indonesia: $30k

---

## 🔧 Technical Stack

- **Frontend:** Streamlit
- **Visualizations:** Plotly
- **Data:** JSON (local currency → IDR → USD)
- **Caching:** Streamlit @cache_data
- **Tests:** Python unittest-style

---

## 📚 Documentation

See `docs/` folder:
- **ADMIN_GUIDE.md** - How to use admin panel
- **Rankings_and_Sources.md** - University rankings explained
- **Scholarships_for_Indonesian_Students.md** - Indonesian scholarships
- **Universal_Scholarships_AI_Masters.md** - Non-Indonesian scholarships

---

## ✅ Recent Changes (2026-03-05)

### Major Refactoring:
- ❌ Removed profile save/load (unnecessary)
- ❌ Removed Decision Tree tab (Mermaid issues)
- ❌ Removed "Generate Assessment" button (instant results now)
- ✅ Refactored to 4 tabs (was 6)
- ✅ Calculator now standalone with smart defaults
- ✅ Profile prefilled - live updates
- ✅ Added budget check and ROI to calculator
- ✅ Admin panel has table views

### Result:
- **Main App:** 1,613 → 827 lines (-49%)
- **Total Code:** ~2,000 lines (including utils + tests)
- **Tabs:** 6 → 4 tabs
- **UX:** Instant results, no friction

---

## 🗺️ Next Steps

See `ROADMAP.md` for detailed TODO list.

**Immediate:**
- Fill in deadlines and eligibility data
- Verify all costs are current (2026-2027)
- Test end-to-end with real profile

---

## 📞 Support

- **Data issues:** Edit `data/university_data.json` or use Admin Panel
- **Currency rates:** Edit `data/exchange_rates.json`
- **Questions:** Check `docs/` folder

---

**Version:** 3.0  
**License:** Personal Use
