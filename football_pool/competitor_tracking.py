"""
Competitor Tracking System for Football Pool Analysis.

This module provides competitor pick tracking and analysis
to identify contrarian opportunities and avoid common picks.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class CompetitorTracker:
    """Tracks competitor picks and identifies contrarian opportunities."""

    def __init__(self):
        """Initialize competitor tracker."""
        self.data_dir = Path("data/competitors")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.tracking_file = self.data_dir / "competitor_picks.json"

    def track_competitor_pick(self, competitor: str, week: int, game: str,
                            team: str, confidence: int) -> None:
        """Track a competitor's pick."""
        try:
            # Load existing data
            data = self._load_tracking_data()

            # Add new pick
            if week not in data:
                data[week] = {}

            if competitor not in data[week]:
                data[week][competitor] = []

            pick = {
                "game": game,
                "team": team,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat()
            }

            data[week][competitor].append(pick)

            # Save updated data
            self._save_tracking_data(data)
            logger.info(f"Tracked pick for {competitor}: {team} in {game}")

        except Exception as e:
            logger.error(f"Error tracking competitor pick: {e}")

    def get_competitor_analysis(self, week: int) -> Dict[str, Any]:
        """Get competitor analysis for a specific week."""
        try:
            data = self._load_tracking_data()

            if week not in data:
                return self._get_default_analysis()

            week_data = data[week]

            # Analyze competitor picks
            analysis = {
                "total_competitors": len(week_data),
                "common_picks": self._find_common_picks(week_data),
                "contrarian_opportunities": self._find_contrarian_opportunities(week_data),
                "avoid_picks": self._find_avoid_picks(week_data),
                "competitor_patterns": self._analyze_competitor_patterns(week_data)
            }

            return analysis

        except Exception as e:
            logger.error(f"Error getting competitor analysis: {e}")
            return self._get_default_analysis()

    def _find_common_picks(self, week_data: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """Find picks that multiple competitors are making."""
        pick_counts = {}

        for competitor, picks in week_data.items():
            for pick in picks:
                key = f"{pick['game']}_{pick['team']}"
                if key not in pick_counts:
                    pick_counts[key] = {
                        "game": pick["game"],
                        "team": pick["team"],
                        "count": 0,
                        "competitors": []
                    }

                pick_counts[key]["count"] += 1
                pick_counts[key]["competitors"].append(competitor)

        # Return picks with 2+ competitors
        common_picks = [
            pick for pick in pick_counts.values()
            if pick["count"] >= 2
        ]

        return sorted(common_picks, key=lambda x: x["count"], reverse=True)

    def _find_contrarian_opportunities(self, week_data: Dict[str, List[Dict]]) -> List[Dict[str, Any]]:
        """Find games where competitors are heavily on one side."""
        game_analysis = {}

        for competitor, picks in week_data.items():
            for pick in picks:
                game = pick["game"]
                team = pick["team"]

                if game not in game_analysis:
                    game_analysis[game] = {"teams": {}, "total_picks": 0}

                if team not in game_analysis[game]["teams"]:
                    game_analysis[game]["teams"][team] = 0

                game_analysis[game]["teams"][team] += 1
                game_analysis[game]["total_picks"] += 1

        # Find games with heavy bias
        contrarian_opportunities = []

        for game, analysis in game_analysis.items():
            if analysis["total_picks"] >= 3:  # Need at least 3 picks to analyze
                teams = list(analysis["teams"].items())
                teams.sort(key=lambda x: x[1], reverse=True)

                if len(teams) >= 2:
                    top_team = teams[0]
                    second_team = teams[1]

                    # If top team has 70%+ of picks, other side is contrarian
                    top_percentage = top_team[1] / analysis["total_picks"]

                    if top_percentage >= 0.7:
                        contrarian_opportunities.append({
                            "game": game,
                            "public_team": top_team[0],
                            "contrarian_team": second_team[0],
                            "public_percentage": round(top_percentage * 100, 1),
                            "contrarian_percentage": round((1 - top_percentage) * 100, 1)
                        })

        return contrarian_opportunities

    def _find_avoid_picks(self, week_data: Dict[str, List[Dict]]) -> List[str]:
        """Find picks to avoid (too many competitors on them)."""
        pick_counts = {}

        for competitor, picks in week_data.items():
            for pick in picks:
                key = f"{pick['game']}_{pick['team']}"
                pick_counts[key] = pick_counts.get(key, 0) + 1

        # Avoid picks with 50%+ of competitors
        total_competitors = len(week_data)
        avoid_picks = [
            pick for pick, count in pick_counts.items()
            if count >= total_competitors * 0.5
        ]

        return avoid_picks

    def _analyze_competitor_patterns(self, week_data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """Analyze competitor picking patterns."""
        patterns = {
            "favorite_pickers": [],
            "underdog_pickers": [],
            "high_confidence_pickers": [],
            "low_confidence_pickers": []
        }

        for competitor, picks in week_data.items():
            if not picks:
                continue

            # Analyze picking patterns
            avg_confidence = sum(pick["confidence"] for pick in picks) / len(picks)

            # Categorize competitors
            if avg_confidence >= 15:
                patterns["high_confidence_pickers"].append(competitor)
            elif avg_confidence <= 10:
                patterns["low_confidence_pickers"].append(competitor)

            # Analyze favorite vs underdog tendencies
            favorite_picks = sum(1 for pick in picks if pick["confidence"] >= 15)
            underdog_picks = sum(1 for pick in picks if pick["confidence"] <= 10)

            if favorite_picks > underdog_picks:
                patterns["favorite_pickers"].append(competitor)
            elif underdog_picks > favorite_picks:
                patterns["underdog_pickers"].append(competitor)

        return patterns

    def _load_tracking_data(self) -> Dict[str, Any]:
        """Load competitor tracking data."""
        if not self.tracking_file.exists():
            return {}

        try:
            with open(self.tracking_file) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading tracking data: {e}")
            return {}

    def _save_tracking_data(self, data: Dict[str, Any]) -> None:
        """Save competitor tracking data."""
        try:
            with open(self.tracking_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving tracking data: {e}")

    def _get_default_analysis(self) -> Dict[str, Any]:
        """Get default analysis when no data is available."""
        return {
            "total_competitors": 0,
            "common_picks": [],
            "contrarian_opportunities": [],
            "avoid_picks": [],
            "competitor_patterns": {
                "favorite_pickers": [],
                "underdog_pickers": [],
                "high_confidence_pickers": [],
                "low_confidence_pickers": []
            }
        }

    def get_contrarian_recommendations(self, week: int, games: List[str]) -> List[Dict[str, Any]]:
        """Get contrarian recommendations based on competitor analysis."""
        analysis = self.get_competitor_analysis(week)

        recommendations = []

        for game in games:
            # Check if this game has contrarian opportunities
            for opportunity in analysis["contrarian_opportunities"]:
                if opportunity["game"] == game:
                    recommendations.append({
                        "game": game,
                        "recommended_team": opportunity["contrarian_team"],
                        "avoid_team": opportunity["public_team"],
                        "reasoning": f"Only {opportunity['contrarian_percentage']}% of competitors on {opportunity['contrarian_team']}",
                        "contrarian_edge": "High - Different from crowd"
                    })

        return recommendations

    def export_competitor_data(self, week: int) -> str:
        """Export competitor data for analysis."""
        try:
            data = self._load_tracking_data()

            if week not in data:
                return "No data available for this week"

            week_data = data[week]
            analysis = self.get_competitor_analysis(week)

            export_data = {
                "week": week,
                "export_timestamp": datetime.now().isoformat(),
                "competitor_picks": week_data,
                "analysis": analysis
            }

            export_file = self.data_dir / f"week_{week}_export.json"
            with open(export_file, "w") as f:
                json.dump(export_data, f, indent=2)

            return str(export_file)

        except Exception as e:
            logger.error(f"Error exporting competitor data: {e}")
            return "Error exporting data"
