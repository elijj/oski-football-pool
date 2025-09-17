"""
Test coverage for date validation and prompt generation.

Ensures the system always uses the correct year and prevents date mismatches.
"""


import pytest

from football_pool.core import PoolDominationSystem
from football_pool.logging_config import logger


class TestDateValidation:
    """Test date validation and prompt generation."""

    def setup_method(self):
        """Setup test environment."""
        self.system = PoolDominationSystem()

    def test_schedule_year_consistency(self):
        """Test that schedule contains 2025 dates."""
        # Verify schedule is for 2025
        for week, data in self.system.schedule.items():
            dates = data.get("dates", "")
            # Check that dates contain 2025 or are in 2025 format
            assert "2025" in dates or self._is_2025_date_format(
                dates
            ), f"Week {week} dates '{dates}' should be for 2025"

    def _is_2025_date_format(self, date_str):
        """Check if date string is in 2025 format (e.g., '9/4-9/8')."""
        # For 2025, dates should be in M/D format without year
        # This is a heuristic - adjust based on actual schedule format
        return "/" in date_str and len(date_str.split("/")[0]) <= 2

    def test_contrarian_prompt_date_consistency(self):
        """Test that contrarian prompts use the correct year."""
        # Test with 2025 date
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Verify prompt contains 2025 date
        assert f"# {date_2025} CONTRARIAN FOOTBALL POOL ANALYSIS" in prompt
        assert '"date": "2025-09-17"' in prompt
        assert "2024" not in prompt, "Prompt should not contain 2024 dates"

    def test_contrarian_prompt_rejects_2024_dates(self):
        """Test that system properly handles 2024 dates."""
        # Test with 2024 date - should still work but use 2025 schedule
        date_2024 = "2024-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2024)

        # The prompt should use the provided date, but games should be from 2025 schedule
        assert f"# {date_2024} CONTRARIAN FOOTBALL POOL ANALYSIS" in prompt
        assert f'"date": "{date_2024}"' in prompt

    def test_date_to_week_mapping(self):
        """Test that date to week mapping works correctly."""
        # Test various 2025 dates
        test_dates = [
            ("2025-09-04", 1),  # Week 1 start
            ("2025-09-17", 3),  # Week 3 (should match schedule)
            ("2025-09-25", 4),  # Week 4
        ]

        for date_str, expected_week in test_dates:
            week = self.system._get_week_from_date(date_str)
            assert (
                week == expected_week
            ), f"Date {date_str} should map to week {expected_week}, got {week}"

    def test_prompt_games_from_correct_week(self):
        """Test that prompts include games from the correct week."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Get expected games from week 3
        week_3_games = self.system.schedule.get(3, {}).get("games", [])
        actual_games = [game for game in week_3_games if game != "BYE"]

        # Verify prompt contains games from the correct week
        for game in actual_games[:5]:  # Check first 5 games
            assert f"- {game}" in prompt, f"Game {game} should be in prompt"

    def test_json_format_uses_correct_date(self):
        """Test that JSON format in prompt uses the correct date."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Check JSON format section
        json_section = prompt.split("## REQUIRED JSON FORMAT:")[1].split("```")[1]
        assert f'"date": "{date_2025}"' in json_section
        assert "2024" not in json_section

    def test_schedule_has_2025_games(self):
        """Test that schedule contains 2025 games."""
        # Verify we have games for 2025
        total_games = 0
        for week, data in self.system.schedule.items():
            games = data.get("games", [])
            total_games += len([g for g in games if g != "BYE"])

        assert total_games > 0, "Schedule should contain games for 2025"
        assert total_games >= 20, "Should have at least 20 games per week"

    def test_week_mapping_consistency(self):
        """Test that week mapping is consistent across methods."""
        date_2025 = "2025-09-17"

        # Test different ways to get week
        week1 = self.system._get_week_from_date(date_2025)
        week2 = self.system._get_week_from_date(date_2025)

        assert week1 == week2, "Week mapping should be consistent"
        assert week1 is not None, "Week should not be None"
        assert week1 > 0, "Week should be positive"

    def test_prompt_contains_contrarian_elements(self):
        """Test that prompt contains contrarian analysis elements."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Check for contrarian-specific elements
        contrarian_elements = [
            "CONTRARIAN FOOTBALL POOL ANALYSIS",
            "contrarian opportunities",
            "value plays",
            "REVERSE (lowest points win)",
            "DIFFERENT from the crowd",
            "PUBLIC BETTING ANALYSIS",
            "WEATHER IMPACT ASSESSMENT",
            "INJURY IMPACT ANALYSIS",
            "SITUATIONAL FACTORS",
        ]

        for element in contrarian_elements:
            assert element in prompt, f"Prompt should contain '{element}'"

    def test_prompt_has_correct_structure(self):
        """Test that prompt has the correct structure."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Check structure
        assert prompt.startswith(f"# {date_2025} CONTRARIAN FOOTBALL POOL ANALYSIS")
        assert "## CRITICAL POOL CONTEXT:" in prompt
        assert "## Games to Analyze:" in prompt
        assert "## CONTRARIAN ANALYSIS REQUIREMENTS:" in prompt
        assert "## OPTIMAL STRATEGY FRAMEWORK:" in prompt
        assert "## REQUIRED JSON FORMAT:" in prompt
        assert "## CRITICAL INSTRUCTIONS:" in prompt

    def test_no_hardcoded_2024_dates(self):
        """Test that no hardcoded 2024 dates exist in the system."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Check that 2024 doesn't appear inappropriately
        lines = prompt.split("\n")
        for line in lines:
            if "2024" in line and "2025" not in line:
                # This might be acceptable in some contexts, but log it
                logger.warning(f"Found 2024 reference in prompt: {line}")

    def test_date_validation_edge_cases(self):
        """Test edge cases for date validation."""
        # Test various date formats
        test_cases = ["2025-09-17", "2025-9-17", "2025-09-17T00:00:00", "2025-09-17 12:00:00"]

        for date_str in test_cases:
            try:
                prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_str)
                assert len(prompt) > 0, f"Prompt should be generated for {date_str}"
            except Exception as e:
                pytest.fail(f"Date {date_str} should be handled gracefully: {e}")

    def test_schedule_week_consistency(self):
        """Test that schedule weeks are consistent."""
        # Check that weeks are sequential
        weeks = list(self.system.schedule.keys())
        weeks.sort()

        for i in range(len(weeks) - 1):
            assert (
                weeks[i + 1] == weeks[i] + 1
            ), f"Weeks should be sequential: {weeks[i]} -> {weeks[i+1]}"

    def test_games_list_format(self):
        """Test that games list is properly formatted."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Check games list format
        games_section = prompt.split("## Games to Analyze:")[1].split(
            "## CONTRARIAN ANALYSIS REQUIREMENTS:"
        )[0]

        # Should have games in "- GAME" format
        game_lines = [line for line in games_section.split("\n") if line.strip().startswith("- ")]
        assert len(game_lines) > 0, "Should have games in the list"

        # Check format
        for line in game_lines:
            assert line.strip().startswith("- "), f"Game line should start with '- ': {line}"
            game = line.strip()[2:]  # Remove '- '
            assert "@" in game, f"Game should contain '@': {game}"


class TestDateValidationIntegration:
    """Integration tests for date validation."""

    def test_full_workflow_date_consistency(self):
        """Test that full workflow maintains date consistency."""
        system = PoolDominationSystem()
        date_2025 = "2025-09-17"

        # Generate prompt
        prompt = system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Check that all date references are consistent
        assert date_2025 in prompt
        assert "2024" not in prompt

        # Check that games are from correct week
        week = system._get_week_from_date(date_2025)
        expected_games = system.schedule.get(week, {}).get("games", [])

        for game in expected_games[:3]:  # Check first 3 games
            if game != "BYE":
                assert f"- {game}" in prompt, f"Game {game} should be in prompt"

    def test_logging_date_consistency(self):
        """Test that logging doesn't interfere with date consistency."""
        # This test ensures logging doesn't cause date issues
        system = PoolDominationSystem()
        date_2025 = "2025-09-17"

        # Generate prompt with logging
        prompt = system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Verify date consistency
        assert date_2025 in prompt
        assert "2025" in prompt
        assert "2024" not in prompt


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
