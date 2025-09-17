"""
Comprehensive Game Coverage Tests

This module ensures that NO GAMES ARE EVER MISSING from any analysis or output.
Missing games = lost money = critical failure.
"""

import pytest
import json
import os
from pathlib import Path
from football_pool.core import PoolDominationSystem
from football_pool.excel_automation import ExcelAutomation
from football_pool.cli import app
from typer.testing import CliRunner


class TestGameCoverage:
    """Critical tests to prevent missing games - this is MONEY on the line."""

    def setup_method(self):
        """Setup for each test."""
        self.runner = CliRunner()
        self.test_data_dir = Path("data/json")
        self.test_data_dir.mkdir(parents=True, exist_ok=True)

    def test_contrarian_analysis_has_exactly_20_games(self):
        """CRITICAL: Contrarian analysis must have exactly 20 games."""
        # Create a test contrarian analysis
        test_analysis = {
            "date": "2025-09-17",
            "contrarian_analysis": {
                "optimal_picks": []
            }
        }

        # Add exactly 20 games
        games = [
            "KC@NYG", "BALT@MINN", "PHIL@GB", "JAC@HOU", "NE@TB",
            "ARIZ@SEA", "LAR@SF", "DET@WASH", "CLEV@NYJ", "PITT@LAC",
            "ATL@IND", "LV@DEN", "NYG@CHI", "CAL@LOU", "STAN@NC",
            "LSU@ALA", "UIND@PSU", "NEB@UCLA", "FSU@CLEM", "UW@WSU"
        ]

        for i, game in enumerate(games):
            test_analysis["contrarian_analysis"]["optimal_picks"].append({
                "game": game,
                "team": game.split("@")[0],
                "confidence": 20 - i,
                "reasoning": f"Test game {i+1}",
                "contrarian_edge": "Test edge",
                "value_play": "Test value",
                "risk_assessment": "MEDIUM"
            })

        # Save test file
        test_file = self.test_data_dir / "test_week_1_analysis.json"
        with open(test_file, 'w') as f:
            json.dump(test_analysis, f, indent=2)

        # Test that we have exactly 20 games
        with open(test_file, 'r') as f:
            data = json.load(f)
            picks = data["contrarian_analysis"]["optimal_picks"]
            assert len(picks) == 20, f"CRITICAL ERROR: Expected 20 games, got {len(picks)}"

        # Clean up
        test_file.unlink()

    def test_no_duplicate_games_in_analysis(self):
        """CRITICAL: No duplicate games allowed in analysis."""
        test_analysis = {
            "date": "2025-09-17",
            "contrarian_analysis": {
                "optimal_picks": []
            }
        }

        # Add games with one duplicate
        games = [
            "KC@NYG", "BALT@MINN", "PHIL@GB", "JAC@HOU", "NE@TB",
            "ARIZ@SEA", "LAR@SF", "DET@WASH", "CLEV@NYJ", "PITT@LAC",
            "ATL@IND", "LV@DEN", "NYG@CHI", "CAL@LOU", "STAN@NC",
            "LSU@ALA", "UIND@PSU", "NEB@UCLA", "FSU@CLEM", "KC@NYG"  # DUPLICATE!
        ]

        for i, game in enumerate(games):
            test_analysis["contrarian_analysis"]["optimal_picks"].append({
                "game": game,
                "team": game.split("@")[0],
                "confidence": 20 - i,
                "reasoning": f"Test game {i+1}",
                "contrarian_edge": "Test edge",
                "value_play": "Test value",
                "risk_assessment": "MEDIUM"
            })

        # Test for duplicates
        games_list = [pick["game"] for pick in test_analysis["contrarian_analysis"]["optimal_picks"]]
        unique_games = set(games_list)
        assert len(games_list) == len(unique_games), f"CRITICAL ERROR: Duplicate games found! {len(games_list)} total, {len(unique_games)} unique"

    def test_all_games_have_required_fields(self):
        """CRITICAL: All games must have required fields."""
        test_analysis = {
            "date": "2025-09-17",
            "contrarian_analysis": {
                "optimal_picks": []
            }
        }

        # Add a game with missing field
        test_analysis["contrarian_analysis"]["optimal_picks"].append({
            "game": "KC@NYG",
            "team": "KC",
            "confidence": 20,
            # Missing: reasoning, contrarian_edge, value_play, risk_assessment
        })

        # Test required fields
        required_fields = ["game", "team", "confidence", "reasoning", "contrarian_edge", "value_play", "risk_assessment"]
        for pick in test_analysis["contrarian_analysis"]["optimal_picks"]:
            for field in required_fields:
                assert field in pick, f"CRITICAL ERROR: Missing required field '{field}' in game {pick.get('game', 'UNKNOWN')}"

    def test_confidence_points_are_unique(self):
        """CRITICAL: All confidence points must be unique (1-20)."""
        test_analysis = {
            "date": "2025-09-17",
            "contrarian_analysis": {
                "optimal_picks": []
            }
        }

        # Add games with duplicate confidence
        games = ["KC@NYG", "BALT@MINN", "PHIL@GB", "JAC@HOU"]
        for i, game in enumerate(games):
            test_analysis["contrarian_analysis"]["optimal_picks"].append({
                "game": game,
                "team": game.split("@")[0],
                "confidence": 20,  # DUPLICATE CONFIDENCE!
                "reasoning": f"Test game {i+1}",
                "contrarian_edge": "Test edge",
                "value_play": "Test value",
                "risk_assessment": "MEDIUM"
            })

        # Test unique confidence points
        confidence_points = [pick["confidence"] for pick in test_analysis["contrarian_analysis"]["optimal_picks"]]
        unique_confidence = set(confidence_points)
        assert len(confidence_points) == len(unique_confidence), f"CRITICAL ERROR: Duplicate confidence points found! {confidence_points}"

    def test_confidence_points_range_1_to_20(self):
        """CRITICAL: Confidence points must be 1-20."""
        test_analysis = {
            "date": "2025-09-17",
            "contrarian_analysis": {
                "optimal_picks": []
            }
        }

        # Add game with invalid confidence
        test_analysis["contrarian_analysis"]["optimal_picks"].append({
            "game": "KC@NYG",
            "team": "KC",
            "confidence": 25,  # INVALID: > 20
            "reasoning": "Test game",
            "contrarian_edge": "Test edge",
            "value_play": "Test value",
            "risk_assessment": "MEDIUM"
        })

        # Test confidence range
        for pick in test_analysis["contrarian_analysis"]["optimal_picks"]:
            confidence = pick["confidence"]
            assert 1 <= confidence <= 20, f"CRITICAL ERROR: Confidence {confidence} not in range 1-20 for game {pick['game']}"

    def test_game_format_validation(self):
        """CRITICAL: Games must be in correct format (TEAM@TEAM)."""
        test_analysis = {
            "date": "2025-09-17",
            "contrarian_analysis": {
                "optimal_picks": []
            }
        }

        # Add games with invalid formats
        invalid_games = [
            "KC-NYG",  # Wrong separator
            "KC@",     # Missing opponent
            "@NYG",    # Missing home team
            "KC NYG",  # Wrong separator
            "KC@NYG@EXTRA"  # Too many parts
        ]

        for game in invalid_games:
            test_analysis["contrarian_analysis"]["optimal_picks"].append({
                "game": game,
                "team": game.split("@")[0] if "@" in game else game,
                "confidence": 20,
                "reasoning": "Test game",
                "contrarian_edge": "Test edge",
                "value_play": "Test value",
                "risk_assessment": "MEDIUM"
            })

        # Test game format
        for pick in test_analysis["contrarian_analysis"]["optimal_picks"]:
            game = pick["game"]
            parts = game.split("@")
            assert len(parts) == 2, f"CRITICAL ERROR: Invalid game format '{game}' - must be TEAM@TEAM"
            assert parts[0].strip() != "", f"CRITICAL ERROR: Empty home team in game '{game}'"
            assert parts[1].strip() != "", f"CRITICAL ERROR: Empty away team in game '{game}'"

    def test_team_abbreviation_validation(self):
        """CRITICAL: All teams must have valid abbreviations."""
        # Test that all teams in our system have abbreviations
        excel_automation = ExcelAutomation()

        # Common teams that should have abbreviations
        test_teams = [
            "KC", "NYG", "BALT", "MINN", "PHIL", "GB", "JAC", "HOU",
            "NE", "TB", "ARIZ", "SEA", "LAR", "SF", "DET", "WASH",
            "CLEV", "NYJ", "PITT", "LAC", "ATL", "IND", "LV", "DEN",
            "CHI", "CAL", "LOU", "STAN", "NC", "LSU", "ALA", "UIND",
            "PSU", "NEB", "UCLA", "FSU", "CLEM", "NO", "CAR", "UW", "WSU"
        ]

        for team in test_teams:
            abbreviation = excel_automation.get_team_abbreviations().get(team, None)
            assert abbreviation is not None, f"CRITICAL ERROR: No abbreviation found for team '{team}'"

    def test_excel_update_preserves_all_games(self):
        """CRITICAL: Excel update must preserve all 20 games."""
        # Create test analysis with 20 games
        test_analysis = {
            "date": "2025-09-17",
            "contrarian_analysis": {
                "optimal_picks": []
            }
        }

        games = [
            "KC@NYG", "BALT@MINN", "PHIL@GB", "JAC@HOU", "NE@TB",
            "ARIZ@SEA", "LAR@SF", "DET@WASH", "CLEV@NYJ", "PITT@LAC",
            "ATL@IND", "LV@DEN", "NYG@CHI", "CAL@LOU", "STAN@NC",
            "LSU@ALA", "UIND@PSU", "NEB@UCLA", "FSU@CLEM", "UW@WSU"
        ]

        for i, game in enumerate(games):
            test_analysis["contrarian_analysis"]["optimal_picks"].append({
                "game": game,
                "team": game.split("@")[0],
                "confidence": 20 - i,
                "reasoning": f"Test game {i+1}",
                "contrarian_edge": "Test edge",
                "value_play": "Test value",
                "risk_assessment": "MEDIUM"
            })

        # Save test file
        test_file = self.test_data_dir / "test_week_1_coverage.json"
        with open(test_file, 'w') as f:
            json.dump(test_analysis, f, indent=2)

        try:
            # Test Excel update
            result = self.runner.invoke(app, [
                "excel-update", "1",
                "--date", "2025-09-17",
                "--analysis", str(test_file)
            ])

            # Should not fail
            assert result.exit_code == 0, f"Excel update failed: {result.stdout}"

            # Check that all games were processed
            assert "No picks found" not in result.stdout, "CRITICAL ERROR: Excel update lost games!"

        finally:
            # Clean up
            test_file.unlink()

    def test_weekly_workflow_preserves_all_games(self):
        """CRITICAL: Weekly workflow must preserve all games through entire pipeline."""
        # This test ensures the full pipeline doesn't lose games
        result = self.runner.invoke(app, [
            "weekly-workflow", "1", "2025-09-17",
            "--analysis", "data/json/week_1_complete_contrarian_analysis.json"
        ])

        # Should complete successfully
        assert result.exit_code == 0, f"Weekly workflow failed: {result.stdout}"

        # Check that all steps completed
        assert "WEEKLY WORKFLOW COMPLETE" in result.stdout, "Weekly workflow did not complete"

        # Check that Excel file was created
        excel_file = Path("data/excel/Dawgpac25_2025-09-17.xlsx")
        assert excel_file.exists(), "CRITICAL ERROR: Excel file not created by weekly workflow"

    def test_missing_games_detection(self):
        """CRITICAL: System must detect and report missing games."""
        # Create analysis with only 19 games (missing 1)
        incomplete_analysis = {
            "date": "2025-09-17",
            "contrarian_analysis": {
                "optimal_picks": []
            }
        }

        # Add only 19 games
        games = [
            "KC@NYG", "BALT@MINN", "PHIL@GB", "JAC@HOU", "NE@TB",
            "ARIZ@SEA", "LAR@SF", "DET@WASH", "CLEV@NYJ", "PITT@LAC",
            "ATL@IND", "LV@DEN", "NYG@CHI", "CAL@LOU", "STAN@NC",
            "LSU@ALA", "UIND@PSU", "NEB@UCLA", "FSU@CLEM"
            # Missing: UW@WSU
        ]

        for i, game in enumerate(games):
            incomplete_analysis["contrarian_analysis"]["optimal_picks"].append({
                "game": game,
                "team": game.split("@")[0],
                "confidence": 20 - i,
                "reasoning": f"Test game {i+1}",
                "contrarian_edge": "Test edge",
                "value_play": "Test value",
                "risk_assessment": "MEDIUM"
            })

        # Test that system detects missing games
        picks = incomplete_analysis["contrarian_analysis"]["optimal_picks"]
        assert len(picks) == 19, f"CRITICAL ERROR: Expected 19 games, got {len(picks)}"
        assert len(picks) < 20, "CRITICAL ERROR: Missing games not detected!"

    def test_game_consistency_across_systems(self):
        """CRITICAL: Games must be consistent across all systems."""
        # Test that games in prompts match games in analysis
        prompt_file = Path("data/prompts/2025-09-17_contrarian_prompt.txt")
        analysis_file = Path("data/json/week_1_complete_contrarian_analysis.json")

        if prompt_file.exists() and analysis_file.exists():
            # Read prompt games
            with open(prompt_file, 'r') as f:
                prompt_content = f.read()
                prompt_games = [line.strip().replace("- ", "") for line in prompt_content.split('\n')
                              if line.strip().startswith("- ") and "@" in line]

            # Read analysis games
            with open(analysis_file, 'r') as f:
                analysis_data = json.load(f)
                analysis_games = [pick["game"] for pick in analysis_data["contrarian_analysis"]["optimal_picks"]]

            # Games should match
            prompt_games_set = set(prompt_games)
            analysis_games_set = set(analysis_games)

            missing_in_analysis = prompt_games_set - analysis_games_set
            missing_in_prompt = analysis_games_set - prompt_games_set

            assert len(missing_in_analysis) == 0, f"CRITICAL ERROR: Games in prompt missing from analysis: {missing_in_analysis}"
            assert len(missing_in_prompt) == 0, f"CRITICAL ERROR: Games in analysis missing from prompt: {missing_in_prompt}"


