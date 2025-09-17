"""
Web Search Integration for Football Pool Analysis

This module provides web search capabilities to enhance LLM prompts with
real-time information about games, teams, and betting trends.
"""

import json
import logging
from typing import Any, Optional

import requests

logger = logging.getLogger(__name__)


class WebSearchIntegration:
    """
    Web search integration for enhanced football analysis.

    Provides real-time web search capabilities to gather:
    - Team news and injury reports
    - Weather conditions
    - Betting trends and public sentiment
    - Expert analysis and predictions
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize web search integration."""
        if not api_key:
            raise ValueError("SMITHERY_API_KEY is required for web search. No fallback data available.")
        self.api_key = api_key
        self.profile = "victorious-barracuda-F6fVdr"
        self.base_url = "https://server.smithery.ai/exa/mcp"
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json", "x-api-key": self.api_key})

        # Cost tracking
        self.cost_tracker = {"searches_performed": 0, "total_cost": 0.0}

    def search_team_news(self, team: str, week: int) -> list[dict[str, Any]]:
        """
        Search for team-specific news and updates.

        Args:
            team: Team abbreviation (e.g., 'KC', 'BALT')
            week: Week number

        Returns:
            List of search results with news and analysis
        """
        try:
            query = f"{team} NFL week {week} news injuries weather analysis"
            return self._perform_search(query, num_results=3)
        except Exception as e:
            logger.warning(f"Team news search failed for {team}: {e}")
            return []

    def search_game_analysis(
        self, away_team: str, home_team: str, week: int
    ) -> list[dict[str, Any]]:
        """
        Search for specific game analysis and predictions.

        Args:
            away_team: Away team abbreviation
            home_team: Home team abbreviation
            week: Week number

        Returns:
            List of search results with game analysis
        """
        try:
            query = f"{away_team} vs {home_team} NFL week {week} prediction analysis spread betting"
            return self._perform_search(query, num_results=3)
        except Exception as e:
            logger.warning(f"Game analysis search failed for {away_team}@{home_team}: {e}")
            return []

    def search_betting_trends(self, week: int) -> list[dict[str, Any]]:
        """
        Search for betting trends and public sentiment.

        Args:
            week: Week number

        Returns:
            List of search results with betting trends
        """
        try:
            query = f"NFL week {week} betting trends public sentiment sharp money"
            return self._perform_search(query, num_results=2)
        except Exception as e:
            logger.warning(f"Betting trends search failed for week {week}: {e}")
            return []

    def _perform_search(self, query: str, num_results: int = 3) -> list[dict[str, Any]]:
        """
        Perform web search using Exa API.

        Args:
            query: Search query string
            num_results: Number of results to return

        Returns:
            List of search results
        """
        # Use MCP endpoint for web search - no fallbacks
        url = f"{self.base_url}?api_key={self.api_key}&profile={self.profile}"

        # MCP protocol uses different request format
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "web_search_exa",
                "arguments": {"query": query, "numResults": num_results},
            },
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse Server-Sent Events (SSE) format
        results = self._parse_sse_response(response.text)
        logger.info(f"MCP Response: {len(results)} results found")

        # Update cost tracking
        self.cost_tracker["searches_performed"] += 1
        self.cost_tracker["total_cost"] += 0.005  # $0.005 per search

        logger.info(f"🔍 Found {len(results)} web search results for: {query}")
        return results

    def _parse_sse_response(self, sse_text: str) -> list[dict[str, Any]]:
        """Parse Server-Sent Events response from MCP endpoint."""
        try:
            # Split by lines and find data lines
            lines = sse_text.strip().split("\n")
            data_lines = []

            for line in lines:
                if line.startswith("data: "):
                    data_lines.append(line[6:])  # Remove 'data: ' prefix

            if not data_lines:
                return []

            # Parse the JSON data
            for data_line in data_lines:
                try:
                    data = json.loads(data_line)
                    if "result" in data and "content" in data["result"]:
                        # Extract results from the content
                        content = data["result"]["content"]
                        if isinstance(content, list) and len(content) > 0:
                            # The content contains the search results
                            result_data = json.loads(content[0]["text"])
                            if "results" in result_data:
                                return result_data["results"]
                except json.JSONDecodeError:
                    continue

            return []

        except Exception as e:
            logger.warning(f"SSE parsing failed: {e}")
            return []

    def format_search_context(self, results: list[dict[str, Any]], max_results: int = 3) -> str:
        """
        Format search results for LLM context.

        Args:
            results: List of search results
            max_results: Maximum number of results to include

        Returns:
            Formatted string for LLM context
        """
        if not results:
            return ""

        context = "\n\n## Recent Web Search Context:\n"
        for i, result in enumerate(results[:max_results], 1):
            title = result.get("title", "No title")
            text = (
                result.get("text", "No content")[:200] + "..."
                if len(result.get("text", "")) > 200
                else result.get("text", "No content")
            )
            context += f"{i}. **{title}**\n"
            context += f"   {text}\n\n"

        return context

    def get_cost_summary(self) -> dict[str, Any]:
        """Get cost tracking summary."""
        return {
            "searches_performed": self.cost_tracker["searches_performed"],
            "total_cost": self.cost_tracker["total_cost"],
            "average_cost_per_search": (
                self.cost_tracker["total_cost"] / max(1, self.cost_tracker["searches_performed"])
            ),
        }


