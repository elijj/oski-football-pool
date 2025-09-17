# 🚀 Quick Reference Card

## **Most Common Commands**

### **🎯 Contrarian Strategy (Recommended)**
```bash
# 1. Generate contrarian prompt
football-pool contrarian-prompt 2025-09-17

# 2. Copy to ChatGPT/Claude, get JSON response
# 3. Update Excel with contrarian picks
football-pool excel-update 1 --date "2025-09-17" --analysis contrarian_analysis.json

# 4. Validate picks
football-pool excel-validate 1 --date "2025-09-17"
```

### **🤖 Automated Analysis**
```bash
# Get LLM analysis
football-pool analyze-llm 3 --model "moonshotai/kimi-k2:free"

# Update Excel
football-pool excel-update 3 --date "2025-09-17" --analysis analysis.json
```

### **🔄 Multi-Analysis (Best Results)**
```bash
# Get multiple analyses
football-pool analyze-llm 3 --model "moonshotai/kimi-k2:free"
football-pool analyze-llm 3 --model "deepseek/deepseek-chat-v3.1:free"

# Combine analyses
football-pool combine-analyses 3 \
  --manual manual_chatgpt.json \
  --manual manual_claude.json \
  --method weighted

# Update Excel with combined analysis
football-pool excel-update 3 --analysis combined_analysis.json
```

### **📊 Monitoring & Debugging**
```bash
# Check system status
football-pool stats

# View logs
football-pool logs

# Check API usage
football-pool api-usage

# Search logs for errors
football-pool logs search --query "ERROR"
```

## **Command Categories**

| Category | Commands | Purpose |
|----------|----------|---------|
| **Analysis** | `contrarian-prompt`, `analyze-llm`, `combine-analyses` | Generate and combine analyses |
| **Excel** | `excel-update`, `excel-validate`, `excel-submit` | Excel automation |
| **Monitoring** | `logs`, `api-usage`, `stats` | System monitoring |
| **Automation** | `auto-workflow`, `create-config` | Automated workflows |

## **Common Options**

| Option | Short | Purpose | Example |
|--------|-------|---------|---------|
| `--date` | `-d` | Date suffix | `--date "2025-09-17"` |
| `--analysis` | `-a` | Analysis file | `--analysis contrarian.json` |
| `--model` | `-m` | LLM model | `--model "moonshotai/kimi-k2:free"` |
| `--method` | | Combination method | `--method weighted` |
| `--output` | `-o` | Save to file | `--output prompt.txt` |

## **Troubleshooting**

| Issue | Solution |
|-------|----------|
| Command not found | `source venv/bin/activate` |
| No API keys | Use manual analysis workflow |
| Excel errors | Check `football-pool logs` |
| Analysis fails | Try different model with `--model` |

## **File Formats**

| File Type | Purpose | Example |
|-----------|---------|---------|
| `*_contrarian_prompt.txt` | LLM prompts | `2025-09-17_contrarian_prompt.txt` |
| `*_analysis.json` | LLM responses | `week_1_contrarian_analysis.json` |
| `*_picks.json` | Pick data | `week_1_contrarian_picks.json` |
| `Dawgpac25_*.xlsx` | Excel files | `Dawgpac25_2025-09-17.xlsx` |

## **Quick Tips**

- **Always use 2025 dates** for consistency
- **Check logs** when things go wrong: `football-pool logs`
- **Validate Excel** before submission: `football-pool excel-validate`
- **Use contrarian strategy** for maximum edge
- **Combine multiple analyses** for best results
