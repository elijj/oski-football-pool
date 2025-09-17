# 🚨 Troubleshooting Guide

## **Common Issues & Solutions**

### **Command Not Found**
```bash
# Problem: 'football-pool' command not found
# Solution: Activate virtual environment
cd /path/to/oski-football-pool
source venv/bin/activate
football-pool --help
```

### **No API Keys**
```bash
# Problem: API errors or missing keys
# Solution: Use manual analysis workflow
football-pool contrarian-prompt 2025-09-17
# Copy prompt to ChatGPT/Claude, get JSON response
football-pool excel-update 1 --date "2025-09-17" --analysis manual_analysis.json
```

### **Excel File Issues**
```bash
# Problem: Excel file not found or corrupted
# Solution: Check file path and permissions
ls -la Dawgpac25*.xlsx
football-pool excel-validate 1 --date "2025-09-17"
```

### **Analysis Failures**
```bash
# Problem: LLM analysis fails
# Solution: Try different model or check logs
football-pool analyze-llm 3 --model "deepseek/deepseek-chat-v3.1:free"
football-pool logs search --query "ERROR"
```

### **Date Issues**
```bash
# Problem: Date format errors
# Solution: Use YYYY-MM-DD format
football-pool contrarian-prompt 2025-09-17  # ✅ Correct
football-pool contrarian-prompt 9/17/2025   # ❌ Wrong format
```

## **Debugging Commands**

### **Check System Status**
```bash
# Check overall system status
football-pool stats

# Check API usage
football-pool api-usage

# View log summary
football-pool logs
```

### **Analyze Logs**
```bash
# Search for errors
football-pool logs search --query "ERROR"

# Analyze LLM interactions
football-pool logs analyze-llm

# Analyze API usage
football-pool logs analyze-api

# View specific log file
football-pool logs tail --file command_execution.log
```

### **Test Components**
```bash
# Test web search
football-pool test-web-search

# Clear cache
football-pool clear-cache

# Test specific model
football-pool analyze-llm 3 --model "moonshotai/kimi-k2:free"
```

## **File Issues**

### **Missing Files**
```bash
# Check if files exist
ls -la *.json *.xlsx *.txt

# Regenerate missing files
football-pool contrarian-prompt 2025-09-17
football-pool analyze-llm 3
```

### **Corrupted Files**
```bash
# Validate JSON files
python -m json.tool week_1_analysis.json

# Validate Excel files
football-pool excel-validate 1 --date "2025-09-17"
```

### **Permission Issues**
```bash
# Fix file permissions
chmod 644 *.json *.txt
chmod 644 *.xlsx
```

## **API Issues**

### **Rate Limits**
```bash
# Check API usage
football-pool api-usage

# Clear cache to reduce API calls
football-pool clear-cache
```

### **Authentication Errors**
```bash
# Check API keys in .env file
cat .env

# Test with manual analysis if API fails
football-pool contrarian-prompt 2025-09-17
```

## **Performance Issues**

### **Slow Analysis**
```bash
# Use faster models
football-pool analyze-llm 3 --model "moonshotai/kimi-k2:free"

# Check system resources
football-pool stats
```

### **Memory Issues**
```bash
# Clear cache
football-pool clear-cache

# Restart virtual environment
deactivate
source venv/bin/activate
```

## **Excel Automation Issues**

### **Pick Alignment Problems**
```bash
# Validate picks
football-pool excel-validate 1 --date "2025-09-17"

# Check pick format
python -c "
import json
with open('week_1_picks.json', 'r') as f:
    data = json.load(f)
    print('Picks:', len(data.get('picks', [])))
    for pick in data.get('picks', []):
        print(f'  {pick.get(\"team\", \"\")} - {pick.get(\"confidence\", 0)}')
"
```

### **Team Name Issues**
```bash
# Check team abbreviations
football-pool excel-update 1 --date "2025-09-17" --analysis analysis.json
# Look for team name conversion errors in logs
football-pool logs search --query "team"
```

## **Advanced Debugging**

### **Verbose Logging**
```bash
# Enable debug logging
export FOOTBALL_POOL_DEBUG=1
football-pool analyze-llm 3
```

### **Step-by-Step Debugging**
```bash
# 1. Test basic functionality
football-pool stats

# 2. Test prompt generation
football-pool contrarian-prompt 2025-09-17

# 3. Test LLM analysis
football-pool analyze-llm 3 --model "moonshotai/kimi-k2:free"

# 4. Test Excel update
football-pool excel-update 1 --date "2025-09-17" --analysis analysis.json

# 5. Test validation
football-pool excel-validate 1 --date "2025-09-17"
```

### **Log Analysis**
```bash
# Get detailed log analysis
football-pool logs analyze-llm
football-pool logs analyze-api

# Search for specific issues
football-pool logs search --query "ERROR"
football-pool logs search --query "WARNING"
football-pool logs search --query "failed"
```

## **Recovery Procedures**

### **Reset System**
```bash
# Clear all cache and logs
football-pool clear-cache
football-pool logs clear --confirm

# Restart fresh
football-pool stats
```

### **Regenerate Files**
```bash
# Regenerate all analysis files
football-pool contrarian-prompt 2025-09-17
football-pool analyze-llm 3
football-pool excel-update 1 --date "2025-09-17"
```

### **Backup and Restore**
```bash
# Backup current state
cp -r . backup_$(date +%Y%m%d_%H%M%S)

# Restore from backup
cp -r backup_20250101_120000/* .
```

## **Getting Help**

### **Check Documentation**
- [Quick Reference](quick-reference.md) - Most common commands
- [CLI Reference](cli-reference.md) - Complete command reference
- [Multi-Analysis Strategy](multi-analysis-strategy.md) - Advanced workflows

### **System Information**
```bash
# Get system info
football-pool stats
football-pool api-usage
football-pool logs summary
```

### **Common Solutions**
1. **Activate virtual environment**: `source venv/bin/activate`
2. **Check file permissions**: `ls -la *.json *.xlsx`
3. **Validate JSON files**: `python -m json.tool file.json`
4. **Check logs**: `football-pool logs search --query "ERROR"`
5. **Clear cache**: `football-pool clear-cache`
6. **Use manual workflow**: If API issues persist

## **Prevention Tips**

- **Always use 2025 dates** for consistency
- **Validate Excel files** before submission
- **Check logs regularly** for early issue detection
- **Backup important files** before major changes
- **Test with simple commands** before complex workflows
- **Use contrarian strategy** for maximum edge
