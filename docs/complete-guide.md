# 📖 Complete Guide - Football Pool Domination System

## 🚀 Quick Setup (5 minutes)

### 1. Installation
```bash
# Clone and setup
git clone <repository>
cd oski-football-pool
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys:
# THE_ODDS_API_KEY=your_odds_api_key
# OPENROUTER_API_KEY=your_openrouter_key
# EXA_API_KEY=your_exa_key (optional, has demo credentials)
```

### 3. Test Installation
```bash
# Test basic functionality
football-pool stats

# Test web search (if API keys configured)
football-pool test-web-search 1
```

## 📋 Weekly Workflow

### Option A: Automated (5 minutes)
```bash
# Complete automated workflow
football-pool analyze-llm 1 && football-pool picks 1 && football-pool report 1
```

### Option B: Manual + Automated (Best Results)
```bash
# 1. Generate enhanced prompt
football-pool prompt 1 --enhanced

# 2. Use with your preferred LLM (ChatGPT, Claude, Gemini)
# Copy prompt → Paste in LLM → Get JSON response
# Save as week_1_manual.json

# 3. Combine with automated analysis
football-pool combine-analyses 1 --automated --manual week_1_manual.json

# 4. Generate picks and report
football-pool picks 1 && football-pool report 1
```

## 🎯 Analysis Methods

### Automated Analysis
- **Speed**: 5 minutes
- **Models**: Free OpenRouter models (moonshotai/kimi-k2:free, deepseek/deepseek-chat-v3.1:free, etc.)
- **Features**: Real odds data + web search context
- **Command**: `football-pool analyze-llm 1`

### Manual Analysis
- **Speed**: 30-60 minutes
- **Flexibility**: Use any LLM (ChatGPT, Claude, Gemini, etc.)
- **Process**: Copy enhanced prompt → Get JSON → Import
- **Command**: `football-pool import-llm 1 week_1_manual.json`

### Combined Analysis
- **Speed**: 10-15 minutes
- **Best of Both**: Automated + Manual insights
- **Methods**: Average, Weighted, Best
- **Command**: `football-pool combine-analyses 1 --automated --manual file.json`

## 🔀 Combination Methods

### Average Method (Default)
- Averages all numerical values
- Combines text fields with unique values
- Best for: Getting consensus from multiple sources

### Weighted Method
- Weights values by confidence scores
- Higher confidence analyses have more influence
- Best for: When you trust some analyses more than others

### Best Method
- Uses the analysis with highest confidence score
- Takes all values from the "best" analysis
- Best for: When you want the most confident single analysis

## 🏆 Pool Strategies

### Protective Strategy (Leading by 30+ points)
- Conservative picks with high confidence
- Avoid high-variance games
- Focus on maintaining lead

### Balanced Strategy (Within 30 points)
- Mix of conservative and moderate picks
- Balanced risk/reward approach
- Maintain competitive position

### High Variance Strategy (Trailing significantly)
- Aggressive picks with potential for big gains
- Target contrarian opportunities
- High-risk, high-reward approach

## 🔧 Monitoring & Maintenance

### API Usage Tracking
```bash
football-pool api-usage          # Check current usage
football-pool clear-cache        # Clear API cache
```

### System Status
```bash
football-pool stats              # Overall system status
football-pool test-web-search 1  # Test web search functionality
```

### Competitor Tracking
```bash
football-pool competitors add "John Doe" --picks "KC,NYG,BUF" --confidence "20,19,18"
football-pool analyze            # Analyze competitor patterns
```

## 📊 Performance Analysis

### Weekly Results
```bash
football-pool results 1 --import week_1_results.json
football-pool report --week 1
```

### Season Projections
```bash
football-pool project            # Season-long projections
football-pool stats              # Overall performance metrics
```

## 🚨 Troubleshooting

### Common Issues

#### No API Keys
```bash
# Check if .env file exists and has correct keys
cat .env

# Test API connectivity
football-pool test-web-search 1
```

#### Web Search Issues
```bash
# Test web search functionality
football-pool test-web-search 1

# Clear cache if needed
football-pool clear-cache
```

#### Pick Generation Errors
```bash
# Check system status
football-pool stats

# Verify analysis was imported
football-pool import-llm 1 week_1_llm.json
```

#### API Limit Issues
```bash
# Check current usage
football-pool api-usage

# Clear cache to reduce API calls
football-pool clear-cache
```

## 💡 Pro Tips

1. **Use combined analysis** for maximum insight from multiple sources
2. **Try different combination methods** to see which works best
3. **Save individual analyses** before combining for comparison
4. **Track competitors** for edge analysis
5. **Monitor API usage** to stay within limits
6. **Submit picks early** to avoid deadline pressure

## 📞 Support

- **System status**: `football-pool stats`
- **API usage**: `football-pool api-usage`
- **Help**: `football-pool --help`
- **Test web search**: `football-pool test-web-search 1`

---

**Total setup time**: 5-60 minutes depending on analysis method chosen.
