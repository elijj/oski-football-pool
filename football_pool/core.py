"""
Core Football Pool Domination System.

This module contains the main PoolDominationSystem class that orchestrates
all functionality for the football pool system.
"""

import json
import logging
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import requests
from dotenv import load_dotenv

from .database import DatabaseManager
from .logging_config import logger as app_logger
from .models import Pick, PoolPosition
from .web_search import FootballWebSearch
from .weather_data import WeatherDataProvider
from .injury_data import InjuryDataProvider
from .competitor_tracking import CompetitorTracker

logger = logging.getLogger(__name__)


class APIUsageTracker:
    """Track API usage to stay within monthly limits."""

    def __init__(self):
        self.usage_file = Path("api_usage.json")
        self.monthly_limits = {
            "odds_api": 500,
            "openrouter": 1000,  # Assuming higher limit for OpenRouter
        }
        self.usage_data = self._load_usage_data()

    def _load_usage_data(self) -> dict[str, Any]:
        """Load usage data from file."""
        if not self.usage_file.exists():
            return {
                "odds_api": {"current_month": None, "requests_used": 0, "last_reset": None},
                "openrouter": {"current_month": None, "requests_used": 0, "last_reset": None},
            }

        try:
            with open(self.usage_file) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading usage data: {e}")
            return {
                "odds_api": {"current_month": None, "requests_used": 0, "last_reset": None},
                "openrouter": {"current_month": None, "requests_used": 0, "last_reset": None},
            }

    def _save_usage_data(self):
        """Save usage data to file."""
        try:
            with open(self.usage_file, "w") as f:
                json.dump(self.usage_data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving usage data: {e}")

    def _check_month_reset(self, api_name: str):
        """Check if we need to reset monthly usage."""
        current_month = datetime.now().strftime("%Y-%m")
        api_data = self.usage_data[api_name]

        if api_data["current_month"] != current_month:
            api_data["current_month"] = current_month
            api_data["requests_used"] = 0
            api_data["last_reset"] = datetime.now().isoformat()
            self._save_usage_data()

    def can_make_request(self, api_name: str) -> bool:
        """Check if we can make a request without exceeding limits."""
        if api_name not in self.usage_data:
            return True

        self._check_month_reset(api_name)
        api_data = self.usage_data[api_name]
        limit = self.monthly_limits.get(api_name, 1000)

        return api_data["requests_used"] < limit

    def record_request(self, api_name: str, success: bool = True):
        """Record an API request."""
        if api_name not in self.usage_data:
            self.usage_data[api_name] = {
                "current_month": None,
                "requests_used": 0,
                "last_reset": None,
            }

        self._check_month_reset(api_name)
        self.usage_data[api_name]["requests_used"] += 1
        self._save_usage_data()

        if success:
            logger.info(
                f"Recorded {api_name} request. Usage: {self.usage_data[api_name]['requests_used']}/{self.monthly_limits.get(api_name, 1000)}"
            )

    def get_usage_stats(self) -> dict[str, Any]:
        """Get current usage statistics."""
        stats = {}
        for api_name, data in self.usage_data.items():
            limit = self.monthly_limits.get(api_name, 1000)
            remaining = limit - data["requests_used"]
            percentage = (data["requests_used"] / limit) * 100

            stats[api_name] = {
                "used": data["requests_used"],
                "limit": limit,
                "remaining": max(0, remaining),
                "percentage": percentage,
                "current_month": data["current_month"],
                "last_reset": data["last_reset"],
            }

        return stats

    def get_warning_level(self, api_name: str) -> str:
        """Get warning level based on usage percentage."""
        if api_name not in self.usage_data:
            return "safe"

        api_data = self.usage_data[api_name]
        limit = self.monthly_limits.get(api_name, 1000)
        percentage = (api_data["requests_used"] / limit) * 100

        if percentage >= 90:
            return "critical"
        elif percentage >= 75:
            return "warning"
        elif percentage >= 50:
            return "caution"
        else:
            return "safe"


class PoolDominationSystem:
    """
    Complete system for dominating your football confidence pool.

    This class provides all the core functionality including:
    - Pick generation and optimization
    - Strategy selection based on pool position
    - LLM integration for enhanced analysis
    - Performance tracking and analytics
    - Competitor analysis
    """

    def __init__(self, db_path: str = "pool_tracker.db"):
        """Initialize the system with database connection."""
        # Load environment variables
        load_dotenv()

        self.db = DatabaseManager(db_path)
        self.current_week = 1
        self.pool_position = PoolPosition(
            rank=1,
            total_players=20,
            points_behind_leader=0,
            points_ahead_of_last=0,
            weekly_scores=[],
            cumulative_score=0,
            weeks_remaining=16,
        )

        # API Keys
        self.odds_api_key = os.getenv("THE_ODDS_API_KEY")
        self.openrouter_api_key = os.getenv("OPENROUTER_API_KEY")

        # API Configuration
        self.odds_api_base = "https://api.the-odds-api.com/v4"
        self.openrouter_api_base = "https://openrouter.ai/api/v1"

        # API Usage Tracking
        self.usage_tracker = APIUsageTracker()

        # Web Search Integration
        self.web_search = FootballWebSearch(os.getenv("SMITHERY_API_KEY"))

        # Weather Data Integration
        self.weather_provider = WeatherDataProvider()

        # Injury Data Integration
        self.injury_provider = InjuryDataProvider()

        # Competitor Tracking Integration
        self.competitor_tracker = CompetitorTracker()

        # Validate required API keys for live data
        self._validate_api_keys()

        # Strategy thresholds
        self.variance_thresholds = {
            "protective": 30,  # Leading by 30+ points
            "balanced": 0,  # Within 30 points
            "high_variance": -50,  # Behind by 50-150 points
            "maximum_variance": -150,  # Behind by 150+ points
        }

        # Team power ratings (example - should be updated with real data)
        self.team_power_ratings = {
            "KC": 95,
            "BALT": 92,
            "SF": 91,
            "BUF": 90,
            "DAL": 89,
            "PHIL": 88,
            "MIA": 87,
            "DET": 86,
            "CLEV": 85,
            "HOU": 84,
            "GB": 83,
            "LAR": 82,
            "SEA": 81,
            "TB": 80,
            "IND": 79,
            "CINC": 78,
            "PITT": 77,
            "LV": 76,
            "NO": 75,
            "ATL": 74,
            "CHI": 73,
            "NYG": 72,
            "WASH": 71,
            "CAR": 70,
            "DEN": 69,
            "NYJ": 68,
            "TENN": 67,
            "JAC": 66,
            "LAC": 65,
            "MINN": 64,
            "ARIZ": 63,
            "NE": 62,
            "CLEV": 61,
            "GB": 60,
        }

        # Schedule data
        self.schedule = self._load_schedule()

    def _load_schedule(self) -> dict[int, dict[str, Any]]:
        """Load the complete season schedule from the Excel file."""
        try:
            import os

            import pandas as pd

            # Try to load from the Excel file
            excel_file = "2025-2026 Football Schedule.xlsx"
            if os.path.exists(excel_file):
                df = pd.read_excel(excel_file, header=None)

                schedule = {}

                # Process each week column
                for col in range(9):  # 9 weeks
                    week_num = col + 1

                    # Get date range (row 2)
                    date_range = df.iloc[2, col]
                    if pd.notna(date_range):
                        # Get games for this week (rows 3 onwards)
                        games = []
                        for row in range(3, len(df)):
                            game = df.iloc[row, col]
                            if pd.notna(game) and str(game).strip() and str(game).strip() != "BYE":
                                game_str = str(game).strip()
                                # Skip header rows, week references, dates, and mixed data
                                if not any(
                                    x in game_str
                                    for x in [
                                        "Week",
                                        "Champ",
                                        "TBD",
                                        "ARMY@NAVY",
                                        "/",
                                        "2025-2026",
                                        "11/",
                                        "12/",
                                        "1/",
                                    ]
                                ):
                                    # Only include games with @ symbol (actual games)
                                    if "@" in game_str:
                                        games.append(game_str)

                        if games:
                            schedule[week_num] = {"dates": str(date_range), "games": games}

                return schedule
            else:
                logger.warning(f"Excel file {excel_file} not found, using default schedule")
                return self._get_default_schedule()

        except Exception as e:
            logger.error(f"Error loading schedule from Excel: {e}")
            return self._get_default_schedule()

    def _get_default_schedule(self) -> dict[int, dict[str, Any]]:
        """Get default schedule as fallback."""
        return {
            1: {"dates": "9/4-9/8", "games": ["BYE", "BYE"]},
            2: {"dates": "9/11-9/15", "games": ["BYE", "BYE"]},
            3: {
                "dates": "9/18-9/22",
                "games": [
                    "CAL@SDSU",
                    "STAN@VA",
                    "UW@WSU",
                    "FLA@Mia,F",
                    "MIA@BUFF",
                    "ATL@CAR",
                    "GB@CLEV",
                    "HOU@JAC",
                    "CINC@MINN",
                    "PITT@NE",
                    "LAR@PHIL",
                    "NYJ@TB",
                    "IND@TENN",
                    "LV@WASH",
                    "DEN@LAC",
                    "NO@SEA",
                    "DAL@CHI",
                    "ARIZ@SF",
                    "KC@NYG",
                    "DET@BALT",
                ],
            },
            4: {
                "dates": "9/25-9/29",
                "games": [
                    "CAL@BC",
                    "SJSU@STAN",
                    "ORE@PSU",
                    "ALA@GEO",
                    "SEA@ARIZ",
                    "MINN@PITT",
                    "WASH@ATL",
                    "NO@BUFF",
                    "CLEV@DET",
                    "TENN@HOU",
                    "CAR@NE",
                    "LAC@NYG",
                    "PHIL@TB",
                    "IND@LAR",
                    "JAC@SF",
                    "BALT@KC",
                    "CHI@LV",
                    "GB@DAL",
                    "NYJ@MIA",
                    "CINC@DEN",
                ],
            },
            # Add more weeks as needed...
        }

    # ============= CORE PICK GENERATION =============

    def generate_optimal_picks(self, week: int, llm_data: Optional[dict] = None) -> list[Pick]:
        """Generate optimal picks for the specified week."""
        logger.info(f"Generating picks for Week {week}")

        # Get week's games
        week_games = self.schedule.get(week, {}).get("games", [])
        if not week_games or week_games == ["BYE", "BYE"]:
            raise ValueError(f"No games scheduled for Week {week}")

        # Determine strategy based on pool position
        strategy = self._determine_strategy()

        # Generate picks based on strategy
        if strategy == "protective":
            picks = self._generate_protective_picks(week, week_games, llm_data)
        elif strategy == "balanced":
            picks = self._generate_balanced_picks(week, week_games, llm_data)
        elif strategy == "high_variance":
            picks = self._generate_high_variance_picks(week, week_games, llm_data)
        elif strategy == "maximum_variance":
            picks = self._generate_maximum_variance_picks(week, week_games, llm_data)
        else:
            picks = self._generate_balanced_picks(week, week_games, llm_data)

        # Apply Fibonacci point assignment
        picks = self._apply_fibonacci_assignment(picks)

        # Add strategy tags
        for pick in picks:
            pick.strategy_tag = strategy
            pick.week = week

        logger.info(f"Generated {len(picks)} picks using {strategy} strategy")
        return picks

    def _determine_strategy(self) -> str:
        """Determine optimal strategy based on pool position."""
        deficit = self.pool_position.points_behind_leader

        if deficit < -30:
            return "protective"
        elif deficit < 0:
            return "balanced"
        elif deficit < 50:
            return "high_variance"
        else:
            return "maximum_variance"

    def _generate_protective_picks(
        self, week: int, games: list[str], llm_data: Optional[dict]
    ) -> list[Pick]:
        """Generate conservative picks to protect a lead."""
        picks = []

        for game in games:
            if "@" in game:
                away, home = game.split("@")

                # Use power ratings and spreads for conservative picks
                away_rating = self.team_power_ratings.get(away, 50)
                home_rating = self.team_power_ratings.get(home, 50)

                # Home field advantage
                home_rating += 3

                # Determine favorite
                if home_rating > away_rating + 5:
                    predicted_winner = home
                    confidence = min(85, 50 + (home_rating - away_rating) * 2)
                elif away_rating > home_rating + 5:
                    predicted_winner = away
                    confidence = min(85, 50 + (away_rating - home_rating) * 2)
                else:
                    # Skip close games in protective mode
                    continue

                pick = Pick(
                    game=game,
                    predicted_winner=predicted_winner,
                    confidence_points=1,  # Will be assigned later
                    conf=confidence,
                    spread=home_rating - away_rating,
                    public_pct=50,  # Default, should be updated with real data
                )
                picks.append(pick)

        return picks[:20]  # Limit to 20 picks

    def _generate_balanced_picks(
        self, week: int, games: list[str], llm_data: Optional[dict]
    ) -> list[Pick]:
        """Generate balanced picks with moderate risk."""
        picks = []

        for game in games:
            if "@" in game:
                away, home = game.split("@")

                # Use power ratings
                away_rating = self.team_power_ratings.get(away, 50)
                home_rating = self.team_power_ratings.get(home, 50)
                home_rating += 3  # Home field advantage

                # Calculate confidence
                rating_diff = abs(home_rating - away_rating)
                confidence = 50 + min(35, rating_diff * 1.5)

                # Determine winner
                if home_rating > away_rating:
                    predicted_winner = home
                else:
                    predicted_winner = away

                pick = Pick(
                    game=game,
                    predicted_winner=predicted_winner,
                    confidence_points=1,
                    conf=confidence,
                    spread=home_rating - away_rating,
                    public_pct=50,
                )
                picks.append(pick)

        return picks[:20]

    def _generate_high_variance_picks(
        self, week: int, games: list[str], llm_data: Optional[dict]
    ) -> list[Pick]:
        """Generate picks with higher variance for catching up."""
        picks = []

        for game in games:
            if "@" in game:
                away, home = game.split("@")

                # Use power ratings but add more variance
                away_rating = self.team_power_ratings.get(away, 50)
                home_rating = self.team_power_ratings.get(home, 50)
                home_rating += 3

                # Add random variance for underdog picks
                variance = random.uniform(-10, 10)
                away_rating += variance
                home_rating += variance

                # Calculate confidence with more risk
                rating_diff = abs(home_rating - away_rating)
                confidence = 50 + min(40, rating_diff * 1.2)

                # Sometimes pick the underdog
                if random.random() < 0.3:  # 30% chance to pick underdog
                    if home_rating > away_rating:
                        predicted_winner = away
                    else:
                        predicted_winner = home
                else:
                    if home_rating > away_rating:
                        predicted_winner = home
                    else:
                        predicted_winner = away

                pick = Pick(
                    game=game,
                    predicted_winner=predicted_winner,
                    confidence_points=1,
                    conf=confidence,
                    spread=home_rating - away_rating,
                    public_pct=50,
                )
                picks.append(pick)

        return picks[:20]

    def _generate_maximum_variance_picks(
        self, week: int, games: list[str], llm_data: Optional[dict]
    ) -> list[Pick]:
        """Generate maximum variance picks for desperate situations."""
        picks = []

        for game in games:
            if "@" in game:
                away, home = game.split("@")

                # Use power ratings but with maximum variance
                away_rating = self.team_power_ratings.get(away, 50)
                home_rating = self.team_power_ratings.get(home, 50)
                home_rating += 3

                # Add significant variance
                variance = random.uniform(-20, 20)
                away_rating += variance
                home_rating += variance

                # High confidence on contrarian picks
                confidence = random.uniform(60, 90)

                # Often pick the underdog
                if random.random() < 0.6:  # 60% chance to pick underdog
                    if home_rating > away_rating:
                        predicted_winner = away
                    else:
                        predicted_winner = home
                else:
                    if home_rating > away_rating:
                        predicted_winner = home
                    else:
                        predicted_winner = away

                pick = Pick(
                    game=game,
                    predicted_winner=predicted_winner,
                    confidence_points=1,
                    conf=confidence,
                    spread=home_rating - away_rating,
                    public_pct=50,
                )
                picks.append(pick)

        return picks[:20]

    def _apply_fibonacci_assignment(self, picks: list[Pick]) -> list[Pick]:
        """Apply Fibonacci-like point assignment to picks."""
        # Sort by confidence
        picks.sort(key=lambda x: x.conf or 0, reverse=True)

        # Unique confidence points from 20 down to 1
        points = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

        for i, pick in enumerate(picks[:20]):
            pick.confidence_points = points[i] if i < len(points) else 1

        return picks[:20]

    # ============= ODDS API INTEGRATION =============

    def fetch_odds_data(self, week: int, force_refresh: bool = False) -> dict[str, Any]:
        """Fetch real odds data from The Odds API with caching to minimize requests."""
        if not self.odds_api_key:
            logger.warning("No odds API key found. Using default data.")
            return self._get_default_odds_data(week)

        # Check usage limits first
        if not self.usage_tracker.can_make_request("odds_api"):
            warning_level = self.usage_tracker.get_warning_level("odds_api")
            logger.warning(f"Odds API limit reached! Warning level: {warning_level}")
            # Try to return cached data
            cached_data = self._get_cached_odds(week)
            if cached_data:
                logger.info("Returning cached odds data due to API limit")
                return cached_data
            return self._get_default_odds_data(week)

        # Check cache first
        if not force_refresh:
            cached_data = self._get_cached_odds(week)
            if cached_data:
                logger.info(f"Using cached odds data for Week {week}")
                return cached_data

        try:
            # Get games for the week
            week_games = self.schedule.get(week, {}).get("games", [])
            if not week_games or week_games == ["BYE", "BYE"]:
                return {}

            # Fetch all odds in a single API call to minimize requests
            odds_data = self._fetch_week_odds_batch(week)

            # Record the API request
            self.usage_tracker.record_request("odds_api", success=True)

            # Cache the results
            self._cache_odds_data(week, odds_data)

            logger.info(f"Fetched odds data for {len(odds_data)} games in Week {week}")
            return odds_data

        except Exception as e:
            logger.error(f"Error fetching odds data: {e}")
            # Record failed request
            self.usage_tracker.record_request("odds_api", success=False)
            # Try to return cached data if available
            cached_data = self._get_cached_odds(week)
            if cached_data:
                logger.info("Returning cached odds data due to API error")
                return cached_data
            return self._get_default_odds_data(week)

    def _fetch_week_odds_batch(self, week: int) -> dict[str, Any]:
        """Fetch odds for all games in a week with a single API call."""
        try:
            # Single API call for all NFL games
            url = f"{self.odds_api_base}/sports/americanfootball_nfl/odds"
            params = {
                "apiKey": self.odds_api_key,
                "regions": "us",
                "markets": "spreads",
                "oddsFormat": "american",
                "dateFormat": "iso",
            }

            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()

            all_games = response.json()
            week_games = self.schedule.get(week, {}).get("games", [])

            # Filter and map to our week's games
            odds_data = {}
            for game_str in week_games:
                if "@" in game_str and game_str != "BYE":
                    away, home = game_str.split("@")
                    away_api = self._map_team_to_api(away)
                    home_api = self._map_team_to_api(home)

                    if away_api and home_api:
                        # Find matching game in API response
                        for api_game in all_games:
                            if (
                                api_game.get("away_team") == away_api
                                and api_game.get("home_team") == home_api
                            ) or (
                                api_game.get("away_team") == home_api
                                and api_game.get("home_team") == away_api
                            ):
                                parsed_odds = self._parse_odds_data(api_game, away, home)
                                if parsed_odds:
                                    odds_data[game_str] = parsed_odds
                                break

            logger.info(f"Batch fetched odds for {len(odds_data)} games in Week {week}")
            return odds_data

        except Exception as e:
            logger.error(f"Error in batch odds fetch: {e}")
            return {}

    def _get_cached_odds(self, week: int) -> Optional[dict[str, Any]]:
        """Get cached odds data if available and not expired."""
        try:
            cache_file = Path(f"cache_odds_week_{week}.json")
            if not cache_file.exists():
                return None

            # Check if cache is less than 6 hours old
            cache_age = datetime.now().timestamp() - cache_file.stat().st_mtime
            if cache_age > 21600:  # 6 hours
                cache_file.unlink()
                return None

            with open(cache_file) as f:
                return json.load(f)

        except Exception as e:
            logger.error(f"Error reading odds cache: {e}")
            return None

    def _cache_odds_data(self, week: int, odds_data: dict[str, Any]) -> None:
        """Cache odds data to file."""
        try:
            cache_file = Path(f"cache_odds_week_{week}.json")
            with open(cache_file, "w") as f:
                json.dump(odds_data, f, indent=2)
            logger.info(f"Cached odds data for Week {week}")
        except Exception as e:
            logger.error(f"Error caching odds data: {e}")

    def _fetch_game_odds(self, away_team: str, home_team: str) -> Optional[dict[str, Any]]:
        """Fetch odds for a specific game (deprecated - use batch method)."""
        logger.warning(
            "Individual game odds fetch is deprecated. Use batch method to minimize API calls."
        )
        return None

    def _map_team_to_api(self, team: str) -> Optional[str]:
        """Map team names to API format."""
        team_mapping = {
            "KC": "Kansas City Chiefs",
            "BALT": "Baltimore Ravens",
            "SF": "San Francisco 49ers",
            "BUF": "Buffalo Bills",
            "DAL": "Dallas Cowboys",
            "PHIL": "Philadelphia Eagles",
            "MIA": "Miami Dolphins",
            "DET": "Detroit Lions",
            "CLEV": "Cleveland Browns",
            "HOU": "Houston Texans",
            "GB": "Green Bay Packers",
            "LAR": "Los Angeles Rams",
            "SEA": "Seattle Seahawks",
            "TB": "Tampa Bay Buccaneers",
            "IND": "Indianapolis Colts",
            "CINC": "Cincinnati Bengals",
            "PITT": "Pittsburgh Steelers",
            "LV": "Las Vegas Raiders",
            "NO": "New Orleans Saints",
            "ATL": "Atlanta Falcons",
            "CHI": "Chicago Bears",
            "NYG": "New York Giants",
            "WASH": "Washington Commanders",
            "CAR": "Carolina Panthers",
            "DEN": "Denver Broncos",
            "NYJ": "New York Jets",
            "TENN": "Tennessee Titans",
            "JAC": "Jacksonville Jaguars",
            "LAC": "Los Angeles Chargers",
            "MINN": "Minnesota Vikings",
            "ARIZ": "Arizona Cardinals",
            "NE": "New England Patriots",
        }
        return team_mapping.get(team)

    def _parse_odds_data(self, game_data: dict, away_team: str, home_team: str) -> dict[str, Any]:
        """Parse odds data from API response."""
        try:
            # Get the best spread odds
            best_spread = None
            best_odds = None

            for bookmaker in game_data.get("bookmakers", []):
                for market in bookmaker.get("markets", []):
                    if market.get("key") == "spreads":
                        for outcome in market.get("outcomes", []):
                            if outcome.get("name") == home_team:
                                spread = outcome.get("point", 0)
                                odds = outcome.get("price", 0)
                                if best_spread is None or abs(spread) < abs(best_spread):
                                    best_spread = spread
                                    best_odds = odds

            return {
                "spread": best_spread,
                "odds": best_odds,
                "away_team": away_team,
                "home_team": home_team,
                "game_time": game_data.get("commence_time"),
                "last_updated": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"Error parsing odds data: {e}")
            return {}

    def _get_default_odds_data(self, week: int) -> dict[str, Any]:
        """Get default odds data when API is unavailable."""
        week_games = self.schedule.get(week, {}).get("games", [])
        default_data = {}

        for game in week_games:
            if "@" in game and game != "BYE":
                # Generate default spread based on team ratings
                away, home = game.split("@")
                away_rating = self.team_power_ratings.get(away, 50)
                home_rating = self.team_power_ratings.get(home, 50)
                home_rating += 3  # Home field advantage

                spread = home_rating - away_rating
                default_data[game] = {
                    "spread": spread,
                    "odds": -110,
                    "away_team": away,
                    "home_team": home,
                    "game_time": None,
                    "last_updated": datetime.now().isoformat(),
                    "source": "default",
                }

        return default_data

    def get_enhanced_llm_prompt(self, date: str, force_refresh: bool = False) -> str:
        """Generate enhanced LLM prompt with real odds data and web search context."""
        # Fetch real odds data for the date
        odds_data = self.fetch_odds_data_by_date(date, force_refresh)

        # Generate base prompt
        base_prompt = self.generate_llm_research_prompt_by_date(date)

        # Add odds data to prompt
        if odds_data:
            odds_section = "\n\n## Current Odds Data:\n"
            for game, data in odds_data.items():
                spread = data.get("spread", 0) or 0
                odds = data.get("odds", -110) or -110
                odds_section += f"- {game}: {spread:+.1f} ({odds:+d})\n"

            enhanced_prompt = base_prompt + odds_section
        else:
            enhanced_prompt = base_prompt

        # Add web search context for better analysis
        web_context = self._get_web_search_context_by_date(date)
        if web_context:
            enhanced_prompt += web_context

        return enhanced_prompt

    def _get_web_search_context(self, week: int) -> str:
        """Get web search context for enhanced analysis."""
        # Get games for the week
        week_games = self.schedule.get(week, {}).get("games", [])
        if not week_games or week_games == ["BYE", "BYE"]:
            return ""

        # Use real web search for enhanced context - no fallbacks
        web_context = self.web_search.get_enhanced_context(week, week_games)

        if web_context:
            logger.info(f"🔍 Generated web search context for Week {week}")
            return web_context
        else:
            logger.warning(f"No web search context generated for Week {week}")
            return ""

    def _get_web_search_context_by_date(self, date: str) -> str:
        """Get web search context for enhanced analysis by date."""
        # Use real web search for enhanced context - no fallbacks
        web_context = self.web_search.get_enhanced_context_by_date(date)

        if web_context:
            logger.info(f"🔍 Generated web search context for {date}")
            return web_context
        else:
            logger.warning(f"No web search context generated for {date}")
            return ""

    def fetch_odds_data_by_date(self, date: str, force_refresh: bool = False) -> dict[str, Any]:
        """Fetch odds data for a specific date."""
        try:
            # For now, return empty data - this would need to be implemented
            # based on the actual odds API date format
            logger.info(f"Fetching odds data for {date}")
            return {}
        except Exception as e:
            logger.error(f"Error fetching odds data for {date}: {e}")
            return {}

    def _get_week_from_date(self, date: str) -> int:
        """Get week number from date string (YYYY-MM-DD format)."""
        try:
            from datetime import datetime, timedelta

            target_date = datetime.strptime(date, "%Y-%m-%d")

            # Find the week that contains this date
            for week, data in self.schedule.items():
                if "dates" in data:
                    # Parse date range (e.g., "9/18-9/22")
                    date_range = data["dates"]
                    if "-" in date_range:
                        start_str, end_str = date_range.split("-")
                        # Parse start date (e.g., "9/18" -> "2024-09-18")
                        start_parts = start_str.split("/")
                        start_date = datetime(2024, int(start_parts[0]), int(start_parts[1]))
                        # Parse end date (e.g., "9/22" -> "2024-09-22")
                        end_parts = end_str.split("/")
                        end_date = datetime(2024, int(end_parts[0]), int(end_parts[1]))

                        # Check if the target date falls within the week's game dates
                        if start_date <= target_date <= end_date:
                            return week
                        # Also check if it's the day before (due date)
                        elif start_date - timedelta(days=1) <= target_date < start_date:
                            return week

            # Default to week 3 if not found
            return 3

        except Exception as e:
            logger.error(f"Error parsing date {date}: {e}")
            return 3

    def generate_llm_research_prompt_by_date(self, date: str) -> str:
        """Generate research prompt for LLM analysis by date."""
        # Get the week and games for this date
        week = self._get_week_from_date(date)
        week_data = self.schedule.get(week, {})
        games = week_data.get("games", [])
        date_range = week_data.get("dates", date)

        # Filter out BYE games
        actual_games = [game for game in games if game != "BYE"]

        if not actual_games:
            return f"# {date} Football Pool Research Request\n\nNo games scheduled for this date."

        # Create games list for the prompt
        games_list = "\n".join([f"- {game}" for game in actual_games])

        prompt = f"""# {date} Football Pool Research Request

Please analyze the following games and provide structured data in JSON format:

## Games to Analyze:
{games_list}

## Required Analysis for Each Game:
1. **Current Spread**: Vegas spread (e.g., -7.5 for home team favored by 7.5)
2. **Public Betting Percentage**: What % of public is betting on each side
3. **Injury Reports**: Key injuries affecting the game
4. **Weather Conditions**: Impact on outdoor games
5. **Situational Factors**:
   - Must-win scenarios
   - Revenge games
   - Lookahead spots
   - Short weeks
   - Extra rest
6. **Confidence Score**: Your confidence in each pick (0-100)

## Required JSON Format:
```json
{{
  "date": "{date}",
  "games": [
    {{
      "game": "KC@NYG",
      "spread": -7.5,
      "public_percentage": 65,
      "injuries": "KC: Mahomes questionable, NYG: Barkley out",
      "weather": "Clear, 45°F",
      "situational_factors": {{
        "must_win": false,
        "revenge_game": false,
        "lookahead_spot": false,
        "short_week": false,
        "extra_rest": false
      }},
      "confidence_score": 78
    }}
  ]
}}
```

Please provide your analysis in the exact JSON format above."""
        return prompt

    def generate_contrarian_analysis_prompt_by_date(self, date: str) -> str:
        """Generate enhanced contrarian analysis prompt for optimal strategy."""
        # Get the week and games for this date
        week = self._get_week_from_date(date)
        week_data = self.schedule.get(week, {})
        games = week_data.get("games", [])
        date_range = week_data.get("dates", date)

        # Filter out BYE games
        actual_games = [game for game in games if game != "BYE"]

        if not actual_games:
            return (
                f"# {date} CONTRARIAN FOOTBALL POOL ANALYSIS\n\nNo games scheduled for this date."
            )

        # Limit to 20 games for the pool (select the first 20 games)
        pool_games = actual_games[:20]

        if len(actual_games) > 20:
            logger.warning(
                f"Week {week} has {len(actual_games)} games, limiting to 20 for pool analysis"
            )

        # Create games list for the prompt
        games_list = "\n".join([f"- {game}" for game in pool_games])

        prompt = f"""# {date} CONTRARIAN FOOTBALL POOL ANALYSIS
**GOAL**: Identify contrarian opportunities and value plays for optimal pool strategy

## CRITICAL POOL CONTEXT:
- **Scoring System**: REVERSE (lowest points win)
- **High Confidence Wrong**: 20 points added (devastating)
- **Strategy**: Must be DIFFERENT from the crowd
- **Focus**: VALUE plays, not just favorites
- **Competitive Edge**: Contrarian analysis wins pools
- **Pool Format**: Select 20 picks from {len(actual_games)} available games

## Games to Analyze ({len(pool_games)} games):
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

### 3. INJURY IMPACT ANALYSIS
For each game, assess:
- **Key Player Injuries**: Star players out/questionable
- **Public Overreaction**: Injuries public overreacts to
- **Depth Analysis**: Teams with good depth vs injury-prone
- **Injury Value**: Underrated impact of role player injuries

### 4. SITUATIONAL FACTORS
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

    # ============= LLM INTEGRATION =============

    def generate_llm_research_prompt(self, week: int) -> str:
        """Generate research prompt for LLM analysis."""
        week_games = self.schedule.get(week, {}).get("games", [])

        # Format games list
        games_list = "\n".join(f"- {game}" for game in week_games if game != "BYE")

        prompt = f"""
# Week {week} Football Pool Research Request

Please analyze the following games and provide structured data in JSON format:

## Games to Analyze:
{games_list}

## Required Analysis for Each Game:
1. **Current Spread**: Vegas spread (e.g., -7.5 for home team favored by 7.5)
2. **Public Betting Percentage**: What % of public is betting on each side
3. **Injury Reports**: Key injuries affecting the game
4. **Weather Conditions**: Impact on outdoor games
5. **Situational Factors**:
   - Must-win scenarios
   - Revenge games
   - Lookahead spots
   - Short weeks
   - Extra rest
6. **Confidence Score**: Your confidence in each pick (0-100)

## Required JSON Format:
```json
{{
  "week": {week},
  "games": [
    {{
      "game": "KC@NYG",
      "spread": -7.5,
      "public_percentage": 65,
      "injuries": "KC: Mahomes questionable, NYG: Barkley out",
      "weather": "Clear, 45°F",
      "situational_factors": {{
        "must_win": false,
        "revenge_game": false,
        "lookahead_spot": false,
        "short_week": false,
        "extra_rest": false
      }},
      "confidence_score": 78
    }}
  ]
}}
```

Please provide your analysis in the exact JSON format above.
"""
        return prompt

    def save_llm_data(self, week: int, llm_data: dict[str, Any]) -> bool:
        """Save LLM analysis data to database."""
        try:
            with open(f"llm_data_week_{week}.json", "w") as f:
                json.dump(llm_data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Error saving LLM data: {e}")
            return False

    def load_llm_data(self, week: int) -> Optional[dict[str, Any]]:
        """Load LLM analysis data for a week."""
        try:
            with open(f"llm_data_week_{week}.json") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
        except Exception as e:
            logger.error(f"Error loading LLM data: {e}")
            return None

    def combine_llm_analyses(
        self, analyses: list[tuple[str, dict[str, Any]]], method: str = "average"
    ) -> Optional[dict[str, Any]]:
        """Combine multiple LLM analyses using specified method."""
        try:
            if not analyses:
                return None

            if len(analyses) == 1:
                return analyses[0][1]

            # Extract games from all analyses
            all_games = []
            for name, analysis in analyses:
                games = analysis.get("games", [])
                for game in games:
                    game["source"] = name
                    all_games.append(game)

            # Group games by game identifier
            game_groups = {}
            for game in all_games:
                game_id = game.get("game", "")
                if game_id not in game_groups:
                    game_groups[game_id] = []
                game_groups[game_id].append(game)

            # Combine each game group
            combined_games = []
            for game_id, games in game_groups.items():
                combined_game = self._combine_game_analyses(games, method)
                if combined_game:
                    combined_games.append(combined_game)

            # Create combined analysis
            combined_analysis = {
                "week": analyses[0][1].get("week", 1),
                "games": combined_games,
                "combination_method": method,
                "sources": [name for name, _ in analyses],
                "timestamp": datetime.now().isoformat(),
            }

            return combined_analysis

        except Exception as e:
            logger.error(f"Error combining analyses: {e}")
            return None

    def _combine_game_analyses(
        self, games: list[dict[str, Any]], method: str
    ) -> Optional[dict[str, Any]]:
        """Combine analyses for a single game."""
        try:
            if not games:
                return None

            if len(games) == 1:
                return games[0]

            # Extract common fields
            game_id = games[0].get("game", "")
            week = games[0].get("week", 1)

            # Combine numerical fields
            spreads = [g.get("spread", 0) for g in games if g.get("spread") is not None]
            public_percentages = [
                g.get("public_percentage", 0)
                for g in games
                if g.get("public_percentage") is not None
            ]
            confidence_scores = [
                g.get("confidence_score", 0) for g in games if g.get("confidence_score") is not None
            ]

            # Combine text fields (concatenate unique values)
            injuries = []
            weather = []
            for game in games:
                if game.get("injuries"):
                    injuries.append(game["injuries"])
                if game.get("weather"):
                    weather.append(game["weather"])

            # Combine situational factors (use most conservative values)
            situational_factors = {}
            for game in games:
                factors = game.get("situational_factors", {})
                for key, value in factors.items():
                    if key not in situational_factors:
                        situational_factors[key] = value
                    elif isinstance(value, bool) and value:
                        # If any analysis says True, use True
                        situational_factors[key] = True

            # Calculate combined values based on method
            if method == "average":
                combined_spread = sum(spreads) / len(spreads) if spreads else 0
                combined_public = (
                    sum(public_percentages) / len(public_percentages) if public_percentages else 0
                )
                combined_confidence = (
                    sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
                )
            elif method == "weighted":
                # Weight by confidence scores
                if confidence_scores:
                    weights = [c / sum(confidence_scores) for c in confidence_scores]
                    combined_spread = sum(s * w for s, w in zip(spreads, weights)) if spreads else 0
                    combined_public = (
                        sum(p * w for p, w in zip(public_percentages, weights))
                        if public_percentages
                        else 0
                    )
                    combined_confidence = sum(c * w for c, w in zip(confidence_scores, weights))
                else:
                    combined_spread = sum(spreads) / len(spreads) if spreads else 0
                    combined_public = (
                        sum(public_percentages) / len(public_percentages)
                        if public_percentages
                        else 0
                    )
                    combined_confidence = (
                        sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
                    )
            elif method == "best":
                # Use highest confidence analysis
                best_game = max(games, key=lambda g: g.get("confidence_score", 0))
                combined_spread = best_game.get("spread", 0)
                combined_public = best_game.get("public_percentage", 0)
                combined_confidence = best_game.get("confidence_score", 0)
            else:
                # Default to average
                combined_spread = sum(spreads) / len(spreads) if spreads else 0
                combined_public = (
                    sum(public_percentages) / len(public_percentages) if public_percentages else 0
                )
                combined_confidence = (
                    sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
                )

            # Create combined game
            combined_game = {
                "game": game_id,
                "week": week,
                "spread": round(combined_spread, 1),
                "public_percentage": round(combined_public, 1),
                "confidence_score": round(combined_confidence, 1),
                "injuries": " | ".join(set(injuries)) if injuries else "",
                "weather": " | ".join(set(weather)) if weather else "",
                "situational_factors": situational_factors,
                "sources": [g.get("source", "unknown") for g in games],
                "combination_method": method,
            }

            return combined_game

        except Exception as e:
            logger.error(f"Error combining game analyses: {e}")
            return None

    # ============= DISPLAY AND FORMATTING =============

    def display_formatted_picks(self, picks: list[Pick]) -> None:
        """Display picks in a formatted table."""
        print(f"\n{'='*50}")
        print(f"WEEK {picks[0].week if picks else 'N/A'} OPTIMAL PICKS")
        print(f"{'='*50}")
        print(f"{'Pts':<4} {'Game':<20} {'Pick':<10} {'Conf':<6} {'Strategy'}")
        print(f"{'-'*50}")

        for pick in sorted(picks, key=lambda x: x.confidence_points, reverse=True):
            print(
                f"{pick.confidence_points:<4} {pick.game:<20} {pick.predicted_winner:<10} "
                f"{pick.conf or 0:.1f}%{'':<2} {pick.strategy_tag or 'N/A'}"
            )

    # ============= RESULTS TRACKING =============

    def track_results(self, week: int, results: dict[str, str]) -> bool:
        """Track game results and update pick performance."""
        return self.db.update_pick_results(week, results)

    def save_picks(self, picks: list[Pick]) -> bool:
        """Save picks to database."""
        return self.db.save_picks(picks)

    def get_picks(self, week: Optional[int] = None) -> list[Pick]:
        """Get picks from database."""
        return self.db.get_picks(week)

    def get_all_picks(self) -> list[Pick]:
        """Get all picks from database."""
        return self.db.get_picks()

    # ============= COMPETITOR ANALYSIS =============

    def track_competitor_picks(self, week: int, competitor: str, picks: list[dict]) -> bool:
        """Track competitor picks for analysis."""
        return self.db.save_competitor_picks(week, competitor, picks)

    def analyze_competitor_patterns(self) -> dict[str, Any]:
        """Analyze competitor picking patterns."""
        return self.db.get_competitor_patterns()

    # ============= PERFORMANCE ANALYTICS =============

    def analyze_strategy_performance(self) -> dict[str, Any]:
        """Analyze performance of different strategies."""
        return self.db.get_performance_stats()

    def get_performance_stats(self) -> dict[str, Any]:
        """Get overall performance statistics."""
        return self.db.get_performance_stats()

    def identify_personal_edges(self) -> dict[str, Any]:
        """Identify personal strengths and weaknesses."""
        stats = self.get_performance_stats()

        # Analyze strategy performance
        strategy_perf = stats.get("strategy_performance", {})

        strengths = []
        weaknesses = []

        for strategy, perf in strategy_perf.items():
            if perf["win_rate"] > 60:
                strengths.append(strategy)
            elif perf["win_rate"] < 40:
                weaknesses.append(strategy)

        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "overall_win_rate": stats.get("win_rate", 0),
        }

    # ============= REPORTING =============

    def generate_weekly_report(self, week: int) -> dict[str, Any]:
        """Generate comprehensive weekly report."""
        picks = self.get_picks(week)

        if not picks:
            return {"error": f"No picks found for Week {week}"}

        # Calculate performance
        correct_picks = sum(1 for pick in picks if pick.hit)
        total_picks = len(picks)
        win_rate = (correct_picks / total_picks * 100) if total_picks else 0

        # Calculate weekly score
        weekly_score = sum(pick.points_earned or 0 for pick in picks)

        report = {
            "week": week,
            "performance": {
                "weekly_score": weekly_score,
                "correct_picks": correct_picks,
                "total_picks": total_picks,
                "win_rate": win_rate,
                "strategy_used": picks[0].strategy_tag if picks else "Unknown",
            },
            "picks": [
                {
                    "game": pick.game,
                    "predicted_winner": pick.predicted_winner,
                    "confidence_points": pick.confidence_points,
                    "hit": pick.hit,
                    "points_earned": pick.points_earned,
                }
                for pick in picks
            ],
            "insights": self._generate_insights(picks, win_rate),
            "recommendations": self._generate_recommendations(win_rate),
        }

        return report

    def _generate_insights(self, picks: list[Pick], win_rate: float) -> list[str]:
        """Generate insights based on performance."""
        insights = []

        if win_rate > 70:
            insights.append("Excellent week! High confidence picks paid off.")
        elif win_rate > 50:
            insights.append("Solid performance. Strategy working well.")
        else:
            insights.append("Tough week. Consider adjusting strategy.")

        # Analyze high-confidence picks
        high_conf_picks = [p for p in picks if p.confidence_points >= 15]
        high_conf_hits = sum(1 for p in high_conf_picks if p.hit)

        if high_conf_picks:
            high_conf_rate = high_conf_hits / len(high_conf_picks) * 100
            if high_conf_rate > 80:
                insights.append("High confidence picks were very reliable.")
            elif high_conf_rate < 50:
                insights.append("High confidence picks underperformed.")

        return insights

    def _generate_recommendations(self, win_rate: float) -> list[str]:
        """Generate recommendations based on performance."""
        recommendations = []

        if win_rate < 40:
            recommendations.append("Consider switching to a more conservative strategy.")
        elif win_rate > 70:
            recommendations.append("Current strategy is working well. Stay the course.")
        else:
            recommendations.append("Monitor performance and adjust as needed.")

        return recommendations

    def project_season_finish(self) -> dict[str, Any]:
        """Project season finish based on current performance."""
        stats = self.get_performance_stats()

        # Simple projection based on current performance
        current_weeks = len(set(pick.week for pick in self.get_all_picks()))
        if current_weeks == 0:
            return {
                "current_rank": 1,
                "total_players": 20,
                "projected_final_rank": 10,
                "win_probability": 50.0,
                "expected_final_score": 200.0,
            }

        avg_weekly_score = stats.get("total_points", 0) / current_weeks
        weeks_remaining = 18 - current_weeks

        projected_final_score = stats.get("total_points", 0) + (avg_weekly_score * weeks_remaining)

        # Simple ranking projection
        if avg_weekly_score > 15:
            projected_rank = 1
            win_prob = 80.0
        elif avg_weekly_score > 12:
            projected_rank = 3
            win_prob = 60.0
        elif avg_weekly_score > 10:
            projected_rank = 8
            win_prob = 30.0
        else:
            projected_rank = 15
            win_prob = 10.0

        return {
            "current_rank": 1,  # Would need actual pool data
            "total_players": 20,
            "projected_final_rank": projected_rank,
            "win_probability": win_prob,
            "expected_final_score": projected_final_score,
        }

    # ============= UTILITY METHODS =============

    def apply_strategy_override(self, picks: list[Pick], strategy: str) -> list[Pick]:
        """Apply strategy override to existing picks."""
        # This would modify picks based on strategy
        # For now, just update strategy tags
        for pick in picks:
            pick.strategy_tag = strategy

        return picks

    def load_week_data(self, path: str) -> dict[str, Any]:
        """Load week data from file."""
        try:
            with open(path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading week data: {e}")
            return {}

    def generate_openrouter_request(
        self, week: int, api_key: Optional[str] = None
    ) -> dict[str, Any]:
        """Generate OpenRouter API request for LLM analysis."""
        # Use enhanced prompt with real odds data
        prompt = self.get_enhanced_llm_prompt(week)

        # Use free models for cost efficiency
        free_models = [
            "moonshotai/kimi-k2:free",  # Best overall performance
            "deepseek/deepseek-chat-v3.1:free",  # Fast and reliable
            "qwen/qwen3-235b-a22b:free",  # Good for analysis tasks
            "openai/gpt-oss-20b:free",  # OpenAI compatible
        ]

        # Select model based on week (for variety) or use default
        model_index = week % len(free_models)
        selected_model = free_models[model_index]

        request_data = {
            "model": selected_model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 4000,
            "temperature": 0.3,
        }

        if api_key:
            request_data["api_key"] = api_key

        return request_data

    def call_openrouter_api(self, week: int) -> Optional[dict[str, Any]]:
        """Call OpenRouter API directly and return parsed response."""
        if not self.openrouter_api_key:
            logger.warning("No OpenRouter API key found.")
            app_logger.log_error(Exception("No OpenRouter API key"), "call_openrouter_api")
            return None

        # Check usage limits
        if not self.usage_tracker.can_make_request("openrouter"):
            warning_level = self.usage_tracker.get_warning_level("openrouter")
            logger.warning(f"OpenRouter API limit reached! Warning level: {warning_level}")
            app_logger.log_error(
                Exception(f"API limit reached: {warning_level}"), "call_openrouter_api"
            )
            return None

        try:
            # Generate request
            request_data = self.generate_openrouter_request(week, self.openrouter_api_key)

            # Log LLM request
            model = request_data.get("model", "unknown")
            prompt = request_data.get("messages", [{}])[0].get("content", "")
            app_logger.log_llm_request(model, prompt, {"week": week})

            # Make API call
            url = f"{self.openrouter_api_base}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
            }

            import time

            start_time = time.time()
            response = requests.post(url, json=request_data, headers=headers, timeout=30)
            response_time = time.time() - start_time

            # Log API call
            app_logger.log_api_call(
                "OpenRouter", "chat/completions", "POST", response.status_code, response_time
            )

            response.raise_for_status()

            result = response.json()

            # Record successful API request
            self.usage_tracker.record_request("openrouter", success=True)

            # Extract content from response
            content = result.get("choices", [{}])[0].get("message", {}).get("content", "")

            # Log LLM response
            tokens_used = result.get("usage", {}).get("total_tokens", 0)
            app_logger.log_llm_response(model, content, tokens_used)

            # Try to parse JSON from response
            try:
                # Look for JSON in the response
                import re

                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    parsed_data = json.loads(json_str)
                    app_logger.llm_logger.info(f"Successfully parsed JSON response from {model}")
                    return parsed_data
                else:
                    logger.warning("No JSON found in OpenRouter response")
                    app_logger.llm_logger.warning("No JSON found in OpenRouter response")
                    return None
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON from OpenRouter response: {e}")
                app_logger.log_error(e, f"JSON parsing error for {model}")
                return None

        except Exception as e:
            logger.error(f"Error calling OpenRouter API: {e}")
            # Record failed request
            self.usage_tracker.record_request("openrouter", success=False)
            return None

    def get_ai_analysis(self, week: int) -> Optional[dict[str, Any]]:
        """Get AI analysis using OpenRouter API."""
        logger.info(f"Getting AI analysis for Week {week}")

        # Try OpenRouter API first
        if self.openrouter_api_key:
            analysis = self.call_openrouter_api(week)
            if analysis:
                logger.info("Successfully got analysis from OpenRouter")
                return analysis

        # Fallback to manual prompt
        logger.info("Falling back to manual prompt generation")
        return None

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