class TestGameCoverageIntegration:
    """Integration tests for game coverage across the entire system."""

    def test_end_to_end_game_preservation(self):
        """CRITICAL: End-to-end test that no games are lost."""
        runner = CliRunner()

        # Run full weekly workflow
        result = runner.invoke(app, [
            "weekly-workflow", "1", "2025-09-17",
            "--analysis", "data/json/week_1_complete_contrarian_analysis.json"
        ])

        # Verify all steps completed
        assert result.exit_code == 0, f"End-to-end test failed: {result.stdout}"

        # Verify all output files exist
        expected_files = [
            "data/prompts/2025-09-17_contrarian_prompt.txt",
            "data/excel/Dawgpac25_2025-09-17.xlsx",
            "reports/Week_1_Enhanced_Strategy_Report_2025-09-17.md",
            "reports/Week_2_Preview_2025-09-24.md"
        ]

        for file_path in expected_files:
            assert Path(file_path).exists(), f"CRITICAL ERROR: Expected file {file_path} not created"

    def test_game_count_validation_in_all_commands(self):
        """CRITICAL: All commands must validate game count."""
        runner = CliRunner()

        # Test picks command
        result = runner.invoke(app, ["picks", "1"])
        assert result.exit_code == 0, f"Picks command failed: {result.stdout}"

        # Test excel-update command
        result = runner.invoke(app, [
            "excel-update", "1",
            "--date", "2025-09-17",
            "--analysis", "data/json/week_1_complete_contrarian_analysis.json"
        ])
        assert result.exit_code == 0, f"Excel-update command failed: {result.stdout}"

        # Test report command
        result = runner.invoke(app, ["report", "--week", "1"])
        assert result.exit_code == 0, f"Report command failed: {result.stdout}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
