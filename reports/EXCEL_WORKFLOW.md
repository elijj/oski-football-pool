# 📊 Excel Automation Workflow

## 🎯 Overview

This system automates the creation and management of Excel files for weekly pool submissions, following the exact format required by the pool organizer.

## 📋 Key Requirements

- **Preserve original format**: Never modify the original `Dawgpac25.xlsx` template
- **Date suffixes**: Use single dates as file suffixes (e.g., `Dawgpac25_2024-09-18.xlsx`)
- **Maintain structure**: Keep the same Excel structure with weeks 1-18 and confidence points 20-1
- **Team abbreviations**: Use standard abbreviations as specified in the pool

## 🚀 Weekly Workflow

### 1. Generate Research Prompt
```bash
# For a specific date
football-pool excel-prompt "2024-09-18" --enhanced

# For a week range
football-pool excel-prompt "Week 3" --enhanced
```

### 2. Get Analysis (Choose One)

#### Option A: Manual Analysis
1. Copy the generated prompt to ChatGPT/Claude/Gemini
2. Get JSON response in the required format
3. Save as `week_3_manual.json`

#### Option B: Automated Analysis
```bash
football-pool analyze-llm 3
```

#### Option C: Combined Analysis
```bash
football-pool combine-analyses 3 --automated --manual week_3_manual.json
```

### 3. Update Excel File
```bash
# With date suffix
football-pool excel-update 3 --date "2024-09-18"

# With picks file
football-pool excel-update 3 --date "2024-09-18" --picks week_3_manual.json

# Generate picks automatically
football-pool excel-update 3 --date "2024-09-18"
```

### 4. Validate Picks
```bash
football-pool excel-validate 3 --date "2024-09-18"
```

### 5. Prepare Submission
```bash
football-pool excel-submit 3 --date "2024-09-18"
```

## 📁 File Naming Convention

- **Template**: `Dawgpac25.xlsx` (never modify)
- **Weekly files**: `Dawgpac25_2024-09-18.xlsx`
- **Backups**: `Dawgpac25_Week3_backup_20240918_143022.xlsx`

## 🔧 Excel Structure

The Excel file maintains the exact structure:
- **Row 1**: Week numbers (1-18)
- **Column A**: Confidence points (20-1)
- **Data cells**: Team abbreviations for each pick

## 📊 Commands Reference

### Excel Commands
```bash
# Generate prompt for specific date
football-pool excel-prompt "2024-09-18" --enhanced

# Update Excel with picks
football-pool excel-update 3 --date "2024-09-18"

# Validate picks
football-pool excel-validate 3 --date "2024-09-18"

# Prepare for submission
football-pool excel-submit 3 --date "2024-09-18"
```

### Options
- `--date`: Date suffix for filename (e.g., "2024-09-18")
- `--picks`: JSON file with picks data
- `--name`: Participant name (default: "Dawgpac")
- `--email`: Email address for submission
- `--subject`: Email subject line

## 🎯 Complete Example

```bash
# 1. Generate enhanced prompt for Week 3 (Sept 18)
football-pool excel-prompt "2024-09-18" --enhanced

# 2. Copy prompt to ChatGPT, get JSON, save as week_3_manual.json

# 3. Update Excel file
football-pool excel-update 3 --date "2024-09-18" --picks week_3_manual.json

# 4. Validate picks
football-pool excel-validate 3 --date "2024-09-18"

# 5. Prepare submission
football-pool excel-submit 3 --date "2024-09-18"
```

## 📧 Submission Process

1. **Generate Excel file** with date suffix
2. **Validate picks** to ensure they meet pool rules
3. **Attach Excel file** to email
4. **Send to pool organizer** with appropriate subject line

## 🔍 Validation Rules

- **20 picks required** (exactly 20 games)
- **Confidence points 1-20** (no duplicates)
- **Valid team abbreviations** (converted automatically)
- **No empty picks** (all cells filled)

## 💡 Pro Tips

1. **Use date suffixes** for better file organization
2. **Create backups** before making changes
3. **Validate picks** before submission
4. **Keep original template** untouched
5. **Use enhanced prompts** for better analysis

## 🚨 Troubleshooting

### Common Issues
- **File not found**: Check if template exists
- **Invalid picks**: Run validation first
- **Wrong format**: Ensure picks are in correct JSON format
- **Missing teams**: Check team abbreviation mapping

### Support Commands
```bash
football-pool stats              # System status
football-pool api-usage          # API usage
football-pool --help             # All commands
```

---

**Total time**: 10-30 minutes depending on analysis method chosen.
