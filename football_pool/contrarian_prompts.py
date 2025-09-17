"""
Enhanced LLM prompts for contrarian analysis and optimal strategy implementation.
"""


def generate_contrarian_analysis_prompt(date: str, games: list) -> str:
    """Generate enhanced prompt for contrarian analysis and optimal strategy."""

    games_list = "\n".join([f"- {game}" for game in games])

    prompt = f"""# {date} CONTRARIAN FOOTBALL POOL ANALYSIS
**GOAL**: Identify contrarian opportunities and value plays for optimal pool strategy

## CRITICAL POOL CONTEXT:
- **Scoring System**: REVERSE (lowest points win)
- **High Confidence Wrong**: 20 points added (devastating)
- **Strategy**: Must be DIFFERENT from the crowd
- **Focus**: VALUE plays, not just favorites
- **Competitive Edge**: Contrarian analysis wins pools

## Games to Analyze:
{games_list}

## CONTRARIAN ANALYSIS REQUIREMENTS:

### 1. PUBLIC BETTING ANALYSIS
For each game, analyze:
- **Public Betting Percentage**: What % of public is on each side
- **Contrarian Opportunities**: Games where public is >70% on one side
- **Sharp Money Indicators**: Line movement vs public betting
- **Value Identification**: Games where public is wrong

### 2. WEATHER IMPACT ASSESSMENT
For outdoor games, analyze:
- **Weather Conditions**: Temperature, wind, precipitation
- **Weather-Dependent Teams**: Which teams benefit/suffer from conditions
- **Public Weather Ignorance**: Weather factors public ignores
- **Weather Plays**: Contrarian opportunities based on conditions
- **Wind Impact**: Passing vs running game advantages
- **Temperature Effects**: Cold weather vs warm weather teams
- **Precipitation**: Rain/snow impact on game strategy

### 3. INJURY IMPACT ANALYSIS
For each game, assess:
- **Key Player Injuries**: Star players out/questionable
- **Public Overreaction**: Injuries public overreacts to
- **Depth Analysis**: Teams with good depth vs injury-prone
- **Injury Value**: Underrated impact of role player injuries
- **Position Impact**: QB vs RB vs WR vs defensive injuries
- **Backup Analysis**: Quality of backup players
- **Injury Trends**: Teams with injury-prone players

### 4. COMPETITOR ANALYSIS
For each game, analyze:
- **Common Picks**: Games where multiple competitors are on same side
- **Contrarian Opportunities**: Games where competitors are heavily on one side
- **Avoid Picks**: Games where 50%+ of competitors are on same team
- **Competitor Patterns**: Favorite vs underdog tendencies
- **Differentiation Strategy**: How to be different from crowd

### 5. SITUATIONAL FACTORS
Identify:
- **Must-Win Scenarios**: Teams with playoff implications
- **Revenge Games**: Emotional motivation factors
- **Lookahead Spots**: Teams looking ahead to bigger games
- **Short Weeks**: Teams with less rest/preparation
- **Extra Rest**: Teams with advantage from bye weeks

### 5. VALUE PLAY IDENTIFICATION
Find:
- **Mispriced Odds**: Games with incorrect spreads
- **Situational Advantages**: Teams with motivational edges
- **Weather Advantages**: Teams that excel in specific conditions
- **Injury Advantages**: Teams with depth vs injury-plagued opponents
- **Contrarian Value**: Games where public is wrong

## OPTIMAL STRATEGY FRAMEWORK:

### HIGH CONFIDENCE (20-16): SAFETY FIRST
- **SAFEST games, not just favorites**
- **7+ point spreads with clear advantages**
- **Avoid games where public is >80% on one side**
- **Consider weather, injuries, situational factors**
- **Minimize risk of major point losses**

### MEDIUM CONFIDENCE (15-6): VALUE PLAYS
- **Contrarian opportunities**
- **Games where public is wrong**
- **Weather plays others ignore**
- **Injury value plays**
- **Situational advantages**

### LOW CONFIDENCE (5-1): UPSIDE PLAYS
- **High-risk, high-reward picks**
- **Contrarian plays for differentiation**
- **Weather-dependent teams**
- **Underdog value**
- **Situational motivation**

## REQUIRED JSON FORMAT:
```json
{{
  "date": "{date}",
  "contrarian_analysis": {{
    "public_betting_analysis": {{
      "high_public_games": ["game1", "game2"],
      "contrarian_opportunities": ["game3", "game4"],
      "sharp_money_indicators": ["game5", "game6"]
    }},
    "weather_impact": {{
      "outdoor_games": ["game1", "game2"],
      "weather_advantages": ["team1", "team2"],
      "weather_plays": ["game3", "game4"]
    }},
    "injury_analysis": {{
      "key_injuries": ["team1", "team2"],
      "public_overreactions": ["team3", "team4"],
      "injury_value": ["team5", "team6"]
    }},
    "situational_factors": {{
      "must_win": ["team1", "team2"],
      "revenge_games": ["team3", "team4"],
      "lookahead_spots": ["team5", "team6"],
      "short_weeks": ["team7", "team8"],
      "extra_rest": ["team9", "team10"]
    }}
  }},
  "optimal_picks": [
    {{
      "game": "KC@NYG",
      "team": "KC",
      "confidence": 20,
      "reasoning": "SAFEST pick - 7+ point spread, home field, no key injuries",
      "contrarian_edge": "Public only 65% on KC, sharp money agrees",
      "value_play": "Weather favors KC's offense, NYG's defense struggles",
      "risk_assessment": "LOW - Clear favorite with multiple advantages"
    }},
    {{
      "game": "ATL@CAR",
      "team": "ATL",
      "confidence": 15,
      "reasoning": "VALUE play - Public overreacting to CAR's recent struggles",
      "contrarian_edge": "Public 75% on CAR, but ATL has situational advantage",
      "value_play": "ATL's offense matches up well vs CAR's defense",
      "risk_assessment": "MEDIUM - Good value with contrarian edge"
    }},
    {{
      "game": "DEN@LAC",
      "team": "DEN",
      "confidence": 5,
      "reasoning": "UPSIDE play - Weather favors DEN's running game",
      "contrarian_edge": "Public 80% on LAC, but weather levels playing field",
      "value_play": "DEN's defense can contain LAC's passing attack",
      "risk_assessment": "HIGH - Contrarian play with weather advantage"
    }}
  ],
  "strategy_summary": {{
    "high_confidence_safety": "Focus on 7+ point spreads with clear advantages",
    "medium_confidence_value": "Target contrarian opportunities and value plays",
    "low_confidence_upside": "Use contrarian plays for differentiation",
    "competitive_edge": "Differentiate from crowd with contrarian analysis"
  }}
}}
```

## CRITICAL INSTRUCTIONS:
1. **ANALYZE ALL GAMES** for contrarian opportunities
2. **IDENTIFY PUBLIC MISTAKES** where crowd is wrong
3. **FIND VALUE PLAYS** with contrarian edges
4. **BALANCE SAFETY** with upside potential
5. **DIFFERENTIATE** from the crowd
6. **FOCUS ON VALUE**, not just favorites
7. **IMPLEMENT OPTIMAL STRATEGY** for pool success

Please provide your contrarian analysis in the exact JSON format above."""

    return prompt


