"""
Multi-LLM Analysis Integration

This module provides functionality to combine and analyze outputs from multiple LLMs
(Grok, ChatGPT, etc.) to create consensus picks and comprehensive analysis.
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime


class MultiLLMAnalyzer:
    """Analyzes and combines multiple LLM outputs for consensus picks."""

    def __init__(self):
        """Initialize the multi-LLM analyzer."""
        self.llm_weights = {
            'grok': 0.4,      # Grok gets 40% weight
            'chatgpt': 0.6    # ChatGPT gets 60% weight (more conservative)
        }

    def combine_analyses(self, analyses: Dict[str, Any], strategy: str = "consensus") -> Dict[str, Any]:
        """
        Combine multiple LLM analyses using specified strategy.

        Args:
            analyses: Dictionary of LLM analyses
            strategy: Combination strategy ('consensus', 'weighted', 'best')

        Returns:
            Combined analysis dictionary
        """
        if strategy == "consensus":
            return self._consensus_combination(analyses)
        elif strategy == "weighted":
            return self._weighted_combination(analyses)
        elif strategy == "best":
            return self._best_combination(analyses)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def _consensus_combination(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Combine analyses using consensus approach."""
        combined = {
            "public_betting_analysis": {},
            "weather_impact": {},
            "injury_analysis": {},
            "situational_factors": {},
            "contrarian_opportunities": [],
            "consensus_games": []
        }

        # Extract common elements across all analyses
        all_games = set()
        for llm_name, analysis in analyses.items():
            if 'contrarian_analysis' in analysis:
                ca = analysis['contrarian_analysis']

                # Collect all games mentioned
                for section in ['public_betting_analysis', 'weather_impact', 'injury_analysis']:
                    if section in ca:
                        for key, value in ca[section].items():
                            if isinstance(value, list):
                                all_games.update(value)

        # Find consensus games (mentioned by multiple LLMs)
        game_mentions = {}
        for llm_name, analysis in analyses.items():
            if 'contrarian_analysis' in analysis:
                ca = analysis['contrarian_analysis']
                for section in ['public_betting_analysis', 'weather_impact', 'injury_analysis']:
                    if section in ca:
                        for key, value in ca[section].items():
                            if isinstance(value, list):
                                for game in value:
                                    if game not in game_mentions:
                                        game_mentions[game] = []
                                    game_mentions[game].append(llm_name)

        # Games mentioned by multiple LLMs are consensus
        consensus_games = [game for game, mentions in game_mentions.items()
                           if len(mentions) > 1]

        combined["consensus_games"] = consensus_games

        return combined

    def _weighted_combination(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Combine analyses using weighted approach."""
        combined = {
            "weighted_analysis": {},
            "confidence_scores": {},
            "weighted_games": []
        }

        # Calculate weighted scores for each game
        game_scores = {}
        total_weight = sum(self.llm_weights.values())

        for llm_name, analysis in analyses.items():
            if 'contrarian_analysis' in analysis:
                weight = self.llm_weights.get(llm_name, 0.5)
                ca = analysis['contrarian_analysis']

                # Score games based on their appearance in different sections
                for section in ['public_betting_analysis', 'weather_impact', 'injury_analysis']:
                    if section in ca:
                        for key, value in ca[section].items():
                            if isinstance(value, list):
                                for game in value:
                                    if game not in game_scores:
                                        game_scores[game] = 0
                                    game_scores[game] += weight

        # Normalize scores
        if game_scores:
            max_score = max(game_scores.values())
            for game in game_scores:
                game_scores[game] = game_scores[game] / max_score

        combined["confidence_scores"] = game_scores
        combined["weighted_games"] = sorted(game_scores.items(),
                                          key=lambda x: x[1], reverse=True)

        return combined

    def _best_combination(self, analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Combine analyses by selecting the best from each LLM."""
        combined = {
            "best_analysis": {},
            "source_llm": {},
            "best_games": []
        }

        # Select best analysis from each LLM
        for llm_name, analysis in analyses.items():
            if 'contrarian_analysis' in analysis:
                ca = analysis['contrarian_analysis']

                # Find the most contrarian opportunities
                if 'public_betting_analysis' in ca:
                    contrarian_opps = ca['public_betting_analysis'].get('contrarian_opportunities', [])
                    if contrarian_opps:
                        combined["best_games"].extend(contrarian_opps)
                        combined["source_llm"][llm_name] = contrarian_opps

        # Remove duplicates while preserving order
        seen = set()
        unique_games = []
        for game in combined["best_games"]:
            if game not in seen:
                seen.add(game)
                unique_games.append(game)

        combined["best_games"] = unique_games

        return combined

    def generate_consensus_picks(self, combined_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate consensus picks from combined analysis.

        Args:
            combined_analysis: Combined analysis from multiple LLMs

        Returns:
            List of consensus picks with confidence points
        """
        picks = []
        confidence_points = list(range(20, 0, -1))  # 20 down to 1

        # Extract games based on combination strategy
        if "consensus_games" in combined_analysis:
            games = combined_analysis["consensus_games"][:20]  # Top 20
        elif "weighted_games" in combined_analysis:
            games = [game[0] for game in combined_analysis["weighted_games"][:20]]
        elif "best_games" in combined_analysis:
            games = combined_analysis["best_games"][:20]
        else:
            games = []

        # Create picks with confidence points
        for i, game in enumerate(games):
            if i < len(confidence_points):
                picks.append({
                    "game": game,
                    "team": self._extract_team_from_game(game),
                    "confidence": confidence_points[i],
                    "reasoning": f"Multi-LLM consensus pick #{i+1}",
                    "contrarian_edge": "High",
                    "value_play": "Yes",
                    "risk_assessment": "Medium"
                })

        return picks

    def _extract_team_from_game(self, game: str) -> str:
        """Extract team name from game string (e.g., 'TEAM@TEAM' -> 'TEAM')."""
        if '@' in game:
            return game.split('@')[0]
        return game

    def generate_multi_llm_report(self, analyses: Dict[str, Any],
                                 combined_analysis: Dict[str, Any],
                                 consensus_picks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate comprehensive report from multi-LLM analysis.

        Args:
            analyses: Individual LLM analyses
            combined_analysis: Combined analysis
            consensus_picks: Generated consensus picks

        Returns:
            Comprehensive report dictionary
        """
        report = {
            "summary": {
                "total_llms": len(analyses),
                "llm_names": list(analyses.keys()),
                "consensus_picks_count": len(consensus_picks),
                "analysis_date": datetime.now().isoformat()
            },
            "llm_comparison": {},
            "consensus_insights": {},
            "recommendations": []
        }

        # Compare LLM outputs
        for llm_name, analysis in analyses.items():
            if 'contrarian_analysis' in analysis:
                ca = analysis['contrarian_analysis']
                report["llm_comparison"][llm_name] = {
                    "contrarian_opportunities": len(ca.get('public_betting_analysis', {}).get('contrarian_opportunities', [])),
                    "weather_plays": len(ca.get('weather_impact', {}).get('weather_plays', [])),
                    "injury_value": len(ca.get('injury_analysis', {}).get('injury_value', []))
                }

        # Generate insights
        if consensus_picks:
            report["consensus_insights"] = {
                "top_confidence_picks": [p for p in consensus_picks if p["confidence"] >= 15],
                "value_plays": [p for p in consensus_picks if p["confidence"] >= 10 and p["confidence"] < 15],
                "contrarian_plays": [p for p in consensus_picks if p["confidence"] < 10]
            }

        # Generate recommendations
        report["recommendations"] = [
            "Focus on consensus picks with high confidence scores",
            "Consider weather and injury factors from multiple LLMs",
            "Monitor public betting patterns identified by consensus",
            "Use contrarian opportunities identified by multiple LLMs"
        ]

        return report
