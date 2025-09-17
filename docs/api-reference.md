# 🔌 API Reference - Football Pool Domination System

## 🚀 Core Commands

### Analysis Commands
```bash
football-pool prompt <week> --enhanced           # Generate research prompt
football-pool analyze-llm <week>                 # Automated AI analysis
football-pool combine-analyses <week> [options]  # Combine multiple analyses
football-pool import-llm <week> <file>           # Import manual analysis
```

### Pick Generation
```bash
football-pool picks <week>                       # Generate optimal picks
football-pool report <week>                      # Create submission report
```

### Monitoring & Utilities
```bash
football-pool stats                              # System status
football-pool api-usage                          # API usage tracking
football-pool test-web-search <week>             # Test web search
football-pool clear-cache                        # Clear API cache
```

### Competitor Tracking
```bash
football-pool competitors add <name> [options]   # Add competitor
football-pool analyze                            # Analyze patterns
```

## 🔧 Command Options

### Prompt Generation
```bash
football-pool prompt 1 --enhanced                # Include real odds + web search
football-pool prompt 1 --force-refresh           # Force refresh odds data
```

### Analysis Combination
```bash
football-pool combine-analyses 1 --automated                    # Automated only
football-pool combine-analyses 1 --manual file.json            # Manual only
football-pool combine-analyses 1 --automated --manual file.json # Both
football-pool combine-analyses 1 --method average              # Average method
football-pool combine-analyses 1 --method weighted             # Weighted method
football-pool combine-analyses 1 --method best                 # Best method
```

### Competitor Management
```bash
football-pool competitors add "John Doe" --picks "KC,NYG,BUF" --confidence "20,19,18"
football-pool competitors list
football-pool competitors remove "John Doe"
```

## 📊 Data Formats

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

## 🔌 API Integration

### Environment Variables
```bash
THE_ODDS_API_KEY=your_odds_api_key      # Real-time betting odds
OPENROUTER_API_KEY=your_openrouter_key  # AI analysis
EXA_API_KEY=your_exa_key                # Web search (optional)
```

### API Limits
- **The Odds API**: 500 requests/month
- **OpenRouter**: 1000+ requests/month
- **Exa API**: Varies by plan

### Usage Tracking
```bash
football-pool api-usage          # Check current usage
football-pool clear-cache        # Clear API cache
```

## 🚨 Error Handling

### Common Errors
- **No API keys**: Check `.env` file configuration
- **Rate limits**: Use `football-pool api-usage` to monitor
- **Web search issues**: Test with `football-pool test-web-search 1`
- **Pick generation**: Verify analysis was imported correctly

### Troubleshooting Commands
```bash
football-pool stats              # System status
football-pool api-usage          # API usage
football-pool test-web-search 1  # Test web search
football-pool clear-cache        # Clear cache
```

## 📞 Support

- **System status**: `football-pool stats`
- **API usage**: `football-pool api-usage`
- **Help**: `football-pool --help`
- **Test web search**: `football-pool test-web-search 1`

---

**Technical reference**: Complete command and data format documentation.