def generate_enhanced_llm_prompt(date: str, games: list) -> str:
    """Generate enhanced LLM prompt with contrarian focus."""

    games_list = "\n".join([f"- {game}" for game in games])

    prompt = f"""# {date} ENHANCED FOOTBALL POOL ANALYSIS
**STRATEGY**: Contrarian analysis for optimal pool performance

## POOL CONTEXT:
- **Scoring**: REVERSE (lowest points win)
- **High Confidence Risk**: 20 points added if wrong
- **Competitive Edge**: Must be different from crowd
- **Focus**: VALUE plays, not just favorites

## Games to Analyze:
{games_list}

## ENHANCED ANALYSIS REQUIREMENTS:

### 1. CONTRARIAN OPPORTUNITY IDENTIFICATION
- **Public Betting Percentages**: What % of public is on each side
- **Contrarian Games**: Where public is >70% on one side
- **Sharp Money Indicators**: Line movement vs public betting
- **Value Identification**: Games where public is wrong

### 2. WEATHER IMPACT ANALYSIS
- **Outdoor Game Conditions**: Temperature, wind, precipitation
- **Weather-Dependent Teams**: Which teams benefit/suffer
- **Public Weather Ignorance**: Factors public ignores
- **Weather Plays**: Contrarian opportunities

### 3. INJURY IMPACT ASSESSMENT
- **Key Player Injuries**: Star players out/questionable
- **Public Overreaction**: Injuries public overreacts to
- **Depth Analysis**: Teams with good depth vs injury-prone
- **Injury Value**: Underrated impact of role player injuries

### 4. SITUATIONAL FACTORS
- **Must-Win Scenarios**: Playoff implications
- **Revenge Games**: Emotional motivation
- **Lookahead Spots**: Teams looking ahead
- **Short Weeks**: Less rest/preparation
- **Extra Rest**: Bye week advantages

### 5. VALUE PLAY IDENTIFICATION
- **Mispriced Odds**: Incorrect spreads
- **Situational Advantages**: Motivational edges
- **Weather Advantages**: Specific conditions
- **Injury Advantages**: Depth vs injury-plagued
- **Contrarian Value**: Public mistakes

## OPTIMAL STRATEGY IMPLEMENTATION:

### HIGH CONFIDENCE (20-16): SAFETY FIRST
- **SAFEST games, not just favorites**
- **7+ point spreads with clear advantages**
- **Avoid games where public is >80% on one side**
- **Consider weather, injuries, situational factors**
- **Minimize risk of major point losses**

### MEDIUM CONFIDENCE (15-6): VALUE PLAYS
- **Contrarian opportunities**
- **Games where public is wrong**
- **Weather plays others ignore**
- **Injury value plays**
- **Situational advantages**

### LOW CONFIDENCE (5-1): UPSIDE PLAYS
- **High-risk, high-reward picks**
- **Contrarian plays for differentiation**
- **Weather-dependent teams**
- **Underdog value**
- **Situational motivation**

## REQUIRED JSON FORMAT:
```json
{{
  "date": "{date}",
  "contrarian_analysis": {{
    "public_betting_analysis": {{
      "high_public_games": ["game1", "game2"],
      "contrarian_opportunities": ["game3", "game4"],
      "sharp_money_indicators": ["game5", "game6"]
    }},
    "weather_impact": {{
      "outdoor_games": ["game1", "game2"],
      "weather_advantages": ["team1", "team2"],
      "weather_plays": ["game3", "game4"]
    }},
    "injury_analysis": {{
      "key_injuries": ["team1", "team2"],
      "public_overreactions": ["team3", "team4"],
      "injury_value": ["team5", "team6"]
    }},
    "situational_factors": {{
      "must_win": ["team1", "team2"],
      "revenge_games": ["team3", "team4"],
      "lookahead_spots": ["team5", "team6"],
      "short_weeks": ["team7", "team8"],
      "extra_rest": ["team9", "team10"]
    }}
  }},
  "optimal_picks": [
    {{
      "game": "KC@NYG",
      "team": "KC",
      "confidence": 20,
      "reasoning": "SAFEST pick - 7+ point spread, home field, no key injuries",
      "contrarian_edge": "Public only 65% on KC, sharp money agrees",
      "value_play": "Weather favors KC's offense, NYG's defense struggles",
      "risk_assessment": "LOW - Clear favorite with multiple advantages"
    }}
  ],
  "strategy_summary": {{
    "high_confidence_safety": "Focus on 7+ point spreads with clear advantages",
    "medium_confidence_value": "Target contrarian opportunities and value plays",
    "low_confidence_upside": "Use contrarian plays for differentiation",
    "competitive_edge": "Differentiate from crowd with contrarian analysis"
  }}
}}
```

## CRITICAL INSTRUCTIONS:
1. **ANALYZE ALL GAMES** for contrarian opportunities
2. **IDENTIFY PUBLIC MISTAKES** where crowd is wrong
3. **FIND VALUE PLAYS** with contrarian edges
4. **BALANCE SAFETY** with upside potential
5. **DIFFERENTIATE** from the crowd
6. **FOCUS ON VALUE**, not just favorites
7. **IMPLEMENT OPTIMAL STRATEGY** for pool success

Please provide your enhanced analysis in the exact JSON format above."""

    return prompt
