# 📝 Examples & Sample Data

## 🚀 Quick Examples

### Basic Workflow
```bash
# Generate enhanced prompt
football-pool prompt 1 --enhanced

# Get automated analysis
football-pool analyze-llm 1

# Generate picks
football-pool picks 1

# Create report
football-pool report 1
```

### Combined Analysis
```bash
# Combine automated + manual analysis
football-pool combine-analyses 1 --automated --manual week_1_manual.json

# Combine multiple manual analyses
football-pool combine-analyses 1 --manual week_1_chatgpt.json --manual week_1_claude.json
```

## 📁 Sample Files

### LLM Analysis Format
```json
{
  "week": 1,
  "games": [
    {
      "game": "KC@NYG",
      "spread": -7.5,
      "public_percentage": 72,
      "injuries": "KC: No significant injuries. NYG: Darren Waller (hamstring) questionable",
      "weather": "Indoor stadium (MetLife Stadium) - no weather impact",
      "situational_factors": {
        "must_win": false,
        "revenge_game": false,
        "lookahead_spot": false,
        "short_week": false,
        "extra_rest": false
      },
      "confidence_score": 85
    }
  ]
}
```

### Results Format
```json
{
  "week": 1,
  "results": [
    {
      "game": "KC@NYG",
      "winner": "KC",
      "score": "KC 31, NYG 17",
      "spread_result": "KC covered -7.5",
      "total_result": "Over 47.5"
    }
  ]
}
```

### Competitor Picks Format
```json
{
  "week": 1,
  "competitors": [
    {
      "name": "John Doe",
      "picks": ["KC", "NYG", "BUF"],
      "confidence": [20, 19, 18]
    }
  ]
}
```

## 🔧 Usage Examples

### Generate Enhanced Prompt
```bash
# Basic prompt
football-pool prompt 1

# Enhanced prompt with real odds + web search
football-pool prompt 1 --enhanced
```

### Import Analysis
```bash
# Import manual LLM analysis
football-pool import-llm 1 week_1_manual.json

# Import results
football-pool results 1 --import week_1_results.json
```

### Track Competitors
```bash
# Add competitor picks
football-pool competitors add "John Doe" --picks "KC,NYG,BUF" --confidence "20,19,18"

# Analyze patterns
football-pool analyze
```

### Monitor System
```bash
# Check API usage
football-pool api-usage

# System status
football-pool stats

# Test web search
football-pool test-web-search 1
```

## 📊 Output Examples

### Pick Generation
```
WEEK 1 OPTIMAL PICKS
====================
Strategy: Balanced (Position: 0 points)

Rank | Game    | Pick | Confidence | Reasoning
-----|---------|------|------------|----------
1    | KC@NYG  | KC   | 20         | Strong favorite, home field
2    | BUF@MIA | BUF  | 19         | Weather advantage
3    | LAR@SF  | LAR  | 18         | Revenge game factor
```

### Performance Report
```
WEEK 1 PERFORMANCE REPORT
========================
Total Points: 45/60
Correct Picks: 15/20
Accuracy: 75%

Top Performers:
- KC@NYG (20 points): ✅ Correct
- BUF@MIA (19 points): ✅ Correct
- LAR@SF (18 points): ❌ Incorrect
```

## 💡 Pro Tips

1. **Save all files** for future reference
2. **Use enhanced prompts** for comprehensive analysis
3. **Combine multiple analyses** for best results
4. **Track competitors** for edge analysis
5. **Monitor API usage** to stay within limits

## 📞 Support

- **System status**: `football-pool stats`
- **API usage**: `football-pool api-usage`
- **Help**: `football-pool --help`
- **Test web search**: `football-pool test-web-search 1`

---

**Examples ready to use**: All sample files are in the `examples/` directory.
