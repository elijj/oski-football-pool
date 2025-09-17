#!/usr/bin/env python3
"""
Generate comprehensive markdown summary of Pool Week 1 picks with contrarian analysis.
"""

import json
from datetime import datetime


def generate_pick_summary():
    """Generate comprehensive markdown summary of Pool Week 1 picks."""

    # Load the contrarian analysis
    with open("week_1_contrarian_analysis.json") as f:
        analysis = json.load(f)

    # Generate markdown summary
    markdown_content = f"""# Pool Week 1 Contrarian Analysis Summary
**Date**: {analysis['date']}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Strategy**: Contrarian Analysis for Optimal Pool Performance

## 🎯 Executive Summary

This analysis implements a **contrarian strategy** designed to differentiate from the crowd and maximize value in a reverse scoring pool system. The approach focuses on:

- **High Confidence (20-16)**: SAFETY FIRST - Safest games with clear advantages
- **Medium Confidence (15-6)**: VALUE PLAYS - Contrarian opportunities and value plays
- **Low Confidence (5-1)**: UPSIDE PLAYS - High-risk, high-reward contrarian plays

## 📊 Contrarian Analysis Overview

### Public Betting Analysis
- **High Public Games**: {', '.join(analysis['contrarian_analysis']['public_betting_analysis']['high_public_games'])}
- **Contrarian Opportunities**: {', '.join(analysis['contrarian_analysis']['public_betting_analysis']['contrarian_opportunities'])}
- **Sharp Money Indicators**: {', '.join(analysis['contrarian_analysis']['public_betting_analysis']['sharp_money_indicators'])}

### Weather Impact
- **Outdoor Games**: {', '.join(analysis['contrarian_analysis']['weather_impact']['outdoor_games'])}
- **Weather Advantages**: {', '.join(analysis['contrarian_analysis']['weather_impact']['weather_advantages'])}
- **Weather Plays**: {', '.join(analysis['contrarian_analysis']['weather_impact']['weather_plays'])}

### Injury Analysis
- **Key Injuries**: {', '.join(analysis['contrarian_analysis']['injury_analysis']['key_injuries'])}
- **Public Overreactions**: {', '.join(analysis['contrarian_analysis']['injury_analysis']['public_overreactions'])}
- **Injury Value**: {', '.join(analysis['contrarian_analysis']['injury_analysis']['injury_value'])}

### Situational Factors
- **Must-Win Scenarios**: {', '.join(analysis['contrarian_analysis']['situational_factors']['must_win'])}
- **Revenge Games**: {', '.join(analysis['contrarian_analysis']['situational_factors']['revenge_games'])}
- **Lookahead Spots**: {', '.join(analysis['contrarian_analysis']['situational_factors']['lookahead_spots'])}
- **Short Weeks**: {', '.join(analysis['contrarian_analysis']['situational_factors']['short_weeks'])}
- **Extra Rest**: {', '.join(analysis['contrarian_analysis']['situational_factors']['extra_rest'])}

## 🏆 Optimal Picks Analysis

### HIGH CONFIDENCE PICKS (20-16): SAFETY FIRST

"""

    # Add high confidence picks
    high_confidence_picks = [pick for pick in analysis["optimal_picks"] if pick["confidence"] >= 16]
    for pick in high_confidence_picks:
        markdown_content += f"""#### {pick['confidence']}. {pick['team']} ({pick['game']})
- **Reasoning**: {pick['reasoning']}
- **Contrarian Edge**: {pick['contrarian_edge']}
- **Value Play**: {pick['value_play']}
- **Risk Assessment**: {pick['risk_assessment']}

"""

    markdown_content += """### MEDIUM CONFIDENCE PICKS (15-6): VALUE PLAYS

"""

    # Add medium confidence picks
    medium_confidence_picks = [
        pick for pick in analysis["optimal_picks"] if 6 <= pick["confidence"] < 16
    ]
    for pick in medium_confidence_picks:
        markdown_content += f"""#### {pick['confidence']}. {pick['team']} ({pick['game']})
- **Reasoning**: {pick['reasoning']}
- **Contrarian Edge**: {pick['contrarian_edge']}
- **Value Play**: {pick['value_play']}
- **Risk Assessment**: {pick['risk_assessment']}

"""

    markdown_content += """### LOW CONFIDENCE PICKS (5-1): UPSIDE PLAYS

"""

    # Add low confidence picks
    low_confidence_picks = [pick for pick in analysis["optimal_picks"] if pick["confidence"] < 6]
    for pick in low_confidence_picks:
        markdown_content += f"""#### {pick['confidence']}. {pick['team']} ({pick['game']})
- **Reasoning**: {pick['reasoning']}
- **Contrarian Edge**: {pick['contrarian_edge']}
- **Value Play**: {pick['value_play']}
- **Risk Assessment**: {pick['risk_assessment']}

"""

    markdown_content += f"""## 📈 Strategy Summary

### High Confidence Safety
{analysis['strategy_summary']['high_confidence_safety']}

### Medium Confidence Value
{analysis['strategy_summary']['medium_confidence_value']}

### Low Confidence Upside
{analysis['strategy_summary']['low_confidence_upside']}

### Competitive Edge
{analysis['strategy_summary']['competitive_edge']}

## 🎯 Key Strategic Insights

### 1. Contrarian Approach
- **Differentiation**: This strategy deliberately differs from the crowd
- **Value Focus**: Prioritizes value plays over just favorites
- **Risk Management**: Balances safety with upside potential

### 2. Weather Impact
- **Outdoor Games**: {len(analysis['contrarian_analysis']['weather_impact']['outdoor_games'])} games affected by weather
- **Weather Advantages**: {len(analysis['contrarian_analysis']['weather_impact']['weather_advantages'])} teams with weather advantages
- **Weather Plays**: {len(analysis['contrarian_analysis']['weather_impact']['weather_plays'])} contrarian weather plays

### 3. Injury Analysis
- **Key Injuries**: {len(analysis['contrarian_analysis']['injury_analysis']['key_injuries'])} teams with key injuries
- **Public Overreactions**: {len(analysis['contrarian_analysis']['injury_analysis']['public_overreactions'])} teams where public overreacts
- **Injury Value**: {len(analysis['contrarian_analysis']['injury_analysis']['injury_value'])} teams with injury value

### 4. Situational Factors
- **Must-Win Scenarios**: {len(analysis['contrarian_analysis']['situational_factors']['must_win'])} teams in must-win situations
- **Revenge Games**: {len(analysis['contrarian_analysis']['situational_factors']['revenge_games'])} revenge game opportunities
- **Lookahead Spots**: {len(analysis['contrarian_analysis']['situational_factors']['lookahead_spots'])} teams in lookahead spots
- **Short Weeks**: {len(analysis['contrarian_analysis']['situational_factors']['short_weeks'])} teams with short weeks
- **Extra Rest**: {len(analysis['contrarian_analysis']['situational_factors']['extra_rest'])} teams with extra rest

## 🚀 Implementation Recommendations

### 1. High Confidence Strategy
- Focus on **7+ point spreads** with clear advantages
- Avoid games where public is **>80%** on one side
- Consider **weather, injuries, situational factors**
- Minimize risk of major point losses

### 2. Medium Confidence Strategy
- Target **contrarian opportunities**
- Find games where **public is wrong**
- Look for **weather plays** others ignore
- Identify **injury value plays**

### 3. Low Confidence Strategy
- Use **contrarian plays** for differentiation
- Target **weather-dependent teams**
- Find **underdog value**
- Focus on **situational motivation**

## 📊 Risk Assessment Summary

| Confidence Level | Picks | Strategy | Risk Level |
|------------------|-------|----------|------------|
| High (20-16) | {len(high_confidence_picks)} | Safety First | LOW |
| Medium (15-6) | {len(medium_confidence_picks)} | Value Plays | MEDIUM |
| Low (5-1) | {len(low_confidence_picks)} | Upside Plays | HIGH |

## 🎯 Competitive Advantages

1. **Contrarian Analysis**: Differentiates from the crowd
2. **Value Focus**: Prioritizes value over just favorites
3. **Weather Impact**: Leverages weather advantages
4. **Injury Analysis**: Identifies public overreactions
5. **Situational Factors**: Finds motivational edges
6. **Risk Management**: Balances safety with upside

## 📈 Expected Outcomes

- **High Confidence**: 90%+ accuracy target (18+ correct out of 20)
- **Medium Confidence**: 70%+ accuracy target (7+ correct out of 10)
- **Low Confidence**: 50%+ accuracy target (2.5+ correct out of 5)
- **Overall**: 65%+ total accuracy (13+ correct out of 20)

---

**Generated by**: Football Pool Domination System
**Strategy**: Contrarian Analysis for Optimal Performance
**Date**: {analysis['date']}
**Status**: Ready for Implementation
"""

    # Save the markdown file
    filename = "Pool_Week_1_Contrarian_Analysis_Summary.md"
    with open(filename, "w") as f:
        f.write(markdown_content)

    print(f"✅ Generated comprehensive pick summary: {filename}")
    return filename


if __name__ == "__main__":
    generate_pick_summary()
