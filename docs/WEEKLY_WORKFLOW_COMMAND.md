# Weekly Workflow Command - Complete Automation

## 🚀 **SINGLE COMMAND FOR EVERYTHING**

Yes! There is now a single command that generates everything you need for the week:

```bash
football-pool weekly-workflow <week> <date>
```

## 🎯 **WHAT IT DOES**

The `weekly-workflow` command is the ultimate convenience command that:

1. **Generates contrarian analysis prompt**
2. **Updates Excel with picks**
3. **Creates strategy report**
4. **Generates next week preview**
5. **Provides complete summary**

## 📋 **USAGE EXAMPLES**

### **Basic Usage:**
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

## 🔄 **COMPLETE WORKFLOW**

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

## 📁 **GENERATED FILES**

After running the command, you get:

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
