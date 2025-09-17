# Weekly Workflow Command - Complete Automation

## 🚀 **ENHANCED WORKFLOW WITH MULTI-LLM INTEGRATION**

You now have **TWO powerful workflow options** for maximum earnings:

### **Option 1: Enhanced Multi-LLM Workflow (RECOMMENDED)**
```bash
football-pool enhanced-weekly-workflow <week> <date>
```

### **Option 2: Standard Workflow**
```bash
football-pool weekly-workflow <week> <date>
```

## 🎯 **WHAT EACH WORKFLOW DOES**

### **Enhanced Multi-LLM Workflow** (RECOMMENDED)
1. **Generates contrarian analysis prompt**
2. **Integrates multiple LLM analyses** (Grok + ChatGPT5)
3. **Creates consensus picks** from multiple perspectives
4. **Updates Excel with consensus picks**
5. **Generates comprehensive CSV**
6. **Creates enhanced strategy report**
7. **Provides complete summary**

### **Standard Workflow**
1. **Generates contrarian analysis prompt**
2. **Updates Excel with picks**
3. **Creates strategy report**
4. **Generates next week preview**
5. **Provides complete summary**

## 📋 **USAGE EXAMPLES**

### **Enhanced Multi-LLM Workflow (RECOMMENDED):**
```bash
# Complete enhanced workflow for Week 1
football-pool enhanced-weekly-workflow 1 2025-09-17

# Skip multi-LLM analysis if you prefer single analysis
football-pool enhanced-weekly-workflow 1 2025-09-17 --no-multi-llm
```

### **Standard Workflow:**
```bash
# Generate everything for Week 1
football-pool weekly-workflow 1 2025-09-17

# Generate everything for Week 2
football-pool weekly-workflow 2 2025-09-24
```

### **With Analysis File:**
```bash
# Use existing analysis
football-pool weekly-workflow 1 2025-09-17 --analysis data/json/week_1_complete_contrarian_analysis.json
```

### **Without LLM Enhancement:**
```bash
# Skip LLM analysis
football-pool weekly-workflow 1 2025-09-17 --no-llm
```

### **Skip Picks Generation:**
```bash
# Skip generating picks (use existing analysis only)
football-pool weekly-workflow 1 2025-09-17 --skip-picks
```

## 🔄 **ENHANCED MULTI-LLM WORKFLOW PROCESS**

### **Step 1: Generate Contrarian Prompt**
- Creates contrarian analysis prompt
- Saves to `data/prompts/{date}_contrarian_prompt.txt`
- **MANUAL STEP**: Copy prompt to Grok and ChatGPT5, save outputs as:
  - `data/json/{date}_contrarian_prompt_grok.json`
  - `data/json/{date}_contrarian_prompt_chatgpt5.json`

### **Step 2: Multi-LLM Analysis Integration**
- Automatically detects both LLM analysis files
- Combines insights using consensus strategy
- Generates 20 consensus picks with confidence points
- Saves to `data/json/week_{week}_multi_llm_analysis.json`

### **Step 3: Update Excel with Consensus Picks**
- Updates Excel file with consensus picks
- Saves to `data/excel/Dawgpac25_{date}.xlsx`
- Ready for pool submission

### **Step 4: Generate Comprehensive CSV**
- Creates detailed CSV with all metadata
- Saves to `data/excel/Week_{week}_Picks_{date}.csv`
- Includes all analysis factors

### **Step 5: Generate Enhanced Strategy Report**
- Creates comprehensive markdown report
- Saves to `reports/Week_{week}_Enhanced_Strategy_Report_{date}.md`
- Includes multi-LLM insights and consensus reasoning

### **Step 6: Complete Summary**
- Shows all generated files
- Provides next steps
- Highlights competitive edge from multiple LLMs

## 🔄 **STANDARD WORKFLOW PROCESS**

### **Step 1: Generate Contrarian Prompt**
- Creates contrarian analysis prompt
- Saves to `data/prompts/{date}_contrarian_prompt.txt`
- Provides instructions for manual LLM step

### **Step 2: Update Excel with Analysis**
- Updates Excel file with contrarian picks
- Saves to `data/excel/Dawgpac25_{date}.xlsx`
- Ready for pool submission

### **Step 3: Generate Strategy Report**
- Creates comprehensive markdown report
- Saves to `reports/Week_{week}_Strategy_Report_{date}.md`
- Includes all picks, reasoning, and analysis

### **Step 4: Generate Next Week Preview**
- Creates next week considerations
- Saves to `reports/Week_{week+1}_Preview_{next_date}.md`
- Provides future planning insights

### **Step 5: Complete Summary**
- Shows all generated files
- Provides next steps
- Highlights competitive edge

## 🎯 **EXACT COMMANDS FOR YOUR WORKFLOW**

### **For Week 1 (Your Current Setup):**

#### **Step 1: Generate Prompt**
```bash
football-pool prompt 1 --date 2025-09-17
```
**Result**: Creates `data/prompts/2025-09-17_contrarian_prompt.txt`

#### **Step 2: Manual LLM Analysis**
1. Copy the prompt to **Grok** → Save output as `data/json/2025-09-17_contrarian_prompt_grok.json`
2. Copy the prompt to **ChatGPT5** → Save output as `data/json/2025-09-17_contrarian_prompt_chatgpt5.json`

