"""
Comprehensive Markdown Report Generator for Football Pool Strategy
"""

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

class StrategyReportGenerator:
    """Generate comprehensive markdown reports for pool strategy."""

    def __init__(self):
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)

    def generate_weekly_strategy_report(
        self,
        week: int,
        date: str,
        analysis_file: str,
        picks_file: Optional[str] = None
    ) -> str:
        """Generate comprehensive weekly strategy report."""

        # Load analysis data
        analysis_data = self._load_analysis_data(analysis_file)

        # Load picks data if available
        picks_data = self._load_picks_data(picks_file) if picks_file else None

        # Generate report content
        report_content = self._build_report_content(
            week, date, analysis_data, picks_data
        )

        # Save report
        report_filename = f"Week_{week}_Strategy_Report_{date}.md"
        report_path = self.reports_dir / report_filename

        with open(report_path, 'w') as f:
            f.write(report_content)

        logger.info(f"Strategy report saved to {report_path}")
        return str(report_path)

    def _load_analysis_data(self, analysis_file: str) -> Dict[str, Any]:
        """Load analysis data from JSON file."""
        try:
            with open(analysis_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading analysis data: {e}")
            return {}

    def _load_picks_data(self, picks_file: str) -> Optional[Dict[str, Any]]:
        """Load picks data from JSON file."""
        try:
            with open(picks_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading picks data: {e}")
            return None

    def _build_report_content(
        self,
        week: int,
        date: str,
        analysis_data: Dict[str, Any],
        picks_data: Optional[Dict[str, Any]]
    ) -> str:
        """Build comprehensive report content."""

        # Extract data
        contrarian_analysis = analysis_data.get("contrarian_analysis", {})
        optimal_picks = analysis_data.get("optimal_picks", [])
        strategy_summary = analysis_data.get("strategy_summary", {})

        # Build report
        report = f"""# Week {week} Strategy Report - {date}

## 🎯 **EXECUTIVE SUMMARY**

**Strategy Focus**: Contrarian analysis for maximum earnings
**Total Picks**: {len(optimal_picks)}
**Date**: {date}
**Week**: {week}

---

## 📊 **CONTRARIAN ANALYSIS OVERVIEW**

### **Public Betting Analysis**
- **High Public Games**: {', '.join(contrarian_analysis.get('public_betting_analysis', {}).get('high_public_games', []))}
- **Contrarian Opportunities**: {', '.join(contrarian_analysis.get('public_betting_analysis', {}).get('contrarian_opportunities', []))}
- **Sharp Money Indicators**: {', '.join(contrarian_analysis.get('public_betting_analysis', {}).get('sharp_money_indicators', []))}

### **Weather Impact**
- **Outdoor Games**: {len(contrarian_analysis.get('weather_impact', {}).get('outdoor_games', []))} games
- **Weather Advantages**: {', '.join(contrarian_analysis.get('weather_impact', {}).get('weather_advantages', []))}
- **Weather Plays**: {', '.join(contrarian_analysis.get('weather_impact', {}).get('weather_plays', []))}

### **Injury Analysis**
- **Key Injuries**: {len(contrarian_analysis.get('injury_analysis', {}).get('key_injuries', []))} significant injuries
- **Public Overreactions**: {len(contrarian_analysis.get('injury_analysis', {}).get('public_overreactions', []))} overreactions identified
- **Injury Value**: {len(contrarian_analysis.get('injury_analysis', {}).get('injury_value', []))} value plays

### **Situational Factors**
- **Must Win**: {', '.join(contrarian_analysis.get('situational_factors', {}).get('must_win', []))}
- **Revenge Games**: {', '.join(contrarian_analysis.get('situational_factors', {}).get('revenge_games', []))}
- **Lookahead Spots**: {', '.join(contrarian_analysis.get('situational_factors', {}).get('lookahead_spots', []))}
- **Short Weeks**: {', '.join(contrarian_analysis.get('situational_factors', {}).get('short_weeks', []))}
- **Extra Rest**: {', '.join(contrarian_analysis.get('situational_factors', {}).get('extra_rest', []))}

---

## 🎯 **OPTIMAL PICKS BREAKDOWN**

### **High Confidence Safety (20-16 points)**
"""

        # Add high confidence picks
        high_confidence_picks = [p for p in optimal_picks if p.get('confidence', 0) >= 16]
        for pick in high_confidence_picks:
            report += f"""
**{pick.get('game', 'N/A')} - {pick.get('team', 'N/A')} ({pick.get('confidence', 0)} pts)**
- **Reasoning**: {pick.get('reasoning', 'N/A')}
- **Contrarian Edge**: {pick.get('contrarian_edge', 'N/A')}
- **Value Play**: {pick.get('value_play', 'N/A')}
- **Risk Assessment**: {pick.get('risk_assessment', 'N/A')}
"""

        report += f"""
### **Medium Confidence Value (15-6 points)**
"""

        # Add medium confidence picks
        medium_confidence_picks = [p for p in optimal_picks if 6 <= p.get('confidence', 0) < 16]
        for pick in medium_confidence_picks:
            report += f"""
**{pick.get('game', 'N/A')} - {pick.get('team', 'N/A')} ({pick.get('confidence', 0)} pts)**
- **Reasoning**: {pick.get('reasoning', 'N/A')}
- **Contrarian Edge**: {pick.get('contrarian_edge', 'N/A')}
- **Value Play**: {pick.get('value_play', 'N/A')}
- **Risk Assessment**: {pick.get('risk_assessment', 'N/A')}
"""

        report += f"""
### **Low Confidence Upside (5-1 points)**
"""

        # Add low confidence picks
        low_confidence_picks = [p for p in optimal_picks if p.get('confidence', 0) < 6]
        for pick in low_confidence_picks:
            report += f"""
**{pick.get('game', 'N/A')} - {pick.get('team', 'N/A')} ({pick.get('confidence', 0)} pts)**
- **Reasoning**: {pick.get('reasoning', 'N/A')}
- **Contrarian Edge**: {pick.get('contrarian_edge', 'N/A')}
- **Value Play**: {pick.get('value_play', 'N/A')}
- **Risk Assessment**: {pick.get('risk_assessment', 'N/A')}
"""

        # Add strategy summary
        report += f"""
---

## 🚀 **STRATEGY FRAMEWORK**

### **High Confidence Safety**
{strategy_summary.get('high_confidence_safety', 'N/A')}

### **Medium Confidence Value**
{strategy_summary.get('medium_confidence_value', 'N/A')}

### **Low Confidence Upside**
{strategy_summary.get('low_confidence_upside', 'N/A')}

### **Competitive Edge**
{strategy_summary.get('competitive_edge', 'N/A')}

---

## 📈 **EXPECTED RESULTS**

### **High Confidence Picks ({len(high_confidence_picks)} picks)**
- **Expected**: 4-5 correct picks
- **Risk**: Low - clear favorites with advantages
- **Impact**: Foundation for pool success

### **Medium Confidence Picks ({len(medium_confidence_picks)} picks)**
- **Expected**: 6-8 correct picks
- **Risk**: Medium - good value with contrarian edge
- **Impact**: Differentiation from crowd

### **Low Confidence Picks ({len(low_confidence_picks)} picks)**
- **Expected**: 2-3 correct picks
- **Risk**: High - contrarian plays for differentiation
- **Impact**: Pool-winning upside potential

---

## 🔍 **NEXT WEEK CONSIDERATIONS**

### **Key Factors to Monitor**
1. **Injury Updates**: Track key player status changes
2. **Weather Conditions**: Monitor outdoor game forecasts
3. **Line Movement**: Watch for sharp money indicators
4. **Public Betting**: Identify new contrarian opportunities
5. **Situational Factors**: Look for must-win scenarios

### **Strategy Refinements**
1. **Review Results**: Analyze which picks worked/didn't work
2. **Adjust Confidence**: Refine confidence point assignment
3. **Update Analysis**: Incorporate new data sources
4. **Competitor Tracking**: Monitor other pool participants
5. **Value Detection**: Identify new value plays

### **Data Sources to Leverage**
1. **Weather API**: Real-time conditions for outdoor games
2. **Injury Reports**: Latest player status updates
3. **Betting Data**: Public vs sharp money analysis
4. **Team Analytics**: Performance trends and matchups
5. **Situational Factors**: Schedule, rest, motivation

---

## 💰 **MAXIMUM EARNINGS STRATEGY**

### **Competitive Advantages**
- **Contrarian Analysis**: Differentiate from crowd
- **Value Plays**: Target mispriced opportunities
- **Risk Management**: Balance safety with upside
- **Data Integration**: Leverage multiple data sources
- **Strategic Edge**: Use advanced analytics

### **Success Metrics**
- **Pick Accuracy**: Target 60-70% overall
- **Contrarian Success**: Beat public consensus
- **Value Capture**: Identify and exploit mispricings
- **Risk Management**: Minimize high-confidence losses
- **Pool Position**: Finish in top 10%

---

## 📁 **FILES GENERATED**

- **Excel File**: `data/excel/Dawgpac25_{date}.xlsx`
- **Analysis Data**: `data/json/week_{week}_complete_contrarian_analysis.json`
- **Strategy Report**: `reports/Week_{week}_Strategy_Report_{date}.md`
- **Prompt**: `data/prompts/{date}_contrarian_prompt.txt`

---

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Week {week} Strategy Report - {date}*
"""

        return report

    def generate_next_week_preview(self, week: int, date: str) -> str:
        """Generate next week preview with considerations."""

        # Calculate next week date
        current_date = datetime.strptime(date, "%Y-%m-%d")
        next_week_date = current_date + timedelta(days=7)
        next_week_str = next_week_date.strftime("%Y-%m-%d")

        preview_content = f"""# Week {week + 1} Preview - {next_week_str}

## 🔍 **NEXT WEEK CONSIDERATIONS**

### **Key Factors to Monitor**
1. **Injury Updates**: Track key player status changes
2. **Weather Conditions**: Monitor outdoor game forecasts
3. **Line Movement**: Watch for sharp money indicators
4. **Public Betting**: Identify new contrarian opportunities
5. **Situational Factors**: Look for must-win scenarios

### **Strategy Refinements**
1. **Review Results**: Analyze which picks worked/didn't work
2. **Adjust Confidence**: Refine confidence point assignment
3. **Update Analysis**: Incorporate new data sources
4. **Competitor Tracking**: Monitor other pool participants
5. **Value Detection**: Identify new value plays

### **Data Sources to Leverage**
1. **Weather API**: Real-time conditions for outdoor games
2. **Injury Reports**: Latest player status updates
3. **Betting Data**: Public vs sharp money analysis
4. **Team Analytics**: Performance trends and matchups
5. **Situational Factors**: Schedule, rest, motivation

---

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Week {week + 1} Preview - {next_week_str}*
"""

        return preview_content

    def generate_llm_enhanced_report(
        self,
        week: int,
        date: str,
        analysis_file: str,
        openrouter_api_key: Optional[str] = None
    ) -> str:
        """Generate LLM-enhanced strategy report with next week considerations."""

        # Load analysis data
        analysis_data = self._load_analysis_data(analysis_file)

        # Generate base report
        base_report = self._build_report_content(week, date, analysis_data, None)

        # Add LLM-enhanced next week considerations if API key available
        if openrouter_api_key:
            llm_analysis = self._get_llm_next_week_analysis(week, date, analysis_data, openrouter_api_key)
            base_report += f"\n\n## 🤖 **LLM-ENHANCED NEXT WEEK ANALYSIS**\n\n{llm_analysis}"
        else:
            # Add standard next week preview
            next_week_preview = self.generate_next_week_preview(week, date)
            base_report += f"\n\n{next_week_preview}"

        return base_report

    def _get_llm_next_week_analysis(
        self,
        week: int,
        date: str,
        analysis_data: Dict[str, Any],
        api_key: str
    ) -> str:
        """Get LLM analysis for next week considerations."""

        # Calculate next week date
        current_date = datetime.strptime(date, "%Y-%m-%d")
        next_week_date = current_date + timedelta(days=7)
        next_week_str = next_week_date.strftime("%Y-%m-%d")

        # Build prompt for LLM
        prompt = f"""Based on the Week {week} contrarian analysis, provide strategic insights for Week {week + 1} ({next_week_str}).

Current Week Analysis:
- Public Betting: {analysis_data.get('contrarian_analysis', {}).get('public_betting_analysis', {})}
- Weather Impact: {analysis_data.get('contrarian_analysis', {}).get('weather_impact', {})}
- Injury Analysis: {analysis_data.get('contrarian_analysis', {}).get('injury_analysis', {})}
- Situational Factors: {analysis_data.get('contrarian_analysis', {}).get('situational_factors', {})}

Please provide:
1. **Key Trends to Watch**: What patterns from Week {week} should we monitor?
2. **Contrarian Opportunities**: Where might public sentiment shift?
3. **Weather Considerations**: What weather factors will be important?
4. **Injury Impact**: Which injuries will have lasting effects?
5. **Situational Advantages**: What motivational factors will emerge?
6. **Strategy Adjustments**: How should we refine our approach?

Format as markdown with clear sections and actionable insights."""

        try:
            # Call OpenRouter API
            response = self._call_openrouter_api(prompt, api_key)
            return response
        except Exception as e:
            logger.error(f"Error getting LLM analysis: {e}")
            return f"*LLM analysis unavailable: {e}*"

    def _call_openrouter_api(self, prompt: str, api_key: str) -> str:
        """Call OpenRouter API for LLM analysis."""

        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "anthropic/claude-3.5-sonnet",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"]
