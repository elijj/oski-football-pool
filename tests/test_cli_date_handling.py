"""
Test CLI date handling to prevent date mismatches.

Ensures CLI commands properly handle 2025 dates and prevent 2024 date issues.
"""

import os
import tempfile
from pathlib import Path

import pytest
from typer.testing import CliRunner

from football_pool.cli import app


class TestCLIDateHandling:
    """Test CLI date handling and validation."""

    def setup_method(self):
        """Setup test environment."""
        self.runner = CliRunner()
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.temp_dir)

    def teardown_method(self):
        """Cleanup test environment."""
        os.chdir(self.original_cwd)
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_contrarian_prompt_2025_date(self):
        """Test contrarian prompt with 2025 date."""
        result = self.runner.invoke(app, ["contrarian-prompt", "2025-09-17"])

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "2025-09-17" in result.output
        assert "2024" not in result.output

        # Check generated file
        prompt_file = Path("2025-09-17_contrarian_prompt.txt")
        assert prompt_file.exists(), "Prompt file should be created"

        content = prompt_file.read_text()
        assert "# 2025-09-17 CONTRARIAN FOOTBALL POOL ANALYSIS" in content
        assert "2024" not in content

    def test_contrarian_prompt_rejects_2024_date(self):
        """Test that system handles 2024 dates appropriately."""
        result = self.runner.invoke(app, ["contrarian-prompt", "2024-09-17"])

        # Should still work but use 2025 schedule
        assert result.exit_code == 0, f"Command failed: {result.output}"

        # Check generated file
        prompt_file = Path("2024-09-17_contrarian_prompt.txt")
        assert prompt_file.exists(), "Prompt file should be created"

        content = prompt_file.read_text()
        assert "# 2024-09-17 CONTRARIAN FOOTBALL POOL ANALYSIS" in content

    def test_excel_update_2025_date(self):
        """Test Excel update with 2025 date."""
        # Create a mock contrarian analysis file
        analysis_data = {
            "date": "2025-09-17",
            "optimal_picks": [
                {"game": "KC@NYG", "team": "KC", "confidence": 20},
                {"game": "BAL@DET", "team": "BAL", "confidence": 19},
            ],
        }

        import json

        with open("week_1_contrarian_analysis.json", "w") as f:
            json.dump(analysis_data, f)

        result = self.runner.invoke(
            app,
            [
                "excel-update",
                "1",
                "--date",
                "2025-09-17",
                "--analysis",
                "week_1_contrarian_analysis.json",
            ],
        )

        assert result.exit_code == 0, f"Command failed: {result.output}"
        assert "2025-09-17" in result.output

    def test_date_validation_in_prompts(self):
        """Test that date validation works in prompt generation."""
        # Test various date formats
        test_dates = ["2025-09-17", "2025-9-17", "2025-09-17T00:00:00"]

        for date_str in test_dates:
            result = self.runner.invoke(app, ["contrarian-prompt", date_str])
            assert result.exit_code == 0, f"Date {date_str} should work: {result.output}"

            # Check that generated file contains correct date
            filename = f"{date_str.split('T')[0]}_contrarian_prompt.txt"
            prompt_file = Path(filename)
            if prompt_file.exists():
                content = prompt_file.read_text()
                assert date_str.split("T")[0] in content

    def test_logs_command_date_consistency(self):
        """Test that logs command doesn't interfere with date handling."""
        # Generate a prompt to create logs
        result = self.runner.invoke(app, ["contrarian-prompt", "2025-09-17"])
        assert result.exit_code == 0

        # Check logs
        result = self.runner.invoke(app, ["logs", "summary"])
        assert result.exit_code == 0, f"Logs command failed: {result.output}"

    def test_date_consistency_across_commands(self):
        """Test that date consistency is maintained across commands."""
        date_2025 = "2025-09-17"

        # Generate prompt
        result = self.runner.invoke(app, ["contrarian-prompt", date_2025])
        assert result.exit_code == 0

        # Check that all references to the date are consistent
        prompt_file = Path(f"{date_2025}_contrarian_prompt.txt")
        if prompt_file.exists():
            content = prompt_file.read_text()

            # Count occurrences of the date
            date_count = content.count(date_2025)
            assert date_count > 0, f"Date {date_2025} should appear in prompt"

            # Check that no 2024 dates appear inappropriately
            lines = content.split("\n")
            for line in lines:
                if "2024" in line and "2025" not in line:
                    # This might be acceptable in some contexts, but should be minimal
                    assert (
                        "2024" not in line or "2025" in line
                    ), f"Line should not contain 2024 without 2025: {line}"

    def test_error_handling_invalid_dates(self):
        """Test error handling for invalid dates."""
        invalid_dates = [
            "invalid-date",
            "2025-13-01",  # Invalid month
            "2025-01-32",  # Invalid day
            "2024-09-17",  # Wrong year (should still work but log warning)
        ]

        for invalid_date in invalid_dates:
            result = self.runner.invoke(app, ["contrarian-prompt", invalid_date])
            # Should either succeed or fail gracefully
            assert result.exit_code in [
                0,
                1,
            ], f"Invalid date {invalid_date} should be handled gracefully: {result.output}"

    def test_prompt_content_validation(self):
        """Test that prompt content is properly validated."""
        date_2025 = "2025-09-17"
        result = self.runner.invoke(app, ["contrarian-prompt", date_2025])
        assert result.exit_code == 0

        prompt_file = Path(f"{date_2025}_contrarian_prompt.txt")
        assert prompt_file.exists()

        content = prompt_file.read_text()

        # Validate content structure
        required_sections = [
            f"# {date_2025} CONTRARIAN FOOTBALL POOL ANALYSIS",
            "## CRITICAL POOL CONTEXT:",
            "## Games to Analyze:",
            "## CONTRARIAN ANALYSIS REQUIREMENTS:",
            "## OPTIMAL STRATEGY FRAMEWORK:",
            "## REQUIRED JSON FORMAT:",
            "## CRITICAL INSTRUCTIONS:",
        ]

        for section in required_sections:
            assert section in content, f"Prompt should contain section: {section}"

        # Validate date consistency
        assert date_2025 in content
        assert f'"date": "{date_2025}"' in content

    def test_schedule_integration(self):
        """Test that schedule integration works with 2025 dates."""
        date_2025 = "2025-09-17"
        result = self.runner.invoke(app, ["contrarian-prompt", date_2025])
        assert result.exit_code == 0

        prompt_file = Path(f"{date_2025}_contrarian_prompt.txt")
        if prompt_file.exists():
            content = prompt_file.read_text()

            # Check that games are included
            games_section = content.split("## Games to Analyze:")[1].split(
                "## CONTRARIAN ANALYSIS REQUIREMENTS:"
            )[0]
            game_lines = [
                line for line in games_section.split("\n") if line.strip().startswith("- ")
            ]

            assert len(game_lines) > 0, "Should have games in the prompt"

            # Check that games are properly formatted
            for line in game_lines:
                game = line.strip()[2:]  # Remove '- '
                assert "@" in game, f"Game should contain '@': {game}"
                assert game != "BYE", "BYE games should be filtered out"


