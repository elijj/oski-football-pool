# 📁 Project Structure

This document outlines the organized structure of the Football Pool Domination System.

## 🏗️ Directory Organization

```
oski-football-pool/
├── 📁 src/                          # Core source code
│   ├── pool_analyzer.py             # Main analyzer with optimization strategies
│   └── pool_core.py                 # Core database and tracking functionality
│
├── 📁 football_pool/                # Main package directory
│   ├── __init__.py
│   ├── cli.py                       # Command-line interface
│   ├── core.py                      # Core system functionality
│   ├── automation.py                # Automation features
│   ├── web_search.py                # Web search integration
│   └── ...                          # Other package modules
│
├── 📁 scripts/                      # Utility and analysis scripts
│   ├── analysis/                    # Analysis scripts
│   │   ├── analyze_optimal_strategy.py
│   │   ├── analyze_week3_games.py
│   │   ├── research_based_strategy.py
│   │   ├── implement_optimal_strategy.py
│   │   ├── generate_pick_summary.py
│   │   ├── extract_contrarian_picks.py
│   │   └── recreate_contrarian_output.py
│   ├── automation/                  # Automation scripts
│   │   └── automated_contrarian_workflow.py
│   └── verification/                # Testing and verification scripts
│       ├── debug_excel.py
│       ├── debug_excel_rows.py
│       └── test_excel_fix.py
│
├── 📁 data/                         # Data files and storage
│   ├── excel/                       # Excel files
│   │   ├── 2025-2026 Football Schedule.xlsx
│   │   ├── Dawgpac25_2024-09-03.xlsx
│   │   ├── Dawgpac25_2024-09-17-favs.xlsx
│   │   ├── Dawgpac25_2024-09-17.xlsx
│   │   ├── Dawgpac25_2024-09-18.xlsx
│   │   ├── Dawgpac25_2024-09-24.xlsx
│   │   └── Dawgpac25.xlsx
│   ├── json/                        # JSON data files
│   │   ├── api_usage.json
│   │   ├── automation.json
│   │   ├── submission_log_4.json
│   │   ├── workflow_results_4.json
│   │   ├── llm_data_week_1.json
│   │   ├── llm_data_week_3.json
│   │   ├── week_1_*.json (multiple analysis files)
│   │   └── week_3_manual.json
│   ├── cache/                       # API cache files
│   └── exports/                     # Generated exports
│
├── 📁 config/                       # Configuration files
│   ├── prompts/                     # Prompt templates
│   │   ├── 2025-09-17_contrarian_prompt.txt
│   │   ├── contrarian_analysis_prompt.txt
│   │   └── test_prompt.txt
│   ├── templates/                   # Template files
│   └── .env.example                 # Environment variables template
│
├── 📁 reports/                      # Generated reports and documentation
│   ├── weekly/                      # Weekly analysis reports
│   ├── analysis/                    # Analysis reports
│   ├── CHANGELOG.md
│   ├── CONTRARIAN_WORKFLOW.md
│   ├── CONTRIBUTING.md
│   ├── EXCEL_WORKFLOW.md
│   ├── FB2022-rules.md
│   ├── Pool_Week_1_Contrarian_Analysis_Summary.md
│   ├── Summary Form Directions25.doc
│   ├── Summary Form Directions25.md
│   └── WEEKLY_WORKFLOW.md
│
├── 📁 archive/                      # Archived files
│   └── htmlcov/                     # Coverage reports
│
├── 📁 tests/                        # Test files
│   └── ...                          # Test modules
│
├── 📁 docs/                         # Documentation
│   └── ...                          # Documentation files
│
├── 📁 examples/                     # Example files
│   └── ...                          # Example data and configurations
│
├── 📁 logs/                         # Log files
│   └── ...                          # Application logs
│
├── 📁 venv/                         # Virtual environment
│   └── ...                          # Python virtual environment
│
├── 📁 football_pool_domination.egg-info/  # Package metadata
│   └── ...                          # Package information
│
├── 📁 .pytest_cache/                # Pytest cache
│   └── ...                          # Pytest temporary files
│
├── 🔧 Configuration Files
├── .env                            # Environment variables (not in git)
├── .gitignore                      # Git ignore rules
├── .pre-commit-config.yaml         # Pre-commit hooks configuration
├── .secrets.baseline              # Secrets detection baseline
├── .trufflehog.yaml               # TruffleHog configuration
├── Makefile                        # Build automation
├── pyproject.toml                  # Project configuration
├── requirements.txt                # Python dependencies
├── requirements-dev.txt            # Development dependencies
├── setup.py                        # Package setup
├── SECURITY.md                     # Security guidelines
└── README.md                       # Project documentation
```

## 🎯 **Key Benefits of This Structure:**

### ✅ **Organization**
- **Clear separation** of concerns
- **Logical grouping** of related files
- **Easy navigation** and maintenance

### ✅ **Security**
- **Sensitive data** properly isolated
- **Configuration files** in dedicated directories
- **Environment variables** properly managed

### ✅ **Development**
- **Source code** in `src/` and `football_pool/`
- **Scripts** organized by purpose
- **Data files** properly categorized

### ✅ **Maintenance**
- **Easy to find** specific file types
- **Clear ownership** of different components
- **Scalable structure** for future growth

## 📋 **File Categories:**

| Directory | Purpose | File Types |
|-----------|---------|------------|
| `src/` | Core source code | `.py` files |
| `scripts/` | Utility scripts | Analysis, automation, verification |
| `data/` | Data storage | `.xlsx`, `.json`, `.db` |
| `config/` | Configuration | `.txt`, `.env.example` |
| `reports/` | Documentation | `.md`, `.doc` |
| `archive/` | Archived files | Coverage, old reports |
| `tests/` | Test files | Test modules |
| `docs/` | Documentation | Help files |
| `examples/` | Examples | Sample data |

## 🚀 **Usage Guidelines:**

1. **New Python files** → `src/` or `football_pool/`
2. **Analysis scripts** → `scripts/analysis/`
3. **Data files** → `data/` (with appropriate subdirectory)
4. **Configuration** → `config/`
5. **Documentation** → `reports/` or `docs/`
6. **Tests** → `tests/`

This structure ensures your project remains organized, maintainable, and professional as it grows!
