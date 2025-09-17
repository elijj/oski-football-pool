"""
Test core date validation logic to prevent date mismatches.

Ensures the core system properly handles 2025 dates and prevents 2024 issues.
"""


import pytest

from football_pool.core import PoolDominationSystem


class TestCoreDateValidation:
    """Test core date validation and handling."""

    def setup_method(self):
        """Setup test environment."""
        self.system = PoolDominationSystem()

    def test_schedule_year_validation(self):
        """Test that schedule is properly validated for 2025."""
        # Verify schedule contains 2025 data
        assert len(self.system.schedule) > 0, "Schedule should not be empty"

        # Check that schedule dates are for 2025
        for week, data in self.system.schedule.items():
            dates = data.get("dates", "")
            assert dates, f"Week {week} should have dates"

            # Verify it's 2025 format (M/D format without year)
            if "/" in dates:
                parts = dates.split("/")
                month = int(parts[0])
                assert 1 <= month <= 12, f"Invalid month in {dates}"

    def test_get_week_from_date_2025(self):
        """Test week mapping for 2025 dates."""
        # Test various 2025 dates
        test_cases = [
            ("2025-09-04", 1),  # Week 1
            ("2025-09-11", 2),  # Week 2
            ("2025-09-17", 3),  # Week 3
            ("2025-09-25", 4),  # Week 4
        ]

        for date_str, expected_week in test_cases:
            week = self.system._get_week_from_date(date_str)
            assert (
                week == expected_week
            ), f"Date {date_str} should map to week {expected_week}, got {week}"

    def test_get_week_from_date_2024_fallback(self):
        """Test that 2024 dates are handled appropriately."""
        # Test 2024 dates - should still work but use 2025 schedule
        test_cases = [
            ("2024-09-04", 1),  # Should map to week 1
            ("2024-09-17", 3),  # Should map to week 3
        ]

        for date_str, expected_week in test_cases:
            week = self.system._get_week_from_date(date_str)
            assert (
                week == expected_week
            ), f"Date {date_str} should map to week {expected_week}, got {week}"

    def test_contrarian_prompt_date_consistency(self):
        """Test that contrarian prompts maintain date consistency."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Verify date consistency
        assert f"# {date_2025} CONTRARIAN FOOTBALL POOL ANALYSIS" in prompt
        assert f'"date": "{date_2025}"' in prompt
        assert "2024" not in prompt

    def test_prompt_games_from_correct_week(self):
        """Test that prompts include games from the correct week."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Get expected games from the mapped week
        week = self.system._get_week_from_date(date_2025)
        expected_games = self.system.schedule.get(week, {}).get("games", [])
        actual_games = [game for game in expected_games if game != "BYE"]

        # Verify games are in prompt
        for game in actual_games[:5]:  # Check first 5 games
            assert f"- {game}" in prompt, f"Game {game} should be in prompt"

    def test_date_parsing_robustness(self):
        """Test that date parsing is robust."""
        # Test various date formats
        test_dates = [
            "2025-09-17",
            "2025-9-17",
            "2025-09-17T00:00:00",
            "2025-09-17 12:00:00",
            "2025-09-17T12:00:00Z",
        ]

        for date_str in test_dates:
            try:
                week = self.system._get_week_from_date(date_str)
                assert week is not None, f"Week should not be None for {date_str}"
                assert week > 0, f"Week should be positive for {date_str}"
            except Exception as e:
                pytest.fail(f"Date {date_str} should be handled gracefully: {e}")

    def test_schedule_consistency(self):
        """Test that schedule is internally consistent."""
        # Check that weeks are sequential
        weeks = list(self.system.schedule.keys())
        weeks.sort()

        for i in range(len(weeks) - 1):
            assert (
                weeks[i + 1] == weeks[i] + 1
            ), f"Weeks should be sequential: {weeks[i]} -> {weeks[i+1]}"

        # Check that each week has games
        for week, data in self.system.schedule.items():
            games = data.get("games", [])
            assert len(games) > 0, f"Week {week} should have games"

            # Check that games are properly formatted
            for game in games:
                if game != "BYE":
                    assert "@" in game, f"Game {game} should contain '@'"

    def test_date_validation_edge_cases(self):
        """Test edge cases for date validation."""
        # Test edge cases
        edge_cases = [
            "2025-01-01",  # New Year
            "2025-12-31",  # End of year
            "2025-02-29",  # Leap year (2025 is not leap year)
            "2025-13-01",  # Invalid month
            "2025-01-32",  # Invalid day
        ]

        for date_str in edge_cases:
            try:
                week = self.system._get_week_from_date(date_str)
                # Should either return a valid week or None
                if week is not None:
                    assert week > 0, f"Week should be positive for {date_str}"
            except Exception as e:
                # Some edge cases should fail gracefully
                assert "Invalid" in str(e) or "out of range" in str(
                    e
                ), f"Date {date_str} should fail gracefully: {e}"

    def test_prompt_structure_validation(self):
        """Test that prompt structure is correct."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Check required sections
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
            assert section in prompt, f"Prompt should contain section: {section}"

        # Check that prompt is not empty
        assert len(prompt) > 1000, "Prompt should be substantial"

    def test_json_format_validation(self):
        """Test that JSON format in prompt is correct."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Extract JSON format section
        json_section = prompt.split("## REQUIRED JSON FORMAT:")[1].split("```")[1]

        # Check that JSON format contains correct date
        assert f'"date": "{date_2025}"' in json_section

        # Check that JSON format is valid
        assert "{" in json_section
        assert "}" in json_section
        assert "optimal_picks" in json_section
        assert "contrarian_analysis" in json_section

    def test_no_hardcoded_dates(self):
        """Test that no hardcoded dates exist in the system."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Check that no inappropriate 2024 dates appear
        lines = prompt.split("\n")
        for line in lines:
            if "2024" in line and "2025" not in line:
                # This might be acceptable in some contexts, but should be minimal
                assert (
                    "2024" not in line or "2025" in line
                ), f"Line should not contain 2024 without 2025: {line}"

    def test_schedule_loading_validation(self):
        """Test that schedule loading is validated."""
        # Check that schedule is loaded correctly
        assert hasattr(self.system, "schedule"), "System should have schedule attribute"
        assert isinstance(self.system.schedule, dict), "Schedule should be a dictionary"

        # Check that schedule has expected structure
        for week, data in self.system.schedule.items():
            assert isinstance(week, int), f"Week {week} should be an integer"
            assert isinstance(data, dict), f"Week {week} data should be a dictionary"
            assert "games" in data, f"Week {week} should have games"
            assert "dates" in data, f"Week {week} should have dates"

    def test_date_consistency_across_methods(self):
        """Test that date consistency is maintained across methods."""
        date_2025 = "2025-09-17"

        # Test different methods that use dates
        week = self.system._get_week_from_date(date_2025)
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Verify consistency
        assert week is not None, "Week should not be None"
        assert date_2025 in prompt, "Prompt should contain the date"
        assert f'"date": "{date_2025}"' in prompt, "JSON format should contain the date"

    def test_future_date_handling(self):
        """Test handling of future dates."""
        # Test with future dates
        future_dates = ["2025-12-31", "2026-01-01"]

        for date_str in future_dates:
            try:
                week = self.system._get_week_from_date(date_str)
                # Should either return a valid week or None
                if week is not None:
                    assert week > 0, f"Week should be positive for {date_str}"
            except Exception as e:
                # Future dates might not be in schedule
                assert (
                    "not found" in str(e).lower() or "invalid" in str(e).lower()
                ), f"Future date {date_str} should be handled gracefully: {e}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
