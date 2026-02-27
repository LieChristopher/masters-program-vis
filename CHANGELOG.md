# Changelog - AI Master's Assessment Tool

## 2026-02-27 - Update 3: Visual Comparison Matrices

### 🆕 Added

#### New Tab: "📊 Visual Comparison"
Interactive scatter plot matrices for multi-dimensional university comparison.

#### 3 Interactive Matrices

**1. Cost vs Quality Matrix**
- **X-axis:** Total Program Cost (tuition + living × duration)
- **Y-axis:** University Tier (1=Best, 3=Lower)
- **Bubble Size:** Number of available scholarships
- **Color:** Region
- **Purpose:** Identify best value universities
- **Key Insight:** ETH Zurich and Zhejiang Hangzhou = Tier 1 at low cost

**2. Research vs Industry Matrix**
- **X-axis:** Research Intensity (Low → Very High)
- **Y-axis:** Industry Connections (Limited → Excellent)
- **Bubble Size:** Post-graduation salary
- **Color:** Region
- **Quadrants:**
  - Top-Right: Hybrid (MIT, Stanford, CMU, Zhejiang)
  - Bottom-Right: Research-focused (Oxford, Cambridge, Tsinghua)
  - Top-Left: Industry-focused (Imperial, TUM, SUSTech)
- **Purpose:** Match program orientation to career goals
- **Key Insight:** Visualize PhD vs Industry trade-offs

**3. Salary vs Visa Difficulty Matrix**
- **X-axis:** Post-Graduation Salary
- **Y-axis:** Visa Difficulty (Easy → Very Hard)
- **Bubble Size:** Total program cost
- **Color:** Region
- **Purpose:** Assess career feasibility
- **Key Insight:** TUM Munich and NUS = best balance (good salary + easy visa)

#### Interactive Features
- ✅ Hover tooltips with detailed information
- ✅ Zoom and pan functionality
- ✅ Click legend to filter by region
- ✅ Download charts as PNG
- ✅ Annotations for standout universities (ETH, Zhejiang, MIT, Oxford)
- ✅ Quadrant lines for easy interpretation
- ✅ Summary comparison table (sortable by ROI)

#### Summary Comparison Table
- Shows all universities with key metrics
- Sortable by ROI (Return on Investment = Salary - Total Cost)
- Formatted currency columns
- Quick reference for all dimensions

### 🔄 Changed

#### Streamlit App Structure
- Added new tab between "Universities" and "Action Items"
- Renumbered tabs:
  - Tab 1: Scholarships
  - Tab 2: Universities
  - Tab 3: **Visual Comparison** (NEW!)
  - Tab 4: Action Items (was Tab 3)
  - Tab 5: Warnings (was Tab 4)
  - Tab 6: Top Picks (was Tab 5)

#### Dependencies
- Added `plotly` for interactive visualizations
- Added `pandas` for data manipulation
- Updated `requirements.txt`

### 📖 Documentation

#### New File: Visual_Comparison_Guide.md
Comprehensive guide covering:
- How to use each matrix
- What each dimension shows
- Key insights from each matrix
- Example decision flows (4 scenarios)
- Interactive features explanation
- Limitations and considerations
- Step-by-step usage guide

### 🎯 Key Insights from Matrices

**Best Value Universities:**
- ETH Zurich: Tier 1, $47k total, $138k salary (ROI: $91k)
- Zhejiang Hangzhou: Tier 1, $45k total, $62k salary (ROI: $17k)

**Program Orientation:**
- Hybrid (PhD or Industry): MIT, Stanford, CMU, Zhejiang, NUS
- Research-focused (PhD): Oxford, Cambridge, Tsinghua, Peking, SJTU
- Industry-focused (Jobs): Imperial, TUM, SUSTech

**Career Feasibility:**
- Best Balance: TUM Munich (€72k, Easy visa), NUS ($70k, Easy visa)
- High Risk/Reward: USA universities ($140-250k, Very Hard visa)
- Moderate: UK universities (£60-120k, Medium visa)

### 💡 Use Cases

**Scenario 1: Budget-Conscious + PhD**
- Matrix 1: Find Tier 1 under $100k → ETH, Zhejiang, Tsinghua
- Matrix 2: Choose high research → All qualify
- Matrix 3: Check visa → ETH best (high salary)
- **Decision:** ETH Zurich

**Scenario 2: High Salary + Risk-Tolerant**
- Matrix 1: Focus on Tier 1 → MIT, Stanford, CMU
- Matrix 2: Choose hybrid → All qualify
- Matrix 3: Accept Very Hard visa for $200k+
- **Decision:** Stanford

**Scenario 3: Job Immediately + Stability**
- Matrix 1: Moderate budget → TUM, Imperial, NUS
- Matrix 2: Choose excellent industry → All qualify
- Matrix 3: Prioritize Easy visa → TUM or NUS
- **Decision:** TUM Munich