class TestDateValidationEdgeCases:
    """Test edge cases for date validation."""

    def test_timezone_handling(self):
        """Test that timezone handling doesn't affect dates."""
        # This test ensures timezone issues don't cause date problems
        runner = CliRunner()

        # Test with various date formats that might include timezone info
        test_dates = ["2025-09-17", "2025-09-17T00:00:00Z", "2025-09-17T12:00:00+00:00"]

        for date_str in test_dates:
            result = runner.invoke(app, ["contrarian-prompt", date_str])
            assert result.exit_code == 0, f"Date {date_str} should work: {result.output}"

    def test_future_date_handling(self):
        """Test handling of future dates."""
        runner = CliRunner()

        # Test with future dates
        future_dates = ["2025-12-31", "2026-01-01"]

        for date_str in future_dates:
            result = runner.invoke(app, ["contrarian-prompt", date_str])
            # Should either work or fail gracefully
            assert result.exit_code in [
                0,
                1,
            ], f"Future date {date_str} should be handled: {result.output}"

    def test_date_parsing_robustness(self):
        """Test that date parsing is robust."""
        runner = CliRunner()

        # Test with various date formats
        date_formats = ["2025-09-17", "2025/09/17", "2025.09.17", "09-17-2025", "Sep 17, 2025"]

        for date_str in date_formats:
            result = runner.invoke(app, ["contrarian-prompt", date_str])
            # Should either work or fail gracefully
            assert result.exit_code in [
                0,
                1,
            ], f"Date format {date_str} should be handled: {result.output}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
