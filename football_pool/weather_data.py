"""
Weather Data Provider for Football Pool Analysis.

This module provides weather data integration for outdoor games,
including wind speed, temperature, and precipitation analysis.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import requests

logger = logging.getLogger(__name__)


class WeatherDataProvider:
    """Provides weather data for NFL games and betting analysis."""

    def __init__(self):
        """Initialize weather data provider."""
        self.api_key = os.getenv("OPENWEATHER_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache_dir = Path("data/cache/weather")
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_game_weather(self, game: str, date: str) -> Dict[str, Any]:
        """Get weather data for a specific game."""
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY is required for weather data. No fallback data available.")

        try:
            # Extract team names and location from game string
            away_team, home_team = game.split("@")

            # Get stadium location (simplified mapping)
            stadium_location = self._get_stadium_location(home_team)

            # Check cache first
            cache_file = self.cache_dir / f"{game}_{date}.json"
            if cache_file.exists():
                with open(cache_file) as f:
                    cached_data = json.load(f)
                    if self._is_cache_valid(cached_data):
                        logger.info(f"Using cached weather data for {game}")
                        return cached_data["weather_data"]

            # Fetch fresh weather data
            weather_data = self._fetch_weather_data(stadium_location, date)

            # Cache the data
            cache_data = {
                "timestamp": datetime.now().isoformat(),
                "weather_data": weather_data
            }
            with open(cache_file, "w") as f:
                json.dump(cache_data, f, indent=2)

            return weather_data

        except Exception as e:
            logger.error(f"Error getting weather data for {game}: {e}")
            raise RuntimeError(f"Failed to fetch weather data for {game}: {e}")

    def _get_stadium_location(self, team: str) -> Dict[str, str]:
        """Get stadium location for a team."""
        stadium_locations = {
            "KC": {"city": "Kansas City", "state": "MO", "lat": "39.0997", "lon": "-94.5786"},
            "NYG": {"city": "East Rutherford", "state": "NJ", "lat": "40.8136", "lon": "-74.0744"},
            "BAL": {"city": "Baltimore", "state": "MD", "lat": "39.2780", "lon": "-76.6227"},
            "DET": {"city": "Detroit", "state": "MI", "lat": "42.3400", "lon": "-83.0456"},
            "LAR": {"city": "Los Angeles", "state": "CA", "lat": "34.0522", "lon": "-118.2437"},
            "PHIL": {"city": "Philadelphia", "state": "PA", "lat": "39.9526", "lon": "-75.1652"},
            "DAL": {"city": "Arlington", "state": "TX", "lat": "32.7473", "lon": "-97.0825"},
            "CHI": {"city": "Chicago", "state": "IL", "lat": "41.8781", "lon": "-87.6298"},
            "SF": {"city": "San Francisco", "state": "CA", "lat": "37.7749", "lon": "-122.4194"},
            "ARIZ": {"city": "Glendale", "state": "AZ", "lat": "33.5387", "lon": "-112.1860"},
            "GB": {"city": "Green Bay", "state": "WI", "lat": "44.5192", "lon": "-88.0198"},
            "CLEV": {"city": "Cleveland", "state": "OH", "lat": "41.4993", "lon": "-81.6944"},
            "MIA": {"city": "Miami", "state": "FL", "lat": "25.7617", "lon": "-80.1918"},
            "BUFF": {"city": "Buffalo", "state": "NY", "lat": "42.8864", "lon": "-78.8784"},
            "HOU": {"city": "Houston", "state": "TX", "lat": "29.7604", "lon": "-95.3698"},
            "JAC": {"city": "Jacksonville", "state": "FL", "lat": "30.3322", "lon": "-81.6557"},
            "CINC": {"city": "Cincinnati", "state": "OH", "lat": "39.1031", "lon": "-84.5120"},
            "MINN": {"city": "Minneapolis", "state": "MN", "lat": "44.9778", "lon": "-93.2650"},
            "PITT": {"city": "Pittsburgh", "state": "PA", "lat": "40.4406", "lon": "-79.9959"},
            "NE": {"city": "Foxborough", "state": "MA", "lat": "42.0934", "lon": "-71.2640"},
            "ATL": {"city": "Atlanta", "state": "GA", "lat": "33.7490", "lon": "-84.3880"},
            "CAR": {"city": "Charlotte", "state": "NC", "lat": "35.2271", "lon": "-80.8431"},
            "DEN": {"city": "Denver", "state": "CO", "lat": "39.7392", "lon": "-104.9903"},
            "LAC": {"city": "Los Angeles", "state": "CA", "lat": "34.0522", "lon": "-118.2437"},
            "LV": {"city": "Las Vegas", "state": "NV", "lat": "36.1699", "lon": "-115.1398"},
            "WASH": {"city": "Landover", "state": "MD", "lat": "38.9072", "lon": "-76.8650"},
            "NO": {"city": "New Orleans", "state": "LA", "lat": "29.9511", "lon": "-90.0715"},
            "SEA": {"city": "Seattle", "state": "WA", "lat": "47.6062", "lon": "-122.3321"},
            "TB": {"city": "Tampa", "state": "FL", "lat": "27.9506", "lon": "-82.4572"},
            "NYJ": {"city": "East Rutherford", "state": "NJ", "lat": "40.8136", "lon": "-74.0744"},
        }

        return stadium_locations.get(team, {"city": "Unknown", "state": "Unknown", "lat": "0", "lon": "0"})

    def _fetch_weather_data(self, location: Dict[str, str], date: str) -> Dict[str, Any]:
        """Fetch weather data from OpenWeatherMap API."""
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY is required for weather data. No fallback data available.")

        try:
            # Convert date to timestamp for API call
            game_date = datetime.strptime(date, "%Y-%m-%d")
            timestamp = int(game_date.timestamp())

            # API call for weather forecast
            url = f"{self.base_url}/forecast"
            params = {
                "lat": location["lat"],
                "lon": location["lon"],
                "appid": self.api_key,
                "units": "imperial"
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            # Find the closest forecast to game time (assuming 1 PM ET)
            game_hour = 13  # 1 PM ET
            closest_forecast = None
            min_time_diff = float('inf')

            for forecast in data.get("list", []):
                forecast_time = datetime.fromtimestamp(forecast["dt"])
                time_diff = abs(forecast_time.hour - game_hour)

                if time_diff < min_time_diff:
                    min_time_diff = time_diff
                    closest_forecast = forecast

            if closest_forecast:
                weather = closest_forecast["weather"][0]
                main = closest_forecast["main"]
                wind = closest_forecast.get("wind", {})

                return {
                    "temperature": main.get("temp", 70),
                    "humidity": main.get("humidity", 50),
                    "wind_speed": wind.get("speed", 0),
                    "wind_direction": wind.get("deg", 0),
                    "precipitation": weather.get("main", "Clear"),
                    "description": weather.get("description", "clear sky"),
                    "visibility": closest_forecast.get("visibility", 10000),
                    "pressure": main.get("pressure", 1013),
                    "weather_impact": self._analyze_weather_impact(
                        main.get("temp", 70),
                        wind.get("speed", 0),
                        weather.get("main", "Clear")
                    )
                }
            else:
                raise RuntimeError("No weather forecast data available for the specified date")

        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            raise RuntimeError(f"Failed to fetch weather data: {e}")

    def _analyze_weather_impact(self, temp: float, wind_speed: float, condition: str) -> Dict[str, Any]:
        """Analyze weather impact on game strategy."""
        impact = {
            "passing_advantage": 0,
            "running_advantage": 0,
            "kicking_advantage": 0,
            "overall_impact": "neutral"
        }

        # Temperature impact
        if temp < 32:  # Freezing
            impact["passing_advantage"] -= 2
            impact["running_advantage"] += 1
            impact["kicking_advantage"] -= 1
        elif temp > 85:  # Hot
            impact["passing_advantage"] -= 1
            impact["running_advantage"] -= 1

        # Wind impact
        if wind_speed > 15:  # Strong wind
            impact["passing_advantage"] -= 3
            impact["kicking_advantage"] -= 2
        elif wind_speed > 10:  # Moderate wind
            impact["passing_advantage"] -= 1
            impact["kicking_advantage"] -= 1

        # Precipitation impact
        if condition in ["Rain", "Drizzle", "Thunderstorm"]:
            impact["passing_advantage"] -= 2
            impact["running_advantage"] += 1
            impact["kicking_advantage"] -= 1

        # Determine overall impact
        total_impact = impact["passing_advantage"] + impact["running_advantage"] + impact["kicking_advantage"]

        if total_impact > 2:
            impact["overall_impact"] = "favorable"
        elif total_impact < -2:
            impact["overall_impact"] = "unfavorable"
        else:
            impact["overall_impact"] = "neutral"

        return impact

    def _is_cache_valid(self, cached_data: Dict[str, Any]) -> bool:
        """Check if cached weather data is still valid (within 6 hours)."""
        try:
            timestamp = datetime.fromisoformat(cached_data["timestamp"])
            age_hours = (datetime.now() - timestamp).total_seconds() / 3600
            return age_hours < 6
        except:
            return False


    def get_weather_summary(self, games: list[str], date: str) -> Dict[str, Any]:
        """Get weather summary for multiple games."""
        weather_summary = {
            "outdoor_games": [],
            "weather_advantages": [],
            "weather_plays": [],
            "game_weather": {}
        }

        for game in games:
            weather_data = self.get_game_weather(game, date)
            weather_summary["game_weather"][game] = weather_data

            # Identify outdoor games (simplified - all NFL games are outdoor)
            weather_summary["outdoor_games"].append(game)

            # Identify weather advantages
            if weather_data["weather_impact"]["overall_impact"] == "favorable":
                weather_summary["weather_advantages"].append(game.split("@")[1])  # Home team
                weather_summary["weather_plays"].append(game)

        return weather_summary
