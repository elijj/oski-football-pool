"""
Tests for database operations.
"""

import os
import tempfile
from pathlib import Path

import pytest

from football_pool.database import DatabaseManager
from football_pool.models import Pick, StrategyPerformance


class TestDatabaseManager:
    """Test DatabaseManager class."""

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        yield db_path

        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)

    def test_database_initialization(self, temp_db):
        """Test database initialization."""
        db = DatabaseManager(temp_db)

        # Check that database file was created
        assert Path(temp_db).exists()

        # Check that tables were created
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]

            expected_tables = ["picks", "results", "strategies", "competitors", "llm_data"]
            for table in expected_tables:
                assert table in tables

    def test_save_and_get_picks(self, temp_db):
        """Test saving and retrieving picks."""
        db = DatabaseManager(temp_db)

        picks = [
            Pick(
                game="KC@NYG",
                predicted_winner="KC",
                confidence_points=20,
                conf=85.0,
                strategy_tag="balanced",
                week=3,
            ),
            Pick(
                game="DAL@CHI",
                predicted_winner="DAL",
                confidence_points=19,
                conf=78.0,
                strategy_tag="balanced",
                week=3,
            ),
        ]

        # Save picks
        result = db.save_picks(picks)
        assert result is True

        # Retrieve picks
        retrieved_picks = db.get_picks(week=3)
        assert len(retrieved_picks) == 2

        # Check first pick
        first_pick = retrieved_picks[0]
        assert first_pick.game == "KC@NYG"
        assert first_pick.predicted_winner == "KC"
        assert first_pick.confidence_points == 20
        assert first_pick.conf == 85.0
        assert first_pick.strategy_tag == "balanced"

    def test_update_pick_results(self, temp_db):
        """Test updating picks with results."""
        db = DatabaseManager(temp_db)

        # First save some picks
        picks = [
            Pick(game="KC@NYG", predicted_winner="KC", confidence_points=20, week=3),
            Pick(game="DAL@CHI", predicted_winner="DAL", confidence_points=19, week=3),
        ]
        db.save_picks(picks)

        # Update with results
        results = {"KC@NYG": "KC", "DAL@CHI": "CHI"}

        result = db.update_pick_results(3, results)
        assert result is True

        # Check updated picks
        updated_picks = db.get_picks(week=3)
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

    def test_save_competitor_picks(self, temp_db):
        """Test saving competitor picks."""
        db = DatabaseManager(temp_db)

        picks_data = [
            {"game": "KC@NYG", "pick": "KC", "points": 20},
            {"game": "DAL@CHI", "pick": "DAL", "points": 19},
        ]

        result = db.save_competitor_picks(3, "Uncle Bob", picks_data)
        assert result is True

        # Retrieve competitor picks
        competitor_picks = db.get_competitor_picks(week=3, competitor="Uncle Bob")
        assert len(competitor_picks) == 2

        first_pick = competitor_picks[0]
        assert first_pick.competitor_name == "Uncle Bob"
        assert first_pick.week == 3
        assert first_pick.game == "KC@NYG"
        assert first_pick.pick == "KC"
        assert first_pick.points == 20

    def test_save_strategy_performance(self, temp_db):
        """Test saving strategy performance."""
        db = DatabaseManager(temp_db)

        performance = StrategyPerformance(
            strategy_name="balanced",
            week=3,
            variance_level="medium",
            pool_position_rank=1,
            pool_position_total=20,
            weekly_score=15,
            cumulative_score=45,
            success_rate=75.0,
            notes="Good week",
        )

        result = db.save_strategy_performance(performance)
        assert result is True

        # Retrieve strategy performance
        performances = db.get_strategy_performance(week=3)
        assert len(performances) == 1

        retrieved_perf = performances[0]
        assert retrieved_perf.strategy_name == "balanced"
        assert retrieved_perf.week == 3
        assert retrieved_perf.variance_level == "medium"
        assert retrieved_perf.weekly_score == 15
        assert retrieved_perf.success_rate == 75.0

    def test_get_performance_stats(self, temp_db):
        """Test getting performance statistics."""
        db = DatabaseManager(temp_db)

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

        # Manually insert picks with results
        with db.get_connection() as conn:
            cursor = conn.cursor()
            for pick in picks:
                cursor.execute(
                    """
                    INSERT INTO picks (
                        week, game, predicted_winner, confidence_points,
                        actual_winner, hit, points_earned, strategy_tag
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        pick.week,
                        pick.game,
                        pick.predicted_winner,
                        pick.confidence_points,
                        pick.actual_winner,
                        pick.hit,
                        pick.points_earned,
                        pick.strategy_tag,
                    ),
                )
            conn.commit()

        # Get performance stats
        stats = db.get_performance_stats()

        assert stats["total_picks"] == 2
        assert stats["correct_picks"] == 1
        assert stats["total_points"] == 20
        assert stats["win_rate"] == 50.0
        assert "strategy_performance" in stats

    def test_get_competitor_patterns(self, temp_db):
        """Test getting competitor patterns."""
        db = DatabaseManager(temp_db)

        # Save competitor picks
        competitor_picks = [
            {"game": "KC@NYG", "pick": "KC", "points": 20},
            {"game": "DAL@CHI", "pick": "DAL", "points": 19},
            {"game": "GB@MINN", "pick": "GB", "points": 18},
        ]

        db.save_competitor_picks(3, "Uncle Bob", competitor_picks)
        db.save_competitor_picks(4, "Uncle Bob", competitor_picks)

        # Get patterns
        patterns = db.get_competitor_patterns()

        assert "Uncle Bob" in patterns
        bob_pattern = patterns["Uncle Bob"]
        assert bob_pattern["total_weeks"] == 2
        assert bob_pattern["total_picks"] == 6
        assert "strategy_type" in bob_pattern