**Scenario 4: LPDP (Path A)**
- Matrix 1: Cost irrelevant, focus Tier 1 → MIT, Oxford, Tsinghua
- Matrix 2: Choose research prestige → Oxford, MIT
- Matrix 3: Visa irrelevant (must return)
- **Decision:** MIT or Oxford

### 📊 Technical Implementation

**Data Transformation:**
- Convert categorical values to numeric for plotting
- Calculate derived metrics (ROI, total cost)
- Create pandas DataFrame for easy manipulation

**Visualization:**
- Plotly Express for scatter plots
- Custom annotations for standout universities
- Quadrant lines for interpretation
- Inverted axes where appropriate (Tier, Visa)

**Performance:**
- Data loaded once from JSON
- Transformed on-demand when tab opened
- Cached by Streamlit for fast re-renders

---

## 2026-02-27 - Update 2: Program Focus (Research vs Industry)

### 🆕 Added

#### Program Focus Attribute (All 16 Universities)
Each university now includes detailed program orientation:
- **Research Intensity**: Very High / High / Medium / Low
- **Industry Connections**: Excellent / Strong / Moderate / Limited
- **Thesis Requirement**: Required / Optional / Capstone
- **Internship Opportunities**: Excellent / Good / Limited
- **Best For**: PhD pipeline / Industry careers / Flexible

#### University Classifications by Focus

**Very High Research (PhD Pipeline):**
- Oxford, Cambridge (UK) - Dissertation required, limited internships
- Tsinghua, Peking, SJTU (China) - Top research + Chinese tech

**High Research (Hybrid - PhD or Industry):**
- MIT, Stanford, CMU (USA) - Research + FAANG recruiting
- ETH Zurich (Switzerland) - Research + Swiss/EU tech
- NUS (Singapore) - Research + Asian tech hub
- Zhejiang, Fudan (China) - Research + Alibaba/finance

**Medium Research (Industry-Focused):**
- Imperial (UK) - London tech scene
- TUM Munich (Germany) - Applied engineering
- Erasmus EMAI (EU) - Multi-country experience
- SUSTech (China) - Shenzhen startups/hardware

### 🔄 Changed

#### Streamlit App Updates
1. **Universities Tab - Comparison Table**:
   - Added "Research" column (research intensity)
   - Added "Industry" column (industry connections)
   - Replaced "AI Maturity" and "Language" with "Best For"
   - More focused on program orientation

2. **Career Attributes Legend**:
   - Added Research Intensity explanation
   - Added Industry Connections explanation
   - Added Program Best For guidance
   - Added Thesis Requirement explanation
   - Added decision framework (PhD vs Industry)

3. **Financial Calculator - Program Focus Section**:
   - New section showing program orientation
   - 3 metrics: Research Intensity, Industry Connections, Thesis
   - Visual indicators (✅ Good for PhD / ✅ Good for jobs)
   - "Best For" summary

### 📖 Documentation

#### New File: Program_Focus_Guide.md
Comprehensive guide covering:
- Why program focus matters
- University classifications (Very High / High / Medium research)
- Decision framework (Research vs Industry vs Hybrid)
- Regional patterns (USA, UK, Europe, China, Singapore)
- Special considerations for Indonesian students
- Quick reference table for all 16 universities
- Action items for choosing

### 🎯 Key Insights

**For Indonesian Students:**

**Path A (LPDP - Return to Indonesia):**
- Research prestige matters MORE
- Indonesian employers value university name
- **Recommendation:** Research-focused or Hybrid
- **Best:** MIT, Stanford, Oxford, Cambridge, Tsinghua

**Path B (International Career):**
- Industry connections matter MORE
- Practical skills + internships = job offers
- **Recommendation:** Industry-focused or Hybrid
- **Best:** MIT, Stanford, CMU, Imperial, NUS, Zhejiang

**Considering PhD Later:**
- Publications during Master's help PhD applications
- **Recommendation:** Research-focused or Hybrid
- **Best:** MIT, Stanford, Oxford, ETH, Tsinghua, SJTU

### 📊 Program Focus Summary

| Focus Level | Universities | Best For | Pros | Cons |
|-------------|--------------|----------|------|------|
| Very High Research | Oxford, Cambridge, Tsinghua, Peking, SJTU | PhD pipeline | Deep theory, publications | Fewer internships |
| High Research (Hybrid) | MIT, Stanford, CMU, ETH, NUS, Zhejiang, Fudan | PhD or Industry | Best of both | May need to choose track |
| Medium Research (Industry) | Imperial, TUM, Erasmus, SUSTech | Industry careers | Job-ready, internships | Less PhD prep |

---

## 2026-02-27 - Update 1: Major Update: China Universities & Career Attributes

### 🆕 Added

