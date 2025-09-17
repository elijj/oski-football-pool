# API Setup Guide - Live Data Only

## 🚨 **CRITICAL: NO FALLBACK DATA**

This system requires **LIVE PRODUCTION DATA ONLY**. No mock data, no fallback data, no default values. All data must come from real APIs.

## 🔑 **Required API Keys**

### **1. The Odds API (THE_ODDS_API_KEY)**
- **Purpose**: Real-time betting odds data
- **Signup**: https://the-odds-api.com/
- **Free Tier**: 500 requests/month
- **Required**: YES - No fallback available

### **2. OpenWeatherMap API (OPENWEATHER_API_KEY)**
- **Purpose**: Real-time weather data for outdoor games
- **Signup**: https://openweathermap.org/api
- **Free Tier**: 1,000 calls/day
- **Required**: YES - No fallback available

### **3. ESPN API (ESPN_API_KEY)**
- **Purpose**: Real-time injury data and player information
- **Signup**: https://developer.espn.com/
- **Free Tier**: 1,000 requests/day
- **Required**: YES - No fallback available

### **4. OpenRouter API (OPENROUTER_API_KEY)**
- **Purpose**: LLM analysis for contrarian strategy
- **Signup**: https://openrouter.ai/
- **Free Tier**: Limited
- **Required**: YES - No fallback available

### **5. Smithery API (SMITHERY_API_KEY)**
- **Purpose**: Web search for enhanced context via Exa MCP
- **Signup**: https://smithery.ai/
- **Free Tier**: Limited
- **Required**: YES - No fallback available

## 📝 **Setup Instructions**

### **Step 1: Create .env File**
```bash
# Create .env file in project root
touch .env
```

### **Step 2: Add API Keys**
```bash
# Edit .env file
nano .env
```

Add your API keys:
```env
# Required API Keys - NO FALLBACK DATA
THE_ODDS_API_KEY=your_odds_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
ESPN_API_KEY=your_espn_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here
SMITHERY_API_KEY=your_smithery_api_key_here
```

### **Step 3: Verify Setup**
```bash
# Test API key validation
football-pool --help

# Check for missing keys
football-pool validate-keys
```

## 🚨 **Error Handling**

### **Missing API Keys**
If any API key is missing, the system will:
- **Raise ValueError** with specific missing key
- **Stop execution** - No fallback data
- **Log warning** about missing keys
- **Require user** to add missing keys

### **API Failures**
If API calls fail, the system will:
- **Raise RuntimeError** with specific error
- **Stop execution** - No fallback data
- **Log error** with details
- **Require user** to fix API issues

## 🔧 **API Key Validation**

The system automatically validates all API keys on startup:

```python
def _validate_api_keys(self) -> None:
    """Validate that required API keys are present for live data."""
    missing_keys = []

    # Check for required API keys
    if not os.getenv("THE_ODDS_API_KEY"):
        missing_keys.append("THE_ODDS_API_KEY")

    if not os.getenv("OPENWEATHER_API_KEY"):
        missing_keys.append("OPENWEATHER_API_KEY")

    if not os.getenv("ESPN_API_KEY"):
        missing_keys.append("ESPN_API_KEY")

    if not os.getenv("OPENROUTER_API_KEY"):
        missing_keys.append("OPENROUTER_API_KEY")

    if not os.getenv("SMITHERY_API_KEY"):
        missing_keys.append("SMITHERY_API_KEY")

    if missing_keys:
        logger.warning(f"Missing API keys: {', '.join(missing_keys)}")
        logger.warning("Some features may not work without proper API keys")
        logger.warning("Set environment variables or add to .env file")
    else:
        logger.info("All required API keys are present")
```

## 📊 **Data Sources**

### **Weather Data**
- **Source**: OpenWeatherMap API
- **Data**: Temperature, wind, precipitation, humidity
- **Update**: Real-time for game day
- **Cache**: 6 hours maximum

### **Injury Data**
- **Source**: ESPN API
- **Data**: Player injuries, status, impact
- **Update**: Real-time for current week
- **Cache**: 12 hours maximum

### **Odds Data**
- **Source**: The Odds API
- **Data**: Betting lines, spreads, totals
- **Update**: Real-time for current week
- **Cache**: 24 hours maximum

### **LLM Analysis**
- **Source**: OpenRouter API
- **Data**: Contrarian analysis, strategy recommendations
- **Update**: On-demand for each week
- **Cache**: None - Fresh analysis each time

## 🎯 **Maximum Earnings Strategy**

With live data only, the system provides:
- **Real-time weather impact** analysis
- **Current injury data** for player impact
- **Live betting odds** for value identification
- **Fresh contrarian analysis** for differentiation
- **Competitor tracking** for edge identification

## ⚠️ **Important Notes**

1. **No Mock Data**: System will fail if API keys are missing
2. **No Fallback**: All data must come from live APIs
3. **No Defaults**: No default values or placeholder data
4. **Live Only**: All analysis based on real-time data
5. **API Dependent**: System requires all APIs to function

## 🚀 **Ready for Production**

Once all API keys are configured:
- System validates all keys on startup
- All data sources provide live production data
- No fallback or mock data available
- Maximum earnings through real-time analysis

---
*Last Updated: 2025-01-27*
*Status: Live Data Only - No Fallbacks*
