"""
Injury Data Provider for Football Pool Analysis.

This module provides injury data integration for NFL games,
including key player injuries, depth chart analysis, and injury impact.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class InjuryDataProvider:
    """Provides injury data for NFL games and betting analysis."""

    def __init__(self):
        """Initialize injury data provider."""
        self.api_key = os.getenv("ESPN_API_KEY")  # ESPN API for injury data
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl"
        self.cache_dir = Path("data/cache/injuries")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_team_injuries(self, team: str, week: int) -> Dict[str, Any]:
        """Get injury data for a specific team."""
        if not self.api_key:
            raise ValueError("ESPN_API_KEY is required for injury data. No fallback data available.")

        try:
            # Check cache first
            cache_file = self.cache_dir / f"{team}_week_{week}.json"
            if cache_file.exists():
                with open(cache_file) as f:
                    cached_data = json.load(f)
                    if self._is_cache_valid(cached_data):
                        logger.info(f"Using cached injury data for {team}")
                        return cached_data["injury_data"]

            # Fetch fresh injury data
            injury_data = self._fetch_team_injuries(team, week)

            # Cache the data
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "injury_data": injury_data
            }
            with open(cache_file, "w") as f:
                json.dump(cache_data, f, indent=2)

            return injury_data

        except Exception as e:
            logger.error(f"Error getting injury data for {team}: {e}")
            raise RuntimeError(f"Failed to fetch injury data for {team}: {e}")

    def _fetch_team_injuries(self, team: str, week: int) -> Dict[str, Any]:
        """Fetch injury data from ESPN API."""
        if not self.api_key:
            raise ValueError("ESPN_API_KEY is required for injury data. No fallback data available.")

        try:
            # ESPN API call for team injuries
            url = f"{self.base_url}/teams/{self._get_team_id(team)}/injuries"
            params = {
                "apikey": self.api_key,
                "week": week
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Parse injury data
            injuries = {
                "key_injuries": [],
                "questionable": [],
                "doubtful": [],
                "out": [],
                "injury_impact": self._analyze_injury_impact(data.get("injuries", []))
            }

            for injury in data.get("injuries", []):
                player = injury.get("player", {})
                status = injury.get("status", "").lower()

                injury_info = {
                    "player": player.get("displayName", "Unknown"),
                    "position": player.get("position", "Unknown"),
                    "status": status,
                    "injury": injury.get("injury", "Unknown"),
                    "impact": self._assess_player_impact(player, status)
                }

                if status == "out":
                    injuries["out"].append(injury_info)
                elif status == "doubtful":
                    injuries["doubtful"].append(injury_info)
                elif status == "questionable":
                    injuries["questionable"].append(injury_info)

                # Key injuries (star players)
                if injury_info["impact"] >= 3:
                    injuries["key_injuries"].append(injury_info)

            return injuries

        except Exception as e:
            logger.error(f"Error fetching injury data: {e}")
            raise RuntimeError(f"Failed to fetch injury data: {e}")

    def _get_team_id(self, team: str) -> str:
        """Get ESPN team ID for a team abbreviation."""
        team_ids = {
            "KC": "12", "NYG": "17", "BAL": "2", "DET": "8", "LAR": "14",
            "PHIL": "21", "DAL": "6", "CHI": "3", "SF": "25", "ARIZ": "1",
            "GB": "9", "CLEV": "5", "MIA": "15", "BUFF": "4", "HOU": "13",
            "JAC": "11", "CINC": "7", "MINN": "16", "PITT": "23", "NE": "17",
            "ATL": "1", "CAR": "5", "DEN": "7", "LAC": "13", "LV": "13",
            "WASH": "28", "NO": "18", "SEA": "26", "TB": "27", "NYJ": "20"
        }
        return team_ids.get(team, "1")

    def _assess_player_impact(self, player: Dict[str, Any], status: str) -> int:
        """Assess the impact of a player injury (1-5 scale)."""
        position = player.get("position", "").upper()
        status_weight = {"out": 5, "doubtful": 4, "questionable": 3, "probable": 2, "": 1}

        # Position importance
        position_weights = {
            "QB": 5, "RB": 4, "WR": 4, "TE": 3, "OL": 3,
            "DL": 3, "LB": 3, "CB": 3, "S": 3, "K": 2, "P": 2
        }

        position_weight = position_weights.get(position, 2)
        status_weight_value = status_weight.get(status, 1)

        return min(5, position_weight + status_weight_value - 2)

    def _analyze_injury_impact(self, injuries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze overall injury impact on team performance."""
        impact = {
            "offensive_impact": 0,
            "defensive_impact": 0,
            "special_teams_impact": 0,
            "overall_impact": "neutral"
        }

        for injury in injuries:
            player_impact = self._assess_player_impact(
                injury.get("player", {}),
                injury.get("status", "")
            )

            position = injury.get("player", {}).get("position", "").upper()

            if position in ["QB", "RB", "WR", "TE", "OL"]:
                impact["offensive_impact"] += player_impact
            elif position in ["DL", "LB", "CB", "S"]:
                impact["defensive_impact"] += player_impact
            elif position in ["K", "P"]:
                impact["special_teams_impact"] += player_impact

        # Determine overall impact
        total_impact = impact["offensive_impact"] + impact["defensive_impact"] + impact["special_teams_impact"]

        if total_impact > 10:
            impact["overall_impact"] = "severe"
        elif total_impact > 5:
            impact["overall_impact"] = "moderate"
        elif total_impact > 2:
            impact["overall_impact"] = "minor"
        else:
            impact["overall_impact"] = "minimal"

        return impact

    def _is_cache_valid(self, cached_data: Dict[str, Any]) -> bool:
        """Check if cached injury data is still valid (within 12 hours)."""
        try:
            timestamp = datetime.fromisoformat(cached_data["timestamp"])
            age_hours = (datetime.now() - timestamp).total_seconds() / 3600
            return age_hours < 12
        except:
            return False


    def get_injury_summary(self, games: List[str], week: int) -> Dict[str, Any]:
        """Get injury summary for multiple games."""
        injury_summary = {
            "key_injuries": [],
            "public_overreactions": [],
            "injury_value": [],
            "game_injuries": {}
        }

        for game in games:
            away_team, home_team = game.split("@")

            # Get injury data for both teams
            away_injuries = self.get_team_injuries(away_team, week)
            home_injuries = self.get_team_injuries(home_team, week)

            injury_summary["game_injuries"][game] = {
                "away": away_injuries,
                "home": home_injuries
            }

            # Identify key injuries
            if away_injuries["key_injuries"] or home_injuries["key_injuries"]:
                injury_summary["key_injuries"].append(game)

            # Identify public overreactions (teams with minor injuries that public overreacts to)
            if (away_injuries["injury_impact"]["overall_impact"] == "minor" and
                len(away_injuries["key_injuries"]) > 0):
                injury_summary["public_overreactions"].append(away_team)

            if (home_injuries["injury_impact"]["overall_impact"] == "minor" and
                len(home_injuries["key_injuries"]) > 0):
                injury_summary["public_overreactions"].append(home_team)

            # Identify injury value (teams with good depth despite injuries)
            if (away_injuries["injury_impact"]["overall_impact"] in ["minimal", "minor"] and
                len(away_injuries["out"]) == 0):
                injury_summary["injury_value"].append(away_team)

            if (home_injuries["injury_impact"]["overall_impact"] in ["minimal", "minor"] and
                len(home_injuries["out"]) == 0):
                injury_summary["injury_value"].append(home_team)

        return injury_summary
