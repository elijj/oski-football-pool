# 🏈 Weekly Football Pool Workflow

## 🚀 Quick Start (5 minutes)

### 1. Generate Research Prompt
```bash
football-pool prompt 1 --enhanced
```
**Output**: Comprehensive prompt with real odds data + web search context

### 2A. Automated Analysis (Recommended)
```bash
football-pool analyze-llm 1
```
**What it does**:
- Uses free OpenRouter models automatically
- Saves analysis to `week_1_llm_analysis.json`
- Imports directly into system

### 2B. Manual Analysis (Alternative)
1. **Copy the generated prompt** from step 1
2. **Paste into your preferred LLM** (ChatGPT, Claude, Gemini, etc.)
3. **Get JSON response** in the required format
4. **Save as `week_1_llm.json`**
5. **Import into system**:
   ```bash
   football-pool import-llm 1 week_1_llm.json
   ```

### 2C. Combined Analysis (Best of Both Worlds!)
```bash
# Get automated analysis AND combine with manual
football-pool combine-analyses 1 --automated --manual week_1_manual.json

# Or just combine multiple manual analyses
football-pool combine-analyses 1 --manual week_1_chatgpt.json --manual week_1_claude.json

# Choose combination method:
football-pool combine-analyses 1 --method average    # Average all values
football-pool combine-analyses 1 --method weighted   # Weight by confidence
football-pool combine-analyses 1 --method best       # Use highest confidence
```

### 3. Generate Optimal Picks
```bash
football-pool picks 1
```
**Output**: Ranked picks with confidence points and strategy

### 4. Generate Final Report
```bash
football-pool report 1
```
**Output**: Formatted picks ready for pool submission

---

## 🔀 Combination Methods

### **Average Method** (Default)
- Averages all numerical values (spreads, percentages, confidence)
- Combines text fields (injuries, weather) with unique values
- Best for: Getting consensus from multiple sources

### **Weighted Method**
- Weights values by confidence scores
- Higher confidence analyses have more influence
- Best for: When you trust some analyses more than others

### **Best Method**
- Uses the analysis with highest confidence score
- Takes all values from the "best" analysis
- Best for: When you want the most confident single analysis

## 💡 Pro Tips

1. **Use combined analysis** for maximum insight from multiple sources
2. **Try different combination methods** to see which works best
3. **Save individual analyses** before combining for comparison
4. **Review picks manually** before submission
5. **Track competitors** for edge analysis
6. **Submit early** to avoid deadline pressure

## 📋 Pre-Submission Checklist

- [ ] **Research completed** (automated or manual)
- [ ] **Analysis imported** into system
- [ ] **Picks generated** and reviewed
- [ ] **All 20 games covered** with confidence points 1-20
- [ ] **Strategy appropriate** for your position
- [ ] **Report generated** for submission
- [ ] **Picks submitted** before deadline

## 🔧 Troubleshooting

### No API Keys
```bash
# Check API usage
football-pool api-usage

# Set up .env file
cp .env.example .env
# Edit .env with your API keys
```

### Web Search Issues
```bash
# Test web search
football-pool test-web-search 1

# Clear cache if needed
football-pool clear-cache
```

### Pick Generation Errors
```bash
# Check system status
football-pool stats

# Verify analysis was imported
football-pool import-llm 1 week_1_llm.json
```

---

## 📞 Support

- **System status**: `football-pool stats`
- **API usage**: `football-pool api-usage`
- **Help**: `football-pool --help`
- **Test web search**: `football-pool test-web-search 1`

**Total time**: 5-60 minutes depending on analysis method chosen.
