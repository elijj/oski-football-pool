# 🏈 Football Pool Domination System

AI-powered football pool analysis with real-time odds, web search, and strategic pick optimization.

## 🚀 Quick Start

### 1. Setup
```bash
# Install dependencies
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure API keys (optional but recommended)
cp .env.example .env
# Edit .env with your keys: THE_ODDS_API_KEY, OPENROUTER_API_KEY
```

### 2. Run Weekly Workflow

#### **🎯 Contrarian Strategy (Recommended):**
```bash
# 1. Generate contrarian analysis prompt
football-pool contrarian-prompt 2025-09-17

# 2. Copy prompt to ChatGPT/Claude/Gemini
# 3. Get JSON response and save as week_1_contrarian_analysis.json
# 4. Update Excel with contrarian picks
football-pool excel-update 1 --date "2025-09-17" --analysis week_1_contrarian_analysis.json

# 5. Generate summary report
football-pool report 1 --date 2025-09-17
```

#### **Start Here (No API keys needed):**
```bash
# 1. Generate research prompt
football-pool prompt 1 --enhanced

# 2. Copy prompt to ChatGPT/Claude/Gemini
# 3. Get JSON response and save as week_1_manual.json
# 4. Import analysis
football-pool import-llm 1 week_1_manual.json

# 5. Generate picks and report
football-pool picks 1 && football-pool report 1
```

#### **With API keys (Optional):**
```bash
# Automated analysis
football-pool analyze-llm 1 && football-pool picks 1 && football-pool report 1

# Combined analysis (best results)
football-pool combine-analyses 1 --automated --manual week_1_manual.json
football-pool picks 1 && football-pool report 1
```

## 📋 Core Commands

| Command | Purpose |
|---------|---------|
| `football-pool prompt 1 --enhanced` | Generate research prompt with real odds |
| `football-pool analyze-llm 1` | Automated AI analysis (free models) |
| `football-pool combine-analyses 1 --automated --manual file.json` | Combine multiple analyses |
| `football-pool picks 1` | Generate optimal picks |
| `football-pool report 1` | Create submission report |

## 🎯 Analysis Options

### **Contrarian Strategy** (Optimal)
- Deliberately different from the crowd
- Value-focused picks over just favorites
- Weather, injury, and situational analysis
- 15-30 minutes total

### **Automated** (Fast)
- Uses free OpenRouter models
- Real odds + web search context
- 5 minutes total

### **Manual** (Flexible)
- Use any LLM (ChatGPT, Claude, Gemini)
- Copy enhanced prompt → Get JSON → Import
- 30-60 minutes total

### **Combined** (Best Results)
- Automated + Manual analysis
- Multiple combination methods (average, weighted, best)
- Maximum insight from multiple sources

## 🔧 Monitoring & Utilities

```bash
football-pool api-usage          # Check API limits
football-pool stats              # System status
football-pool test-web-search 1  # Test web search
football-pool clear-cache        # Clear API cache
```

## 🚨 Quick Troubleshooting

### Command not found?
```bash
# Make sure you're in the project directory and virtual environment is activated
cd /path/to/oski-football-pool
source venv/bin/activate
football-pool --help
```

### No API keys?
```bash
# You can still use manual analysis
football-pool prompt 1 --enhanced
# Copy to ChatGPT/Claude, get JSON, save as week_1_manual.json
football-pool import-llm 1 week_1_manual.json
football-pool picks 1
```

### Need help?
```bash
football-pool --help             # See all commands
football-pool stats              # Check system status
```

## 📚 Documentation

- [Quick Reference](docs/quick-reference.md) - **🚀 Most common commands**
- [CLI Reference](docs/cli-reference.md) - **📋 Complete command reference**
- [Troubleshooting](docs/troubleshooting.md) - **🚨 Common issues & solutions**
- [Contrarian Workflow](CONTRARIAN_WORKFLOW.md) - **🎯 Optimal strategy guide**
- [Weekly Workflow](WEEKLY_WORKFLOW.md) - Complete step-by-step guide
- [Multi-Analysis Strategy](docs/multi-analysis-strategy.md) - Advanced analysis combination
- [docs/](docs/) - **📚 Complete documentation index**

## 🏆 Pool Rules

- **20 games** with confidence points 1-20
- **Strategy based on position**: Protective (leading), Balanced (close), High Variance (trailing)
- **Real-time odds** and public betting data
- **Injury/weather** analysis included

---

**Time**: 5-60 minutes depending on analysis method.