#### **Step 3: Enhanced Multi-LLM Workflow (ONE COMMAND)**
```bash
football-pool enhanced-weekly-workflow 1 --date 2025-09-17
```
**Result**: Complete automation with consensus picks from both LLMs

### **For Future Weeks:**
```bash
# Generate prompt for Week 2
football-pool prompt 2 --date 2025-09-24

# After manual LLM analysis, run enhanced workflow
football-pool enhanced-weekly-workflow 2 --date 2025-09-24
```

## 📁 **GENERATED FILES**

### **Enhanced Multi-LLM Workflow Output:**
```
📁 Generated Files:
  📝 Contrarian Prompt: data/prompts/2025-09-17_contrarian_prompt.txt
  🤖 Multi-LLM Analysis: data/json/week_1_multi_llm_analysis.json
  📊 Excel File: data/excel/Dawgpac25_2025-09-17.xlsx
  📈 Comprehensive CSV: data/excel/Week_1_Picks_2025-09-17.csv
  📋 Enhanced Strategy Report: reports/Week_1_Enhanced_Strategy_Report_2025-09-17.md
```

### **Standard Workflow Output:**
```
📁 Generated Files:
  📝 Contrarian Prompt: data/prompts/2025-09-17_contrarian_prompt.txt
  📊 Excel File: data/excel/Dawgpac25_2025-09-17.xlsx
  📋 Strategy Report: reports/Week_1_Strategy_Report_2025-09-17.md
  🔍 Next Week Preview: reports/Week_2_Preview_2025-09-24.md
```

## 🎯 **WORKFLOW SCENARIOS**

### **Scenario 1: First Time (No Analysis)**
```bash
football-pool weekly-workflow 1 2025-09-17
```
**Result**: Generates prompt, shows manual step required, continues with standard picks

### **Scenario 2: With Analysis File**
```bash
football-pool weekly-workflow 1 2025-09-17 --analysis data/json/week_1_complete_contrarian_analysis.json
```
**Result**: Complete workflow with contrarian analysis

### **Scenario 3: LLM Enhanced**
```bash
football-pool weekly-workflow 1 2025-09-17 --llm
```
**Result**: Enhanced report with LLM insights for next week

## 🚀 **NEXT STEPS AFTER COMMAND**

The command provides clear next steps:

```
🚀 Next Steps:
1. Review the strategy report for your picks
2. Submit the Excel file to your pool
3. Use the next week preview for future planning
4. Track results and refine strategy
```

## 💰 **COMPETITIVE EDGE**

The command highlights your advantages:

```
💰 Competitive Edge:
✅ Contrarian analysis for differentiation
✅ Value plays for maximum earnings
✅ Risk management with confidence points
✅ Future planning with next week insights
```

## 🔧 **COMMAND OPTIONS**

### **Required Arguments:**
- `week`: Week number (1-18)
- `date`: Date in YYYY-MM-DD format

### **Optional Arguments:**
- `--llm/--no-llm`: Use LLM for enhanced analysis (default: --llm)
- `--skip-picks`: Skip generating picks (use existing analysis)
- `--analysis`: Path to existing analysis JSON file

## 📊 **EXAMPLE OUTPUT**

```
🚀 Starting COMPLETE WEEKLY WORKFLOW for Week 1 (2025-09-17)
================================================================================

📝 Step 1: Generating contrarian analysis prompt...
✅ Contrarian prompt saved: data/prompts/2025-09-17_contrarian_prompt.txt
💡 Copy this prompt to ChatGPT/Claude/Gemini and get JSON response

📊 Step 2: Updating Excel with contrarian analysis...
✅ Excel file updated: data/excel/Dawgpac25_2025-09-17.xlsx

📋 Step 3: Generating strategy report...
✅ Strategy report generated: reports/Week_1_Strategy_Report_2025-09-17.md

🔍 Step 4: Generating next week preview...
✅ Next week preview generated: reports/Week_2_Preview_2025-09-24.md

================================================================================
🎯 WEEKLY WORKFLOW COMPLETE!
================================================================================
```

## 🎯 **BENEFITS**

### **1. Single Command**
- **One command** generates everything
- **No manual steps** required (except LLM analysis)
- **Complete automation** of weekly workflow

### **2. Comprehensive Output**
- **Contrarian prompt** for LLM analysis
- **Excel file** ready for pool submission
- **Strategy report** with complete documentation
- **Next week preview** for future planning

### **3. Flexible Options**
- **With/without LLM** enhancement
- **Custom analysis** files
- **Skip options** for specific needs

### **4. Professional Documentation**
- **Markdown reports** for easy reading
- **Clear structure** and organization
- **Future planning** insights

## 🚀 **READY FOR MAXIMUM EARNINGS**

The weekly workflow command is the ultimate tool for pool domination:

- **Complete automation** of weekly tasks
- **Contrarian analysis** for differentiation
- **Professional documentation** for strategy
- **Future planning** for continuous improvement

**One command, complete weekly strategy!** 🎯💰

---
*Last Updated: 2025-01-27*
*Status: Weekly workflow command fully implemented*
