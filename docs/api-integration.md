# 🔌 API Integration Guide

## 🚀 Quick Setup

### 1. Get API Keys
- **The Odds API**: [the-odds-api.com](https://the-odds-api.com) (500 requests/month)
- **OpenRouter**: [openrouter.ai](https://openrouter.ai) (1000+ requests/month)
- **Exa API**: [exa.ai](https://exa.ai) (optional, has demo credentials)

### 2. Configure Environment
```bash
# Copy template
cp .env.example .env

# Edit .env file
THE_ODDS_API_KEY=your_odds_api_key
OPENROUTER_API_KEY=your_openrouter_key
EXA_API_KEY=your_exa_key
```

### 3. Test Integration
```bash
# Test API connectivity
football-pool test-web-search 1
football-pool api-usage
```

## 📊 API Usage & Limits

### The Odds API
- **Limit**: 500 requests/month
- **Usage**: Real-time betting odds and spreads
- **Caching**: 6-hour cache to minimize requests
- **Tracking**: `football-pool api-usage`

### OpenRouter API
- **Limit**: 1000+ requests/month
- **Models**: Free models (moonshotai/kimi-k2:free, deepseek/deepseek-chat-v3.1:free, etc.)
- **Usage**: AI-powered game analysis
- **Tracking**: `football-pool api-usage`

### Exa API (Web Search)
- **Limit**: Varies by plan
- **Usage**: Enhanced web search for context
- **Demo**: Hardcoded credentials available
- **Tracking**: `football-pool api-usage`

## 🔧 Monitoring & Management

### Check Usage
```bash
football-pool api-usage          # Current usage across all APIs
football-pool stats              # System status
```

### Optimize Usage
```bash
football-pool clear-cache        # Clear API cache
football-pool test-web-search 1  # Test web search functionality
```

### Cache Management
- **Odds API**: 6-hour cache for game data
- **Web Search**: No caching (real-time results)
- **LLM Analysis**: Saved to files for reuse

## 🚨 Troubleshooting

### API Key Issues
```bash
# Check if keys are loaded
football-pool stats

# Test specific APIs
football-pool test-web-search 1
football-pool analyze-llm 1
```

### Rate Limit Issues
```bash
# Check current usage
football-pool api-usage

# Clear cache to reduce calls
football-pool clear-cache
```

### Web Search Issues
```bash
# Test web search
football-pool test-web-search 1

# Check if Exa API key is configured
football-pool stats
```

## 💡 Optimization Tips

1. **Use caching**: System automatically caches odds data for 6 hours
2. **Monitor usage**: Check `football-pool api-usage` regularly
3. **Combine analyses**: Use multiple sources to maximize value
4. **Clear cache**: When needed to get fresh data
5. **Test connectivity**: Use `football-pool test-web-search 1` to verify

## 📞 Support

- **System status**: `football-pool stats`
- **API usage**: `football-pool api-usage`
- **Test web search**: `football-pool test-web-search 1`
- **Clear cache**: `football-pool clear-cache`

---

**Setup time**: 5-10 minutes for API configuration.
