"""
Tests for core system functionality.
"""

import os
import tempfile

import pytest

from football_pool.core import PoolDominationSystem
from football_pool.models import Pick, PoolPosition


class TestPoolDominationSystem:
    """Test PoolDominationSystem class."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        yield db_path

        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)

    def test_system_initialization(self, temp_db):
        """Test system initialization."""
        system = PoolDominationSystem(db_path=temp_db)

        assert system.current_week == 1
        assert isinstance(system.pool_position, PoolPosition)
        assert system.db is not None
        assert len(system.team_power_ratings) > 0
        assert len(system.schedule) > 0

    def test_determine_strategy(self, temp_db):
        """Test strategy determination based on pool position."""
        system = PoolDominationSystem(db_path=temp_db)

        # Test protective strategy (leading by 30+)
        system.pool_position.points_behind_leader = -40
        strategy = system._determine_strategy()
        assert strategy == "protective"

        # Test balanced strategy (within 30 points)
        system.pool_position.points_behind_leader = -10
        strategy = system._determine_strategy()
        assert strategy == "balanced"

        # Test high variance strategy (behind by 50-150)
        system.pool_position.points_behind_leader = 75
        strategy = system._determine_strategy()
        assert strategy == "high_variance"

        # Test maximum variance strategy (behind by 150+)
        system.pool_position.points_behind_leader = 200
        strategy = system._determine_strategy()
        assert strategy == "maximum_variance"

    def test_generate_protective_picks(self, temp_db):
        """Test generating protective picks."""
        system = PoolDominationSystem(db_path=temp_db)

        games = ["KC@NYG", "DAL@CHI", "GB@MINN"]
        picks = system._generate_protective_picks(3, games, None)

        assert len(picks) <= 20
        assert all(isinstance(pick, Pick) for pick in picks)
        assert all(pick.week is None for pick in picks)  # Week not set yet

        # Check that picks have reasonable confidence
        for pick in picks:
            assert pick.conf is not None
            assert 0 <= pick.conf <= 100

    def test_generate_balanced_picks(self, temp_db):
        """Test generating balanced picks."""
        system = PoolDominationSystem(db_path=temp_db)

        games = ["KC@NYG", "DAL@CHI", "GB@MINN"]
        picks = system._generate_balanced_picks(3, games, None)

        assert len(picks) <= 20
        assert all(isinstance(pick, Pick) for pick in picks)

        # Check that picks have reasonable confidence
        for pick in picks:
            assert pick.conf is not None
            assert 0 <= pick.conf <= 100

    def test_generate_high_variance_picks(self, temp_db):
        """Test generating high variance picks."""
        system = PoolDominationSystem(db_path=temp_db)

        games = ["KC@NYG", "DAL@CHI", "GB@MINN"]
        picks = system._generate_high_variance_picks(3, games, None)

        assert len(picks) <= 20
        assert all(isinstance(pick, Pick) for pick in picks)

        # Check that picks have reasonable confidence
        for pick in picks:
            assert pick.conf is not None
            assert 0 <= pick.conf <= 100

    def test_generate_maximum_variance_picks(self, temp_db):
        """Test generating maximum variance picks."""
        system = PoolDominationSystem(db_path=temp_db)

        games = ["KC@NYG", "DAL@CHI", "GB@MINN"]
        picks = system._generate_maximum_variance_picks(3, games, None)

        assert len(picks) <= 20
        assert all(isinstance(pick, Pick) for pick in picks)

        # Check that picks have reasonable confidence
        for pick in picks:
            assert pick.conf is not None
            assert 0 <= pick.conf <= 100

    def test_apply_fibonacci_assignment(self, temp_db):
        """Test Fibonacci point assignment."""
        system = PoolDominationSystem(db_path=temp_db)

        picks = [
            Pick(game="KC@NYG", predicted_winner="KC", confidence_points=0, conf=90),
            Pick(game="DAL@CHI", predicted_winner="DAL", confidence_points=0, conf=80),
            Pick(game="GB@MINN", predicted_winner="GB", confidence_points=0, conf=70),
            Pick(game="BALT@HOU", predicted_winner="BALT", confidence_points=0, conf=60),
            Pick(game="SF@SEA", predicted_winner="SF", confidence_points=0, conf=50),
        ]

        assigned_picks = system._apply_fibonacci_assignment(picks)

        # Check that points were assigned
        assert all(pick.confidence_points > 0 for pick in assigned_picks)

        # Check that points are in descending order
        points = [pick.confidence_points for pick in assigned_picks]
        assert points == sorted(points, reverse=True)

        # Check that we have the right number of points
        assert len(assigned_picks) <= 20
        assert all(1 <= pick.confidence_points <= 20 for pick in assigned_picks)

    def test_generate_optimal_picks(self, temp_db):
        """Test generating optimal picks."""
        system = PoolDominationSystem(db_path=temp_db)

        # Test with week 3 (has games)
        picks = system.generate_optimal_picks(week=3)

        assert len(picks) <= 20
        assert all(isinstance(pick, Pick) for pick in picks)
        assert all(pick.week == 3 for pick in picks)
        assert all(pick.confidence_points > 0 for pick in picks)
        assert all(pick.strategy_tag is not None for pick in picks)

    def test_generate_llm_research_prompt(self, temp_db):
        """Test generating LLM research prompt."""
        system = PoolDominationSystem(db_path=temp_db)

        prompt = system.generate_llm_research_prompt(week=3)

        assert isinstance(prompt, str)
        assert "Week 3" in prompt
        assert "JSON" in prompt
        assert "spread" in prompt.lower()
        assert "confidence" in prompt.lower()

    def test_save_and_load_llm_data(self, temp_db):
        """Test saving and loading LLM data."""
        system = PoolDominationSystem(db_path=temp_db)

        llm_data = {
            "week": 3,
            "games": [{"game": "KC@NYG", "spread": -7.5}],
            "spreads": {"KC@NYG": -7.5},
            "public_percentages": {"KC@NYG": 65.0},
            "injuries": {"KC@NYG": "No key injuries"},
            "weather": {"KC@NYG": "Clear, 45°F"},
            "situational_factors": {"KC@NYG": {"must_win": False}},
            "confidence_scores": {"KC@NYG": 78.0},
        }

        # Save data
        result = system.save_llm_data(3, llm_data)
        assert result is True

        # Load data
        loaded_data = system.load_llm_data(3)
        assert loaded_data is not None
        assert loaded_data["week"] == 3
        assert "KC@NYG" in loaded_data["spreads"]

    def test_track_results(self, temp_db):
        """Test tracking results."""
        system = PoolDominationSystem(db_path=temp_db)

        # First save some picks
        picks = [
            Pick(game="KC@NYG", predicted_winner="KC", confidence_points=20, week=3),
            Pick(game="DAL@CHI", predicted_winner="DAL", confidence_points=19, week=3),
        ]
        system.save_picks(picks)

        # Track results
        results = {"KC@NYG": "KC", "DAL@CHI": "CHI"}

        result = system.track_results(3, results)
        assert result is True

        # Check that picks were updated
        updated_picks = system.get_picks(week=3)
        assert len(updated_picks) == 2

        # Check first pick (correct)
        first_pick = next(p for p in updated_picks if p.game == "KC@NYG")
        assert first_pick.actual_winner == "KC"
        assert first_pick.hit is True
        assert first_pick.points_earned == 20

        # Check second pick (incorrect)
        second_pick = next(p for p in updated_picks if p.game == "DAL@CHI")
        assert second_pick.actual_winner == "CHI"
        assert second_pick.hit is False
        assert second_pick.points_earned == 0

    def test_get_performance_stats(self, temp_db):
        """Test getting performance statistics."""
        system = PoolDominationSystem(db_path=temp_db)

        # Save some picks with results
        picks = [
            Pick(
                game="KC@NYG",
                predicted_winner="KC",
                confidence_points=20,
                week=3,
                actual_winner="KC",
                hit=True,
                points_earned=20,
                strategy_tag="balanced",
            ),
            Pick(
                game="DAL@CHI",
                predicted_winner="DAL",
                confidence_points=19,
                week=3,
                actual_winner="CHI",
                hit=False,
                points_earned=0,
                strategy_tag="balanced",
            ),
        ]

        # Manually save picks with results
        system.save_picks(picks)

        # Get performance stats
        stats = system.get_performance_stats()

        assert "total_picks" in stats
        assert "correct_picks" in stats
        assert "total_points" in stats
        assert "win_rate" in stats
        assert "strategy_performance" in stats

    def test_identify_personal_edges(self, temp_db):
        """Test identifying personal edges."""
        system = PoolDominationSystem(db_path=temp_db)

        edges = system.identify_personal_edges()

        assert "strengths" in edges
        assert "weaknesses" in edges
        assert "overall_win_rate" in edges
        assert isinstance(edges["strengths"], list)
        assert isinstance(edges["weaknesses"], list)

    def test_generate_weekly_report(self, temp_db):
        """Test generating weekly report."""
        system = PoolDominationSystem(db_path=temp_db)

        # Save some picks
        picks = [
            Pick(
                game="KC@NYG",
                predicted_winner="KC",
                confidence_points=20,
                week=3,
                actual_winner="KC",
                hit=True,
                points_earned=20,
                strategy_tag="balanced",
            )
        ]
        system.save_picks(picks)

        # Generate report
        report = system.generate_weekly_report(week=3)

        assert "week" in report
        assert "performance" in report
        assert "picks" in report
        assert "insights" in report
        assert "recommendations" in report

        assert report["week"] == 3
        assert report["performance"]["weekly_score"] == 20
        assert report["performance"]["correct_picks"] == 1
        assert report["performance"]["total_picks"] == 1
        assert report["performance"]["win_rate"] == 100.0

    def test_project_season_finish(self, temp_db):
        """Test projecting season finish."""
        system = PoolDominationSystem(db_path=temp_db)

        projection = system.project_season_finish()

        assert "current_rank" in projection
        assert "total_players" in projection
        assert "projected_final_rank" in projection
        assert "win_probability" in projection
        assert "expected_final_score" in projection

        assert isinstance(projection["current_rank"], int)
        assert isinstance(projection["total_players"], int)
        assert isinstance(projection["projected_final_rank"], int)
        assert isinstance(projection["win_probability"], float)
        assert isinstance(projection["expected_final_score"], float)

    def test_apply_strategy_override(self, temp_db):
        """Test applying strategy override."""
        system = PoolDominationSystem(db_path=temp_db)

        picks = [
            Pick(
                game="KC@NYG", predicted_winner="KC", confidence_points=20, strategy_tag="balanced"
            ),
            Pick(
                game="DAL@CHI",
                predicted_winner="DAL",
                confidence_points=19,
                strategy_tag="balanced",
            ),
        ]

        overridden_picks = system.apply_strategy_override(picks, "aggressive")

        assert len(overridden_picks) == 2
        assert all(pick.strategy_tag == "aggressive" for pick in overridden_picks)

    def test_generate_openrouter_request(self, temp_db):
        """Test generating OpenRouter request."""
        system = PoolDominationSystem(db_path=temp_db)

        request = system.generate_openrouter_request(week=3)

        assert "model" in request
        assert "messages" in request
        assert "max_tokens" in request
        assert "temperature" in request

        assert request["model"] == "openai/gpt-4o-mini"
        assert len(request["messages"]) == 1
        assert request["messages"][0]["role"] == "user"
        assert "Week 3" in request["messages"][0]["content"]
