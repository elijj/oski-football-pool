"""
Tests for data models.
"""

from datetime import datetime

import pytest

from football_pool.models import (
    CompetitorPick,
    GameResult,
    LLMData,
    Pick,
    PoolPosition,
    StrategyPerformance,
)


class TestPick:
    """Test Pick model."""

    def test_pick_creation(self):
        """Test basic pick creation."""
        pick = Pick(game="KC@NYG", predicted_winner="KC", confidence_points=20)

        assert pick.game == "KC@NYG"
        assert pick.predicted_winner == "KC"
        assert pick.confidence_points == 20
        assert pick.conf is None
        assert pick.strategy_tag is None

    def test_pick_validation(self):
        """Test pick validation."""
        # Valid pick
        pick = Pick(game="KC@NYG", predicted_winner="KC", confidence_points=15, conf=75.5)
        assert pick.confidence_points == 15
        assert pick.conf == 75.5

        # Invalid confidence points
        with pytest.raises(ValueError, match="Confidence points must be between 1 and 20"):
            Pick(game="KC@NYG", predicted_winner="KC", confidence_points=25)

        with pytest.raises(ValueError, match="Confidence points must be between 1 and 20"):
            Pick(game="KC@NYG", predicted_winner="KC", confidence_points=0)

        # Invalid confidence percentage
        with pytest.raises(ValueError, match="Confidence percentage must be between 0 and 100"):
            Pick(game="KC@NYG", predicted_winner="KC", confidence_points=15, conf=150.0)


class TestGameResult:
    """Test GameResult model."""

    def test_game_result_creation(self):
        """Test basic game result creation."""
        result = GameResult(week=3, game="KC@NYG", winner="KC")

        assert result.week == 3
        assert result.game == "KC@NYG"
        assert result.winner == "KC"
        assert result.score_home is None
        assert result.score_away is None
        assert isinstance(result.timestamp, datetime)

    def test_game_result_with_scores(self):
        """Test game result with scores."""
        result = GameResult(week=3, game="KC@NYG", winner="KC", score_home=24, score_away=17)

        assert result.score_home == 24
        assert result.score_away == 17


class TestCompetitorPick:
    """Test CompetitorPick model."""

    def test_competitor_pick_creation(self):
        """Test basic competitor pick creation."""
        pick = CompetitorPick(
            week=3, competitor_name="Uncle Bob", game="KC@NYG", pick="KC", points=20
        )

        assert pick.week == 3
        assert pick.competitor_name == "Uncle Bob"
        assert pick.game == "KC@NYG"
        assert pick.pick == "KC"
        assert pick.points == 20
        assert isinstance(pick.timestamp, datetime)


class TestStrategyPerformance:
    """Test StrategyPerformance model."""

    def test_strategy_performance_creation(self):
        """Test basic strategy performance creation."""
        perf = StrategyPerformance(
            strategy_name="balanced",
            week=3,
            variance_level="medium",
            pool_position_rank=1,
            pool_position_total=20,
            weekly_score=15,
            cumulative_score=45,
            success_rate=75.0,
        )

        assert perf.strategy_name == "balanced"
        assert perf.week == 3
        assert perf.variance_level == "medium"
        assert perf.pool_position_rank == 1
        assert perf.pool_position_total == 20
        assert perf.weekly_score == 15
        assert perf.cumulative_score == 45
        assert perf.success_rate == 75.0
        assert isinstance(perf.timestamp, datetime)


class TestLLMData:
    """Test LLMData model."""

    def test_llm_data_creation(self):
        """Test basic LLM data creation."""
        data = LLMData(
            week=3,
            games=[{"game": "KC@NYG", "spread": -7.5}],
            spreads={"KC@NYG": -7.5},
            public_percentages={"KC@NYG": 65.0},
            injuries={"KC@NYG": "No key injuries"},
            weather={"KC@NYG": "Clear, 45°F"},
            situational_factors={"KC@NYG": {"must_win": False}},
            confidence_scores={"KC@NYG": 78.0},
        )

        assert data.week == 3
        assert len(data.games) == 1
        assert data.spreads["KC@NYG"] == -7.5
        assert data.public_percentages["KC@NYG"] == 65.0
        assert isinstance(data.timestamp, datetime)

    def test_llm_data_from_dict(self):
        """Test creating LLMData from dictionary."""
        data_dict = {
            "week": 3,
            "games": [{"game": "KC@NYG", "spread": -7.5}],
            "spreads": {"KC@NYG": -7.5},
            "public_percentages": {"KC@NYG": 65.0},
            "injuries": {"KC@NYG": "No key injuries"},
            "weather": {"KC@NYG": "Clear, 45°F"},
            "situational_factors": {"KC@NYG": {"must_win": False}},
            "confidence_scores": {"KC@NYG": 78.0},
        }

        data = LLMData.from_dict(data_dict)

        assert data.week == 3
        assert len(data.games) == 1
        assert data.spreads["KC@NYG"] == -7.5


class TestPoolPosition:
    """Test PoolPosition model."""

    def test_pool_position_creation(self):
        """Test basic pool position creation."""
        position = PoolPosition(
            rank=1,
            total_players=20,
            points_behind_leader=0,
            points_ahead_of_last=50,
            weekly_scores=[15, 18, 12],
            cumulative_score=45,
            weeks_remaining=16,
        )

        assert position.rank == 1
        assert position.total_players == 20
        assert position.points_behind_leader == 0
        assert position.points_ahead_of_last == 50
        assert len(position.weekly_scores) == 3
        assert position.cumulative_score == 45
        assert position.weeks_remaining == 16

    def test_pool_position_properties(self):
        """Test pool position properties."""
        # Leading position
        leading = PoolPosition(
            rank=1,
            total_players=20,
            points_behind_leader=0,
            points_ahead_of_last=50,
            weekly_scores=[],
            cumulative_score=0,
            weeks_remaining=16,
        )
        assert leading.is_leading is True
        assert leading.is_trailing is False
        assert leading.needs_variance is False

        # Trailing position
        trailing = PoolPosition(
            rank=15,
            total_players=20,
            points_behind_leader=120,
            points_ahead_of_last=0,
            weekly_scores=[],
            cumulative_score=0,
            weeks_remaining=16,
        )
        assert trailing.is_leading is False
        assert trailing.is_trailing is True
        assert trailing.needs_variance is True
