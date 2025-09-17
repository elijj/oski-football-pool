# 📁 Output Organization Guide

This document outlines the clean organization of all project outputs and generated files.

## 🎯 **Output Directory Structure**

```
data/
├── excel/           # Excel files for pool submissions
│   ├── Dawgpac25_YYYY-MM-DD.xlsx    # Weekly submission files
│   └── Week_X_Picks_YYYY-MM-DD.csv  # Comprehensive CSV with metadata
├── json/            # JSON analysis files
│   ├── week_X_complete_contrarian_analysis.json  # Final contrarian analysis
│   ├── week_X_value_analysis.json               # Value optimization reports
│   └── api_usage.json                          # API usage tracking
├── prompts/         # Generated prompts
│   └── YYYY-MM-DD_contrarian_prompt.txt         # Contrarian analysis prompts
├── cache/           # Cached data
│   └── *.json       # Cached API responses
└── competitors/     # Competitor tracking data
    └── *.json       # Competitor pick logs

reports/
├── Week_X_Enhanced_Strategy_Report_YYYY-MM-DD.md  # Main strategy reports
├── Week_X_Strategy_Report_YYYY-MM-DD.md          # Basic strategy reports
├── Week_X_Preview_YYYY-MM-DD.md                  # Next week previews
├── analysis/        # Detailed analysis reports
└── weekly/          # Weekly workflow outputs

logs/
├── command_execution.log    # CLI command logs
├── llm_interactions.log     # LLM API interactions
├── excel_automation.log     # Excel automation logs
└── api_calls.log           # API usage logs
```

## 📊 **File Naming Conventions**

### Excel Files
- **Submission Files**: `Dawgpac25_YYYY-MM-DD.xlsx`
- **CSV Exports**: `Week_X_Picks_YYYY-MM-DD.csv`

### JSON Files
- **Contrarian Analysis**: `week_X_complete_contrarian_analysis.json`
- **Value Analysis**: `week_X_value_analysis.json`
- **API Usage**: `api_usage.json`
- **Automation Config**: `automation.json`

### Reports
- **Enhanced Reports**: `Week_X_Enhanced_Strategy_Report_YYYY-MM-DD.md`
- **Basic Reports**: `Week_X_Strategy_Report_YYYY-MM-DD.md`
- **Previews**: `Week_X_Preview_YYYY-MM-DD.md`

### Prompts
- **Contrarian Prompts**: `YYYY-MM-DD_contrarian_prompt.txt`

## 🔧 **Output Configuration**

### Excel Automation
- **Default Output**: `data/excel/`
- **Template**: `Dawgpac25.xlsx` (root directory)
- **Generated Files**: Weekly submission files with date suffixes

### CSV Generation
- **Default Output**: `data/excel/`
- **Format**: Comprehensive CSV with all metadata columns
- **Columns**: Game, Team, Confidence_Points, Strategy_Type, etc.

### JSON Analysis
- **Default Output**: `data/json/`
- **Format**: Structured JSON with contrarian analysis
- **Content**: Optimal picks, reasoning, contrarian edges, value plays

### Reports
- **Default Output**: `reports/`
- **Format**: Markdown with comprehensive analysis
- **Content**: Strategy analysis, next week previews, value optimization

### Prompts
- **Default Output**: `data/prompts/`
- **Format**: Text files with contrarian analysis prompts
- **Content**: Structured prompts for LLM analysis

## 🚀 **Weekly Workflow Outputs**

When running `football-pool weekly-workflow`, the following files are generated:

### Required Files
1. **`data/prompts/YYYY-MM-DD_contrarian_prompt.txt`** - Contrarian analysis prompt
2. **`data/excel/Dawgpac25_YYYY-MM-DD.xlsx`** - Excel submission file
3. **`reports/Week_X_Enhanced_Strategy_Report_YYYY-MM-DD.md`** - Strategy report
4. **`reports/Week_X_Preview_YYYY-MM-DD.md`** - Next week preview

### Optional Files
5. **`data/excel/Week_X_Picks_YYYY-MM-DD.csv`** - Comprehensive CSV (via comprehensive-csv command)
6. **`data/json/week_X_value_analysis.json`** - Value optimization report (via value-optimization command)

## 📋 **Output Validation**

### File Count Validation
- **Excel Files**: 1 per week (submission file)
- **CSV Files**: 1 per week (comprehensive metadata)
- **JSON Files**: 1-2 per week (analysis + optional value analysis)
- **Reports**: 2 per week (strategy + preview)
- **Prompts**: 1 per week (contrarian prompt)

### Content Validation
- **Excel Files**: Must contain exactly 20 games
- **CSV Files**: Must contain all metadata columns
- **JSON Files**: Must contain valid contrarian analysis structure
- **Reports**: Must contain strategy analysis and recommendations

## 🧹 **Cleanup Guidelines**

### Safe to Remove
- Lock files (`.~lock.*`)
- Old template files
- Redundant analysis files
- Empty log files

### Keep Always
- Latest submission files
- Final analysis files
- Configuration files
- Essential cache data

## 🔄 **Output Lifecycle**

1. **Generation**: Files created during weekly workflow
2. **Validation**: Content and structure validation
3. **Usage**: Files used for pool submissions and analysis
4. **Archival**: Old files moved to archive or cleaned up
5. **Cleanup**: Redundant files removed periodically

## 📝 **Documentation Updates**

When adding new output types:
1. Update this documentation
2. Update `.gitignore` if needed
3. Update CLI help text
4. Update README.md with new outputs
5. Test output generation and validation
