# 🚀 Quick Start: Multi-LLM Enhanced Workflow

## **Your Weekly Commands (Exactly What to Run)**

### **Step 1: Generate Contrarian Prompt**
```bash
football-pool prompt 1 --date 2025-09-17
```
**What it does**: Creates the contrarian analysis prompt
**Output**: `data/prompts/2025-09-17_contrarian_prompt.txt`

### **Step 2: Manual LLM Analysis (5 minutes)**
1. **Copy the prompt** from `data/prompts/2025-09-17_contrarian_prompt.txt`
2. **Paste into Grok** → Get JSON response → Save as `data/json/2025-09-17_contrarian_prompt_grok.json`
3. **Paste into ChatGPT5** → Get JSON response → Save as `data/json/2025-09-17_contrarian_prompt_chatgpt5.json`

### **Step 3: Enhanced Multi-LLM Workflow (ONE COMMAND)**
```bash
football-pool enhanced-weekly-workflow 1 --date 2025-09-17
```
**What it does**:
- ✅ Combines Grok + ChatGPT5 analyses
- ✅ Creates consensus picks
- ✅ Updates Excel file
- ✅ Generates comprehensive CSV
- ✅ Creates enhanced strategy report
- ✅ Provides complete summary

## **🎯 That's It! You're Done!**

### **What You Get:**
- 📊 **Excel file ready for pool submission**: `data/excel/Dawgpac25_2025-09-17.xlsx`
- 📈 **Comprehensive CSV with all metadata**: `data/excel/Week_1_Picks_2025-09-17.csv`
- 📋 **Enhanced strategy report**: `reports/Week_1_Enhanced_Strategy_Report_2025-09-17.md`
- 🤖 **Multi-LLM consensus analysis**: `data/json/week_1_multi_llm_analysis.json`

### **For Future Weeks:**
```bash
# Week 2
football-pool prompt 2 --date 2025-09-24
# [Manual LLM step]
football-pool enhanced-weekly-workflow 2 --date 2025-09-24

# Week 3
football-pool prompt 3 --date 2025-10-01
# [Manual LLM step]
football-pool enhanced-weekly-workflow 3 --date 2025-10-01
```

## **🎯 Why This is Powerful:**

1. **Multiple LLM Perspectives**: Grok + ChatGPT5 = Better insights
2. **Consensus Picks**: Games mentioned by both LLMs get higher confidence
3. **Complete Automation**: One command does everything after manual LLM step
4. **Professional Output**: Excel, CSV, and reports ready for submission
5. **Competitive Edge**: Multi-LLM analysis gives you better picks than single LLM

## **💡 Pro Tips:**

- **Always use both Grok and ChatGPT5** for maximum consensus
- **The enhanced workflow automatically detects** your LLM files
- **Consensus picks are weighted** - games mentioned by both LLMs get higher confidence
- **All outputs are organized** in clean directories
- **One command generates everything** you need for the week

## **🚀 Ready to Dominate Your Pool!**

Your workflow is now:
1. **Generate prompt** (1 command)
2. **Get LLM analyses** (5 minutes manual)
3. **Run enhanced workflow** (1 command)
4. **Submit to pool** (done!)

**Maximum earnings with minimum effort!** 🎯💰
