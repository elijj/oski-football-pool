# 🏈 CLI Reference Guide

Complete reference for all Football Pool Domination System commands and options.

## 📋 **Table of Contents**

- [Core Commands](#core-commands)
- [Analysis Commands](#analysis-commands)
- [Excel Automation](#excel-automation)
- [Automation & Workflow](#automation--workflow)
- [Utility Commands](#utility-commands)
- [Logging & Debugging](#logging--debugging)

---

## 🎯 **Core Commands**

### **`prompt`** - Generate LLM Research Prompt

Generate research prompts for LLM analysis with optional real odds data.

```bash
football-pool prompt [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--output, -o PATH` - Save prompt to file
- `--enhanced` - Include real odds data in prompt
- `--force-refresh` - Force refresh odds data (uses API)
- `--help` - Show help message

**Examples:**
```bash
# Basic prompt generation
football-pool prompt 3

# Enhanced prompt with real odds
football-pool prompt 3 --enhanced

# Save to file
football-pool prompt 3 --output week_3_prompt.txt

# Force refresh odds data
football-pool prompt 3 --enhanced --force-refresh
```

---

### **`contrarian-prompt`** - Generate Contrarian Analysis Prompt

Generate specialized prompts for contrarian analysis and optimal strategy.

```bash
football-pool contrarian-prompt [OPTIONS] DATE
```

**Arguments:**
- `DATE` - Date for contrarian analysis (e.g., '2025-09-17') [required]

**Options:**
- `--output, -o PATH` - Save prompt to file
- `--help` - Show help message

**Examples:**
```bash
# Generate contrarian prompt
football-pool contrarian-prompt 2025-09-17

# Save to file
football-pool contrarian-prompt 2025-09-17 --output contrarian_prompt.txt
```

---

### **`import-llm`** - Import LLM Analysis Data

Import LLM analysis data for the specified week.

```bash
football-pool import-llm [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number to analyze [required]

**Options:**
- `--file, -f PATH` - Path to LLM analysis JSON file
- `--help` - Show help message

**Examples:**
```bash
# Import LLM analysis
football-pool import-llm 3 --file week_3_analysis.json
```

---

### **`picks`** - Generate Optimal Picks

Generate optimal picks for the specified week.

```bash
football-pool picks [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--strategy, -s TEXT` - Strategy to use (conservative, balanced, aggressive)
- `--help` - Show help message

**Examples:**
```bash
# Generate picks with default strategy
football-pool picks 3

# Use specific strategy
football-pool picks 3 --strategy aggressive
```

---

## 🧠 **Analysis Commands**

### **`analyze-llm`** - Get LLM Analysis Directly

Get LLM analysis directly using OpenRouter models.

```bash
football-pool analyze-llm [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number to analyze [required]

**Options:**
- `--model, -m TEXT` - Specific model to use (optional)
- `--save/--no-save` - Save analysis to file [default: save]
- `--help` - Show help message

**Available Models:**
- `moonshotai/kimi-k2:free`
- `deepseek/deepseek-chat-v3.1:free`
- `qwen/qwen3-235b-a22b:free`
- `openai/gpt-oss-20b:free`

**Examples:**
```bash
# Get analysis with default model
football-pool analyze-llm 3

# Use specific model
football-pool analyze-llm 3 --model "moonshotai/kimi-k2:free"

# Don't save to file
football-pool analyze-llm 3 --no-save
```

---

### **`combine-analyses`** - Combine Multiple LLM Analyses

Combine automated and manual LLM analyses for enhanced insights.

```bash
football-pool combine-analyses [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number to analyze [required]

**Options:**
- `--automated/--no-automated` - Run automated OpenRouter analysis [default: automated]
- `--manual, -m TEXT` - Path to manual LLM analysis file (can be used multiple times)
- `--method TEXT` - Combination method: average, weighted, or best [default: average]
- `--help` - Show help message

**Combination Methods:**
- `average` - Average confidence scores across analyses
- `weighted` - Weight by model performance and confidence
- `best` - Select best pick from each confidence level

**Examples:**
```bash
# Combine with automated analysis
football-pool combine-analyses 3

# Combine multiple manual analyses
football-pool combine-analyses 3 \
  --manual manual_chatgpt.json \
  --manual manual_claude.json \
  --method weighted

# Use best selection method
football-pool combine-analyses 3 \
  --manual manual_gpt4.json \
  --method best
```

---

### **`results`** - Track and Import Game Results

Track and import game results for analysis.

```bash
football-pool results [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--file, -f PATH` - Path to results JSON file
- `--help` - Show help message

**Examples:**
```bash
# Import results
football-pool results 3 --file week_3_results.json
```

---

### **`report`** - Generate Weekly Performance Report

Generate weekly performance report.

```bash
football-pool report [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--output, -o PATH` - Save report to file
- `--help` - Show help message

**Examples:**
```bash
# Generate report
football-pool report 3

# Save report to file
football-pool report 3 --output week_3_report.md
```

---

### **`stats`** - Display Overall Performance Statistics

Display overall performance statistics.

```bash
football-pool stats [OPTIONS]
```

**Options:**
- `--help` - Show help message

**Examples:**
```bash
# Show performance stats
football-pool stats
```

---

### **`competitors`** - Track Competitor Picks

Track competitor picks for analysis.

```bash
football-pool competitors [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--file, -f PATH` - Path to competitor picks JSON file
- `--help` - Show help message

**Examples:**
```bash
# Import competitor picks
football-pool competitors 3 --file competitor_picks.json
```

---

### **`analyze`** - Analyze Competitor Patterns

Analyze competitor patterns and personal edges.

```bash
football-pool analyze [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--output, -o PATH` - Save analysis to file
- `--help` - Show help message

**Examples:**
```bash
# Analyze competitor patterns
football-pool analyze 3

# Save analysis to file
football-pool analyze 3 --output competitor_analysis.md
```

---

### **`project`** - Project Season Finish

Project season finish based on current performance.

```bash
football-pool project [OPTIONS]
```

**Options:**
- `--help` - Show help message

**Examples:**
```bash
# Project season finish
football-pool project
```

---

## 📊 **Excel Automation**

### **`excel-prompt`** - Generate Excel Research Prompt

Generate LLM research prompt for the specified date.

```bash
football-pool excel-prompt [OPTIONS] DATE
```

**Arguments:**
- `DATE` - Date for analysis (e.g., '2025-09-17') [required]

**Options:**
- `--output, -o PATH` - Save prompt to file
- `--help` - Show help message

**Examples:**
```bash
# Generate Excel prompt
football-pool excel-prompt 2025-09-17

# Save to file
football-pool excel-prompt 2025-09-17 --output excel_prompt.txt
```

---

### **`excel-update`** - Update Excel File with Picks

Update Excel file with picks for the specified week.

```bash
football-pool excel-update [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--date, -d TEXT` - Date suffix (e.g., '2025-09-17')
- `--picks, -p TEXT` - JSON file with picks data
- `--analysis, -a TEXT` - Contrarian analysis JSON file
- `--name, -n TEXT` - Participant name [default: Dawgpac]
- `--help` - Show help message

**Examples:**
```bash
# Update Excel with generated picks
football-pool excel-update 3 --date 2025-09-17

# Update with specific picks file
football-pool excel-update 3 --picks week_3_picks.json

# Update with contrarian analysis
football-pool excel-update 3 --analysis contrarian_analysis.json

# Update with custom name
football-pool excel-update 3 --name "MyTeam" --date 2025-09-17
```

---

### **`excel-validate`** - Validate Excel Picks

Validate picks in Excel file for the specified week.

```bash
football-pool excel-validate [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--date, -d TEXT` - Date suffix (e.g., '2025-09-17')
- `--help` - Show help message

**Examples:**
```bash
# Validate Excel picks
football-pool excel-validate 3 --date 2025-09-17
```

---

### **`excel-submit`** - Prepare Excel for Submission

Prepare Excel file for submission.

```bash
football-pool excel-submit [OPTIONS] WEEK
```

**Arguments:**
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--date, -d TEXT` - Date suffix (e.g., '2025-09-17')
- `--help` - Show help message

**Examples:**
```bash
# Prepare Excel for submission
football-pool excel-submit 3 --date 2025-09-17
```

---

## 🤖 **Automation & Workflow**

### **`auto-workflow`** - Run Complete Automated Workflow

Run the complete automated weekly workflow.

```bash
football-pool auto-workflow [OPTIONS] DATE WEEK
```

**Arguments:**
- `DATE` - Date for the week (YYYY-MM-DD format) [required]
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--config, -c TEXT` - Path to automation config file
- `--help` - Show help message

**Examples:**
```bash
# Run automated workflow
football-pool auto-workflow 2025-09-17 3

# Use custom config
football-pool auto-workflow 2025-09-17 3 --config my_config.json
```

---

### **`create-config`** - Create Automation Configuration

Create an automation configuration file.

```bash
football-pool create-config [OPTIONS]
```

**Options:**
- `--output, -o PATH` - Save config to file
- `--help` - Show help message

**Examples:**
```bash
# Create default config
football-pool create-config

# Save to specific file
football-pool create-config --output my_automation_config.json
```

---

### **`schedule-workflow`** - Schedule Automated Workflow

Schedule automated workflow for a specific week.

```bash
football-pool schedule-workflow [OPTIONS] DATE WEEK
```

**Arguments:**
- `DATE` - Date for the week (YYYY-MM-DD format) [required]
- `WEEK` - Week number (3-18) [required]

**Options:**
- `--config, -c TEXT` - Path to automation config file
- `--help` - Show help message

**Examples:**
```bash
# Schedule workflow
football-pool schedule-workflow 2025-09-17 3
```

---

## 🛠️ **Utility Commands**

### **`api-usage`** - Check API Usage and Limits

Check API usage and limits.

```bash
football-pool api-usage [OPTIONS]
```

**Options:**
- `--help` - Show help message

**Examples:**
```bash
# Check API usage
football-pool api-usage
```

---

### **`clear-cache`** - Clear API Cache Files

Clear API cache files.

```bash
football-pool clear-cache [OPTIONS]
```

**Options:**
- `--help` - Show help message

**Examples:**
```bash
# Clear API cache
football-pool clear-cache
```

---

### **`test-web-search`** - Test Web Search Functionality

Test web search functionality.

```bash
football-pool test-web-search [OPTIONS] [QUERY]
```

**Arguments:**
- `QUERY` - Search query (optional)

**Options:**
- `--help` - Show help message

**Examples:**
```bash
# Test web search
football-pool test-web-search

# Test with specific query
football-pool test-web-search "NFL Week 3 predictions"
```

---

## 📝 **Logging & Debugging**

### **`logs`** - View and Analyze Log Files

View and analyze log files.

```bash
football-pool logs [OPTIONS] [ACTION]
```

**Arguments:**
- `ACTION` - Action: summary, tail, search, analyze-llm, analyze-api, clear [default: summary]

**Options:**
- `--file, -f TEXT` - Log file name (for tail/search)
- `--query, -q TEXT` - Search query
- `--lines, -n INTEGER` - Number of lines to show [default: 50]
- `--confirm` - Confirm destructive actions
- `--help` - Show help message

**Actions:**
- `summary` - Show log file summary
- `tail` - Show last N lines of a log file
- `search` - Search logs for specific content
- `analyze-llm` - Analyze LLM interactions
- `analyze-api` - Analyze API usage
- `clear` - Clear log files

**Examples:**
```bash
# Show log summary
football-pool logs

# Show last 100 lines of command log
football-pool logs tail --file command_execution.log --lines 100

# Search for errors
football-pool logs search --query "ERROR"

# Analyze LLM interactions
football-pool logs analyze-llm

# Analyze API usage
football-pool logs analyze-api

# Clear all logs (with confirmation)
football-pool logs clear --confirm
```

---

## 🎯 **Common Workflows**

### **Basic Weekly Workflow**
```bash
# 1. Generate contrarian prompt
football-pool contrarian-prompt 2025-09-17

# 2. Get LLM analysis
football-pool analyze-llm 3 --model "moonshotai/kimi-k2:free"

# 3. Update Excel file
football-pool excel-update 3 --date 2025-09-17 --analysis contrarian_analysis.json

# 4. Validate picks
football-pool excel-validate 3 --date 2025-09-17
```

### **Multi-Analysis Workflow**
```bash
# 1. Get multiple analyses
football-pool analyze-llm 3 --model "moonshotai/kimi-k2:free"
football-pool analyze-llm 3 --model "deepseek/deepseek-chat-v3.1:free"

# 2. Combine analyses
football-pool combine-analyses 3 \
  --manual manual_chatgpt.json \
  --manual manual_claude.json \
  --method weighted

# 3. Update Excel with combined analysis
football-pool excel-update 3 --analysis combined_analysis.json
```

### **Automated Workflow**
```bash
# Run complete automation
football-pool auto-workflow 2025-09-17 3

# Or with custom config
football-pool auto-workflow 2025-09-17 3 --config my_config.json
```

### **Debugging Workflow**
```bash
# Check logs
football-pool logs summary

# Search for specific issues
football-pool logs search --query "ERROR"

# Analyze LLM performance
football-pool logs analyze-llm

# Check API usage
football-pool api-usage
```

---

## 📚 **Additional Resources**

- [Complete Guide](complete-guide.md) - Comprehensive setup and usage guide
- [Strategy Guide](strategy-guide.md) - Optimal strategies for pool success
- [Multi-Analysis Strategy](multi-analysis-strategy.md) - Advanced analysis combination
- [Excel Workflow](excel-workflow.md) - Excel automation guide
- [Automation Guide](automation-guide.md) - Automated workflow setup

---

## 🆘 **Getting Help**

- Use `football-pool <command> --help` for command-specific help
- Check logs with `football-pool logs` for debugging
- Review the [troubleshooting guide](troubleshooting.md) for common issues
