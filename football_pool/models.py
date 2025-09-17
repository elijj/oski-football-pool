"""
Data models for the Football Pool Domination System.

This module defines the core data structures used throughout the system.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional


@dataclass
class Pick:
    """Represents a single game pick with confidence points."""

    game: str
    predicted_winner: str
    confidence_points: int
    conf: Optional[float] = None
    strategy_tag: Optional[str] = None
    week: Optional[int] = None
    spread: Optional[float] = None
    public_pct: Optional[float] = None
    actual_winner: Optional[str] = None
    hit: Optional[bool] = None
    points_earned: Optional[int] = None

    def __post_init__(self):
        """Validate the pick data after initialization."""
        if self.confidence_points < 1 or self.confidence_points > 20:
            raise ValueError("Confidence points must be between 1 and 20")

        if self.conf and (self.conf < 0 or self.conf > 100):
            raise ValueError("Confidence percentage must be between 0 and 100")


@dataclass
class GameResult:
    """Represents the result of a completed game."""

    week: int
    game: str
    winner: str
    score_home: Optional[int] = None
    score_away: Optional[int] = None
    spread_result: Optional[float] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class CompetitorPick:
    """Represents a competitor's pick for a game."""

    week: int
    competitor_name: str
    game: str
    pick: str
    points: int
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class StrategyPerformance:
    """Tracks performance of different strategies."""

    strategy_name: str
    week: int
    variance_level: str
    pool_position_rank: int
    pool_position_total: int
    weekly_score: int
    cumulative_score: int
    success_rate: float
    notes: Optional[str] = None
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class LLMData:
    """Structured data from LLM analysis."""

    week: int
    games: list[dict[str, Any]]
    spreads: dict[str, float]
    public_percentages: dict[str, float]
    injuries: dict[str, str]
    weather: dict[str, str]
    situational_factors: dict[str, dict[str, Any]]
    confidence_scores: dict[str, float]
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "LLMData":
        """Create LLMData from dictionary."""
        return cls(
            week=data.get("week", 0),
            games=data.get("games", []),
            spreads=data.get("spreads", {}),
            public_percentages=data.get("public_percentages", {}),
            injuries=data.get("injuries", {}),
            weather=data.get("weather", {}),
            situational_factors=data.get("situational_factors", {}),
            confidence_scores=data.get("confidence_scores", {}),
            timestamp=datetime.now(),
        )


@dataclass
class PoolPosition:
    """Represents current position in the pool."""

    rank: int
    total_players: int
    points_behind_leader: int
    points_ahead_of_last: int
    weekly_scores: list[int]
    cumulative_score: int
    weeks_remaining: int

    @property
    def is_leading(self) -> bool:
        """Check if currently in the lead."""
        return self.rank == 1

    @property
    def is_trailing(self) -> bool:
        """Check if trailing by significant margin."""
        return self.points_behind_leader > 50

    @property
    def needs_variance(self) -> bool:
        """Check if needs high variance strategy."""
        return self.points_behind_leader > 100


@dataclass
class WeeklyReport:
    """Comprehensive weekly report."""

    week: int
    picks: list[Pick]
    strategy_used: str
    variance_level: str
    expected_score: float
    risk_assessment: str
    competitor_analysis: dict[str, Any]
    key_insights: list[str]
    recommendations: list[str]
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class SeasonProjection:
    """Projected season finish."""

    current_rank: int
    total_players: int
    projected_final_rank: int
    win_probability: float
    expected_final_score: float
    scenarios: dict[str, float]  # 'win', 'top3', 'top10', etc.
    key_weeks_remaining: list[int]
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