class FootballWebSearch:
    """
    Specialized web search for football pool analysis.

    Provides targeted search capabilities for:
    - Team-specific news and injuries
    - Game analysis and predictions
    - Betting trends and public sentiment
    - Weather and situational factors
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize football-specific web search."""
        # Use demo credentials if no API key provided
        self.web_search = WebSearchIntegration(api_key)
        self.team_mapping = {
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

    def get_enhanced_context(self, week: int, games: list[str]) -> str:
        """
        Get enhanced web search context for a week's games.

        Args:
            week: Week number
            games: List of games in format 'AWAY@HOME'

        Returns:
            Formatted web search context
        """
        try:
            all_results = []

            # Search for betting trends
            trends = self.web_search.search_betting_trends(week)
            if trends:
                all_results.extend(trends)

            # Search for key games
            for game in games[:3]:  # Limit to top 3 games
                if "@" in game and game != "BYE":
                    away, home = game.split("@")
                    game_results = self.web_search.search_game_analysis(away, home, week)
                    if game_results:
                        all_results.extend(game_results)

            # Format context
            if all_results:
                return self.web_search.format_search_context(all_results, max_results=5)
            else:
                return ""

        except Exception as e:
            logger.warning(f"Enhanced context generation failed: {e}")
            return ""

    def search_team_news(self, team: str, week: int) -> list[dict[str, Any]]:
        """Search for team-specific news."""
        return self.web_search.search_team_news(team, week)

    def search_game_analysis(
        self, away_team: str, home_team: str, week: int
    ) -> list[dict[str, Any]]:
        """Search for game-specific analysis."""
        return self.web_search.search_game_analysis(away_team, home_team, week)

    def search_web(self, query: str, num_results: int = 3) -> list[dict[str, Any]]:
        """Perform web search using the underlying WebSearchIntegration."""
        return self.web_search._perform_search(query, num_results)

    def get_enhanced_context_by_date(self, date: str) -> str:
        """Get enhanced context using real web search for a specific date."""
        try:
            # Create search query for the date
            query = f"{date} NFL CFB football games analysis betting odds injuries weather"

            # Perform web search
            results = self.search_web(query, num_results=3)

            if results:
                context = "\n\n## Web Search Context:\n"
                for i, result in enumerate(results[:3], 1):
                    context += f"{i}. **{result.get('title', 'No title')}**\n"
                    context += f"   {result.get('url', 'No URL')}\n"
                    context += f"   {result.get('content', 'No content')[:200]}...\n\n"

                return context
            else:
                return ""

        except Exception as e:
            logger.error(f"Error getting enhanced context for {date}: {e}")
            return ""
