"""
Tests for CLI functionality.
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from football_pool.cli import app


class TestCLI:
    """Test CLI functionality."""

    @pytest.fixture
    def runner(self):
        """Create CLI runner for testing."""
        return CliRunner()

    @pytest.fixture
    def temp_db(self):
        """Create temporary database for testing."""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        yield db_path

        # Cleanup
        if os.path.exists(db_path):
            os.unlink(db_path)

    def test_prompt_command(self, runner):
        """Test prompt generation command."""
        result = runner.invoke(app, ["prompt", "3"])

        assert result.exit_code == 0
        assert "Week 3" in result.stdout
        assert "JSON" in result.stdout

    def test_prompt_command_with_output(self, runner, temp_dir):
        """Test prompt generation with output file."""
        output_file = temp_dir / "prompt.txt"

        result = runner.invoke(app, ["prompt", "3", "--output", str(output_file)])

        assert result.exit_code == 0
        assert output_file.exists()
        assert "Week 3" in output_file.read_text()

    def test_import_llm_command(self, runner, temp_dir):
        """Test LLM data import command."""
        # Create test LLM data file
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

        llm_file = temp_dir / "llm_data.json"
        llm_file.write_text(str(llm_data).replace("'", '"'))

        with patch("football_pool.cli.PoolDominationSystem") as mock_system:
            mock_instance = MagicMock()
            mock_system.return_value = mock_instance

            result = runner.invoke(app, ["import-llm", "3", str(llm_file)])

            assert result.exit_code == 0
            assert "LLM data imported" in result.stdout

    def test_picks_command(self, runner):
        """Test picks generation command."""
        with patch("football_pool.cli.PoolDominationSystem") as mock_system:
            mock_instance = MagicMock()
            mock_system.return_value = mock_instance

            # Mock picks
            from football_pool.models import Pick

            mock_picks = [
                Pick(
                    game="KC@NYG",
                    predicted_winner="KC",
                    confidence_points=20,
                    conf=85.0,
                    strategy_tag="balanced",
                ),
                Pick(
                    game="DAL@CHI",
                    predicted_winner="DAL",
                    confidence_points=19,
                    conf=78.0,
                    strategy_tag="balanced",
                ),
            ]
            mock_instance.generate_optimal_picks.return_value = mock_picks
            mock_instance.load_llm_data.return_value = None

            result = runner.invoke(app, ["picks", "3"])

            assert result.exit_code == 0
            assert "KC@NYG" in result.stdout
            assert "DAL@CHI" in result.stdout

    def test_picks_command_csv_format(self, runner):
        """Test picks command with CSV format."""
        with patch("football_pool.cli.PoolDominationSystem") as mock_system:
            mock_instance = MagicMock()
            mock_system.return_value = mock_instance

            # Mock picks
            from football_pool.models import Pick

            mock_picks = [
                Pick(
                    game="KC@NYG",
                    predicted_winner="KC",
                    confidence_points=20,
                    conf=85.0,
                    strategy_tag="balanced",
                ),
                Pick(
                    game="DAL@CHI",
                    predicted_winner="DAL",
                    confidence_points=19,
                    conf=78.0,
                    strategy_tag="balanced",
                ),
            ]
            mock_instance.generate_optimal_picks.return_value = mock_picks
            mock_instance.load_llm_data.return_value = None

            result = runner.invoke(app, ["picks", "3", "--format", "csv"])

            assert result.exit_code == 0
            assert "Game,Pick,Points" in result.stdout
            assert "KC@NYG,KC,20" in result.stdout

    def test_picks_command_json_format(self, runner):
        """Test picks command with JSON format."""
        with patch("football_pool.cli.PoolDominationSystem") as mock_system:
            mock_instance = MagicMock()
            mock_system.return_value = mock_instance

            # Mock picks
            from football_pool.models import Pick

            mock_picks = [
                Pick(
                    game="KC@NYG",
                    predicted_winner="KC",
                    confidence_points=20,
                    conf=85.0,
                    strategy_tag="balanced",
                )
            ]
            mock_instance.generate_optimal_picks.return_value = mock_picks
            mock_instance.load_llm_data.return_value = None

            result = runner.invoke(app, ["picks", "3", "--format", "json"])

            assert result.exit_code == 0
            assert "KC@NYG" in result.stdout
            assert "KC" in result.stdout

    def test_results_command_import(self, runner, temp_dir):
        """Test results import command."""
        # Create test results file
        results = {"KC@NYG": "KC", "DAL@CHI": "CHI"}

        results_file = temp_dir / "results.json"
        results_file.write_text(str(results).replace("'", '"'))

        with patch("football_pool.cli.PoolDominationSystem") as mock_system:
            mock_instance = MagicMock()
            mock_system.return_value = mock_instance
            mock_instance.track_results.return_value = True

            result = runner.invoke(app, ["results", "3", "--import", str(results_file)])

            assert result.exit_code == 0
            assert "Results imported" in result.stdout

    def test_report_command(self, runner):
        """Test report generation command."""
        with patch("football_pool.cli.PoolDominationSystem") as mock_system:
            mock_instance = MagicMock()
            mock_system.return_value = mock_instance

            # Mock report data
            mock_report = {
                "week": 3,
                "performance": {
                    "weekly_score": 20,
                    "correct_picks": 1,
                    "total_picks": 1,
                    "win_rate": 100.0,
                    "strategy_used": "balanced",
                },
                "insights": ["Great week!"],
                "recommendations": ["Keep it up!"],
            }
            mock_instance.generate_weekly_report.return_value = mock_report
            mock_instance.get_all_picks.return_value = []

            result = runner.invoke(app, ["report", "--week", "3"])

            assert result.exit_code == 0
            assert "Week 3" in result.stdout

    def test_stats_command(self, runner):
        """Test stats command."""
        with patch("football_pool.cli.PoolDominationSystem") as mock_system:
            mock_instance = MagicMock()
            mock_system.return_value = mock_instance

            # Mock stats
            mock_stats = {
                "total_picks": 20,
                "correct_picks": 12,
                "win_rate": 60.0,
                "total_points": 180,
                "avg_correct_confidence": 15.5,
                "avg_wrong_confidence": 8.2,
                "strategy_performance": {
                    "balanced": {"uses": 10, "wins": 6, "win_rate": 60.0, "avg_points": 9.0}
                },
            }
            mock_instance.get_performance_stats.return_value = mock_stats

            result = runner.invoke(app, ["stats"])

            assert result.exit_code == 0
            assert "Performance Statistics" in result.stdout
            assert "Total Picks" in result.stdout
            assert "Win Rate" in result.stdout

    def test_competitors_command(self, runner, temp_dir):
        """Test competitors command."""
        # Create test competitor picks file
        competitor_picks = [
            {"game": "KC@NYG", "pick": "KC", "points": 20},
            {"game": "DAL@CHI", "pick": "DAL", "points": 19},
        ]

        picks_file = temp_dir / "competitor_picks.json"
        picks_file.write_text(str(competitor_picks).replace("'", '"'))

        with patch("football_pool.cli.PoolDominationSystem") as mock_system:
            mock_instance = MagicMock()
            mock_system.return_value = mock_instance
            mock_instance.track_competitor_picks.return_value = True

            result = runner.invoke(app, ["competitors", "3", "Uncle Bob", str(picks_file)])

            assert result.exit_code == 0
            assert "Competitor picks tracked" in result.stdout

    def test_analyze_command(self, runner):
        """Test analyze command."""
        with patch("football_pool.cli.PoolDominationSystem") as mock_system:
            mock_instance = MagicMock()
            mock_system.return_value = mock_instance

            # Mock analysis data
            mock_patterns = {"Uncle Bob": {"strategy_type": "conservative", "total_weeks": 3}}
            mock_edges = {"strengths": ["balanced"], "weaknesses": ["aggressive"]}

            mock_instance.analyze_competitor_patterns.return_value = mock_patterns
            mock_instance.identify_personal_edges.return_value = mock_edges

            result = runner.invoke(app, ["analyze"])

            assert result.exit_code == 0
            assert "Competitor Analysis" in result.stdout
            assert "Personal Edges" in result.stdout

    def test_project_command(self, runner):
        """Test project command."""
        with patch("football_pool.cli.PoolDominationSystem") as mock_system:
            mock_instance = MagicMock()
            mock_system.return_value = mock_instance

            # Mock projection data
            mock_projection = {
                "current_rank": 1,
                "total_players": 20,
                "projected_final_rank": 3,
                "win_probability": 75.0,
                "expected_final_score": 300.0,
            }
            mock_instance.project_season_finish.return_value = mock_projection

            result = runner.invoke(app, ["project"])

            assert result.exit_code == 0
            assert "Season Projection" in result.stdout
            assert "Current Rank" in result.stdout
            assert "Win Probability" in result.stdout

    def test_invalid_week(self, runner):
        """Test with invalid week number."""
        result = runner.invoke(app, ["prompt", "25"])

        # Should handle gracefully or show error
        assert result.exit_code != 0 or "Week 25" in result.stdout

    def test_missing_file(self, runner):
        """Test with missing file."""
        result = runner.invoke(app, ["import-llm", "3", "nonexistent.json"])

        assert result.exit_code != 0
        assert "File not found" in result.stdout

    def test_invalid_json(self, runner, temp_dir):
        """Test with invalid JSON file."""
        invalid_file = temp_dir / "invalid.json"
        invalid_file.write_text("invalid json content")

        result = runner.invoke(app, ["import-llm", "3", str(invalid_file)])

        assert result.exit_code != 0
        assert "Invalid JSON" in result.stdout
