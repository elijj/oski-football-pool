"""
pool_analyzer.py - Strategy and Analysis Engine
Main analyzer with all optimization strategies
"""

import logging
import os

# Import core components
import sys

sys.path.append(os.path.dirname(__file__))
from pool_core import PoolDatabase, ScheduleManager

logger = logging.getLogger(__name__)


class PoolDominationSystem:
    """
    Complete system for dominating your football confidence pool
    """

    def __init__(self, db_path: str = "pool_tracker.db"):
        self.db = PoolDatabase(db_path)
        self.schedule = ScheduleManager.get_schedule()
        self.current_week = 1
        self.pool_position = {"rank": 1, "total": 20, "points_behind": 0}
        self.variance_strategy = "balanced"

    # ============= VARIANCE MANAGEMENT =============

    def calculate_variance_need(
        self, current_week: int, my_score: int, leader_score: int, weeks_remaining: int
    ) -> str:
        """Dynamically calculate how much variance/risk you need"""
        deficit = leader_score - my_score
        avg_needed_per_week = deficit / max(weeks_remaining, 1)

        logger.info(f"Week {current_week}: Deficit={deficit}, Avg needed={avg_needed_per_week:.1f}")

        if avg_needed_per_week > 15:
            return "maximum_variance"
        elif avg_needed_per_week > 8:
            return "high_variance"
        elif deficit < -30:
            return "protective"
        else:
            return "balanced"

    # ============= GAME ANALYSIS =============

    def identify_correlated_games(self, week_games: list[str]) -> list[dict]:
        """Find games whose outcomes affect each other"""
        correlations = []
        teams_playing = {}

        for game in week_games:
            if "@" in game:
                away, home = game.split("@")
                teams_playing[away] = game
                teams_playing[home] = game

        # Division correlations
        divisions = {
            "AFC West": ["KC", "DEN", "LV", "LAC"],
            "NFC North": ["GB", "DET", "MINN", "CHI"],
            "AFC North": ["BALT", "PITT", "CLEV", "CINC"],
            "NFC East": ["DAL", "PHIL", "NYG", "WASH"],
        }

        for div_name, teams in divisions.items():
            division_games = [teams_playing.get(team) for team in teams if team in teams_playing]
            division_games = [g for g in division_games if g]  # Remove None values

            if len(division_games) > 1:
                correlations.append(
                    {
                        "type": "divisional",
                        "division": div_name,
                        "games": list(set(division_games)),
                        "impact": "high",
                    }
                )

        return correlations

    def calculate_game_state_value(self, game: str, week: int, extra_info: dict = None) -> float:
        """Calculate situational value adjustments"""
        value = 0

        if extra_info:
            # Injury impacts
            if "backup" in extra_info.get("injuries", "").lower():
                value -= 20
            elif "questionable" in extra_info.get("injuries", "").lower():
                value -= 5

            # Motivational factors
            if extra_info.get("must_win"):
                value += 15
            if extra_info.get("playoff_eliminated"):
                value -= 15
            if extra_info.get("playoff_clinched"):
                value -= 10

            # Situational spots
            if extra_info.get("revenge_game"):
                value += 5
            if extra_info.get("lookahead_spot"):
                value -= 8
            if extra_info.get("sandwich_spot"):
                value -= 7
            if extra_info.get("short_week"):
                value -= 5
            if extra_info.get("extra_rest"):
                value += 3

        # Week-specific adjustments
        if week == 13:  # Thanksgiving week
            value += 5  # Home teams perform well
        elif week == 14:  # Championship week
            value += 10  # Favorites dominate
        elif week >= 17:  # Final weeks
            value -= 5  # Chaos reigns

        return value

    def find_ownership_arbitrage(
        self, game: str, public_pct: float, sharp_pct: float = None
    ) -> dict:
        """Find games where public and sharps disagree"""
        arbitrage = {"game": game, "opportunity": False, "direction": None, "strength": 0}

        # Heavy public play
        if public_pct > 75:
            arbitrage["opportunity"] = True
            arbitrage["direction"] = "fade_public"
            arbitrage["strength"] = min((public_pct - 75) / 25 * 10, 10)

        # Contrarian spot
        elif public_pct < 30:
            arbitrage["opportunity"] = True
            arbitrage["direction"] = "contrarian"
            arbitrage["strength"] = min((30 - public_pct) / 30 * 10, 10)

        # Sharp divergence
        if sharp_pct and abs(public_pct - sharp_pct) > 20:
            arbitrage["opportunity"] = True
            arbitrage["direction"] = "follow_sharps" if sharp_pct > public_pct else "fade_sharps"
            arbitrage["strength"] = min(abs(public_pct - sharp_pct) / 20 * 10, 10)

        return arbitrage

    # ============= POINT ASSIGNMENT =============

    def fibonacci_confidence_assignment(self, games: list[dict]) -> list[dict]:
        """Use Fibonacci-like gaps for point assignment"""
        # Sort by confidence
        games.sort(key=lambda x: x.get("confidence_score", 50), reverse=True)

        # Unique confidence points from 20 down to 1
        points = [
            20, 19, 18, 17, 16, 15, 14, 13, 12, 11,
            10, 9, 8, 7, 6, 5, 4, 3, 2, 1
        ]

        for i, game in enumerate(games[:20]):
            game["confidence_points"] = points[i] if i < len(points) else 1

        return games[:20]

    # ============= SPECIAL WEEK HANDLING =============

    def identify_pool_killer_weeks(self, week: int) -> dict:
        """Identify weeks with maximum upset potential"""
        pool_killers = {
            3: {
                "name": "Reality Check",
                "variance": "high",
                "notes": "First real test, early season surprises",
            },
            8: {
                "name": "Trade Deadline",
                "variance": "medium",
                "notes": "Teams adjusting to roster changes",
            },
            9: {
                "name": "Marquee Matchups",
                "variance": "low",
                "notes": "PSU@OSU, USC@NEB - big games, clear favorites",
            },
            13: {
                "name": "Thanksgiving Chaos",
                "variance": "very_high",
                "notes": "Emotions high, division rivalries, OSU@MICH",
            },
            14: {
                "name": "Championship Week",
                "variance": "very_low",
                "notes": "Most predictable - load up on favorites",
            },
            17: {
                "name": "Playoff Positioning",
                "variance": "extreme",
                "notes": "Some teams resting, others fighting for life",
            },
            18: {
                "name": "Motivation Roulette",
                "variance": "extreme",
                "notes": "Who needs it? Who's sitting starters?",
            },
        }

        return pool_killers.get(
            week,
            {"name": "Standard Week", "variance": "medium", "notes": "Normal variance expected"},
        )

    # ============= ANTI-CONSENSUS ENGINE =============

    def generate_anti_consensus_picks(self, picks: list[dict], variance_level: str) -> list[dict]:
        """Systematically fade the field based on variance needs"""
        # Sort by public agreement
        picks.sort(key=lambda x: x.get("public_pct", 50), reverse=True)

        flips_needed = {"protective": 0, "balanced": 1, "high_variance": 3, "maximum_variance": 5}