#### 6 Chinese Universities (City-Level Breakdown)
1. **Tsinghua University** (Beijing, Tier 1)
   - Top AI program globally
   - $75k salary, $24k/year living cost
   - Companies: Baidu, ByteDance, Xiaomi

2. **Peking University** (Beijing, Tier 1)
   - Elite university
   - $72k salary, $24k/year living cost
   - Companies: Baidu, ByteDance, Xiaomi

3. **Fudan University** (Shanghai, Tier 1)
   - Top-tier program
   - $68k salary, $24k/year living cost
   - Companies: Alibaba Cloud, International firms

4. **Shanghai Jiao Tong University** (Shanghai, Tier 1)
   - Tied #1 globally in AI research output
   - $68k salary, $24k/year living cost
   - Companies: Alibaba Cloud, International firms

5. **Zhejiang University** (Hangzhou, New Tier 1) ⭐ BEST VALUE
   - Tied #3 with CMU in AI rankings
   - $62k salary, $18k/year living cost (30% cheaper!)
   - Companies: Alibaba HQ, E-commerce startups
   - Beautiful city, great quality of life

6. **SUSTech** (Shenzhen, Tier 1)
   - Young, innovative university
   - $68k salary, $22k/year living cost
   - Companies: Tencent, Huawei, DJI

#### Career Attributes (All Universities)
Each university now includes:
- **Salary Tier**: Highest / High / Medium-High / Medium
- **Visa Difficulty**: Easy / Medium / Hard / Very Hard
- **AI Maturity**: Tier 1 / Tier 2 / Tier 3
- **Path to PR**: Timeline and difficulty
- **Work Language**: English / Mandarin / etc.

#### Regional Structure
- **North America**: USA, Canada
- **Europe**: UK, Germany, Switzerland, Netherlands, France, Sweden
- **China**: Broken down by city tier (Tier 1, New Tier 1, Tier 2)
- **Asia-Pacific**: Singapore, Australia, NZ, Japan, Korea, ASEAN countries (combined)
- **Middle East**: UAE, Saudi Arabia, Qatar

#### Chinese Government Scholarship (CSC)
- Full tuition coverage
- ¥3,000-3,500/month stipend
- Available for all Chinese universities
- No return requirement
- Medium success rate

### 🔄 Changed

#### Streamlit App Updates
1. **Region Filter** in sidebar (replaces country filter)
   - Filter by: North America, Europe, China, Asia-Pacific, Middle East
   - Sub-filter by country/city within region

2. **Universities Tab** - New Features:
   - Region filter dropdown
   - Detailed comparison table with career attributes
   - Career attributes legend/explanation
   - China city-level comparison table
   - City tier information for Chinese universities

3. **Financial Calculator** - Enhanced:
   - Shows region in program description
   - Career outlook section with 4 metrics:
     - Salary tier + actual salary
     - Visa difficulty
     - AI maturity
     - Path to PR + work language
   - China-specific city details (companies, pros/cons)

4. **Data Structure**:
   - All universities have `region` field
   - All scholarships have `eligible_regions` field
   - Chinese universities have `city_tier` and `city_details`

### 📊 Statistics

**Before:**
- 10 universities
- 13 scholarships
- 3 regions (implicit)

**After:**
- 16 universities (+6 Chinese)
- 14 scholarships (+1 CSC)
- 5 explicit regions with characteristics
- Career attributes for all universities
- City-level breakdown for China

### 🎯 Key Insights

#### Best Value Options:
1. **Zhejiang University (Hangzhou)** - Top AI program at 30% lower cost than Beijing
2. **ETH Zurich** - Highest salary ($138k) with minimal tuition
3. **TUM Munich** - Affordable with easy visa path

#### China City Tiers:
- **Tier 1** (Beijing, Shanghai, Shenzhen): $24k/year living, $68-75k salary
- **New Tier 1** (Hangzhou, Nanjing): $18k/year living, $62k salary (30% cheaper!)
- **Tier 2** (Xi'an, Hefei): $14-16k/year living, $50-55k salary (most affordable)

#### Visa Difficulty Rankings:
- **Easy**: Germany, Singapore, Canada, Australia
- **Medium**: UK, Netherlands, Switzerland
- **Hard**: China, Switzerland (PR)
- **Very Hard**: USA (H-1B lottery)

### 📝 TODO Updates

Added to TODO.md:
- Chinese universities research section
- CSC scholarship details
- China city cost comparisons
- Visa/immigration details for China
- Salary research for China

### 🔗 References Added

Added 8 new references to AI_Masters_References.md:
- Zhejiang University AI rankings (4 sources)
- China cost of living comparisons (4 sources)

---

## Previous Updates

### 2026-02-27 - Initial Release
- Created comprehensive assessment tool
- 10 universities (USA, UK, Europe, Singapore)
- 13 scholarships
- 3 career paths (A, B, C)
- Modular code structure
- JSON as single source of truth

---

**Last Updated:** 2026-02-27
**Version:** 2.0
