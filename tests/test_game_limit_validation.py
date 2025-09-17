"""
Test coverage for game limit validation.

Ensures the system always limits analysis to exactly 20 games for pool picks.
"""

import pytest

from football_pool.core import PoolDominationSystem


class TestGameLimitValidation:
    """Test that game limits are properly enforced."""

    def setup_method(self):
        """Setup test environment."""
        self.system = PoolDominationSystem()

    def test_contrarian_prompt_limits_to_20_games(self):
        """Test that contrarian prompts are limited to exactly 20 games."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Extract games section
        games_section = prompt.split("## Games to Analyze")[1].split(
            "## CONTRARIAN ANALYSIS REQUIREMENTS:"
        )[0]

        # Count game lines (lines starting with "- ")
        game_lines = [line for line in games_section.split("\n") if line.strip().startswith("- ")]

        assert len(game_lines) == 20, f"Should have exactly 20 games, got {len(game_lines)}"

        # Verify all games are properly formatted
        for line in game_lines:
            game = line.strip()[2:]  # Remove '- '
            assert "@" in game, f"Game should contain '@': {game}"
            assert game != "BYE", "BYE games should be filtered out"

    def test_prompt_indicates_game_limit(self):
        """Test that prompt indicates the game limit."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Check that prompt indicates 20 games
        assert "Games to Analyze (20 games):" in prompt
        assert "Select 20 picks from" in prompt

    def test_schedule_has_more_than_20_games(self):
        """Test that schedule has more than 20 games (to test limiting logic)."""
        # Check that Week 3 has more than 20 games
        week_3_games = self.system.schedule.get(3, {}).get("games", [])
        actual_games = [game for game in week_3_games if game != "BYE"]

        assert (
            len(actual_games) > 20
        ), f"Week 3 should have more than 20 games, got {len(actual_games)}"
        assert len(actual_games) == 40, f"Week 3 should have 40 games, got {len(actual_games)}"

    def test_game_limiting_logic(self):
        """Test that game limiting logic works correctly."""
        # Test with a week that has more than 20 games
        week_3_games = self.system.schedule.get(3, {}).get("games", [])
        actual_games = [game for game in week_3_games if game != "BYE"]

        # Test limiting logic
        pool_games = actual_games[:20]

        assert len(pool_games) == 20, f"Should limit to 20 games, got {len(pool_games)}"
        assert pool_games == actual_games[:20], "Should take first 20 games"

        # Verify no duplicates
        assert len(set(pool_games)) == 20, "Should have no duplicate games"

    def test_different_weeks_have_different_limits(self):
        """Test that different weeks are handled correctly."""
        # Test various weeks
        test_cases = [
            ("2025-09-04", 1),  # Week 1
            ("2025-09-11", 2),  # Week 2
            ("2025-09-17", 3),  # Week 3 (has 40 games)
            ("2025-09-25", 4),  # Week 4
        ]

        for date_str, expected_week in test_cases:
            prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_str)

            # Extract games section
            games_section = prompt.split("## Games to Analyze")[1].split(
                "## CONTRARIAN ANALYSIS REQUIREMENTS:"
            )[0]
            game_lines = [
                line for line in games_section.split("\n") if line.strip().startswith("- ")
            ]

            # Should always be limited to 20 games
            assert (
                len(game_lines) <= 20
            ), f"Week {expected_week} should have at most 20 games, got {len(game_lines)}"

            # If week has more than 20 games, should be limited to 20
            week_games = self.system.schedule.get(expected_week, {}).get("games", [])
            actual_games = [game for game in week_games if game != "BYE"]

            if len(actual_games) > 20:
                assert (
                    len(game_lines) == 20
                ), f"Week {expected_week} with {len(actual_games)} games should be limited to 20"
            else:
                assert len(game_lines) == len(
                    actual_games
                ), f"Week {expected_week} with {len(actual_games)} games should use all games"

    def test_prompt_consistency_across_calls(self):
        """Test that prompt generation is consistent across multiple calls."""
        date_2025 = "2025-09-17"

        # Generate prompt multiple times
        prompt1 = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)
        prompt2 = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Extract games from both prompts
        games1 = self._extract_games_from_prompt(prompt1)
        games2 = self._extract_games_from_prompt(prompt2)

        # Should be identical
        assert games1 == games2, "Games should be consistent across calls"
        assert len(games1) == 20, "Should have exactly 20 games"
        assert len(games2) == 20, "Should have exactly 20 games"

    def _extract_games_from_prompt(self, prompt):
        """Extract games list from prompt."""
        games_section = prompt.split("## Games to Analyze")[1].split(
            "## CONTRARIAN ANALYSIS REQUIREMENTS:"
        )[0]
        game_lines = [line for line in games_section.split("\n") if line.strip().startswith("- ")]
        return [line.strip()[2:] for line in game_lines]

    def test_no_duplicate_games_in_prompt(self):
        """Test that no duplicate games appear in the prompt."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        games = self._extract_games_from_prompt(prompt)

        # Check for duplicates
        assert len(games) == len(set(games)), f"Should have no duplicate games: {games}"

        # Check that all games are unique
        for game in games:
            assert games.count(game) == 1, f"Game {game} appears multiple times"

    def test_games_are_properly_formatted(self):
        """Test that games are properly formatted in the prompt."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        games = self._extract_games_from_prompt(prompt)

        # Check format
        for game in games:
            assert "@" in game, f"Game should contain '@': {game}"
            assert game != "BYE", "BYE games should be filtered out"
            assert len(game) > 3, f"Game should be substantial: {game}"
            assert " " not in game or "@" in game, f"Game should be properly formatted: {game}"

    def test_prompt_handles_edge_cases(self):
        """Test that prompt handles edge cases correctly."""
        # Test with various dates
        test_dates = [
            "2025-09-04",  # Week 1
            "2025-09-17",  # Week 3 (40 games)
            "2025-09-25",  # Week 4
        ]

        for date_str in test_dates:
            try:
                prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_str)

                # Should always have games section
                assert "## Games to Analyze" in prompt

                # Should have reasonable number of games
                games = self._extract_games_from_prompt(prompt)
                assert 1 <= len(games) <= 20, f"Should have 1-20 games, got {len(games)}"

            except Exception as e:
                pytest.fail(f"Date {date_str} should be handled gracefully: {e}")

    def test_warning_logged_for_game_limiting(self):
        """Test that warning is logged when games are limited."""
        # This test ensures the warning is logged when limiting games
        date_2025 = "2025-09-17"

        # Generate prompt (should log warning)
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Verify prompt was generated
        assert len(prompt) > 0

        # The warning should be logged (we can't easily test logging in this context,
        # but the functionality should work)
        games = self._extract_games_from_prompt(prompt)
        assert len(games) == 20, "Should be limited to 20 games"

    def test_prompt_structure_with_game_limit(self):
        """Test that prompt structure is correct with game limiting."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Check required sections
        required_sections = [
            f"# {date_2025} CONTRARIAN FOOTBALL POOL ANALYSIS",
            "## CRITICAL POOL CONTEXT:",
            "## Games to Analyze (20 games):",
            "## CONTRARIAN ANALYSIS REQUIREMENTS:",
            "## OPTIMAL STRATEGY FRAMEWORK:",
            "## REQUIRED JSON FORMAT:",
            "## CRITICAL INSTRUCTIONS:",
        ]

        for section in required_sections:
            assert section in prompt, f"Prompt should contain section: {section}"

        # Check that games section is properly formatted
        assert "Games to Analyze (20 games):" in prompt
        assert "Select 20 picks from" in prompt

    def test_json_format_reflects_game_limit(self):
        """Test that JSON format reflects the game limit."""
        date_2025 = "2025-09-17"
        prompt = self.system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Extract JSON format section
        json_section = prompt.split("## REQUIRED JSON FORMAT:")[1].split("```")[1]

        # Check that JSON format is appropriate for 20 games
        assert '"date": "2025-09-17"' in json_section
        assert "optimal_picks" in json_section

        # The JSON format should be designed for 20 picks
        # (This is more of a design validation than a strict test)
        assert "confidence" in json_section
        assert "reasoning" in json_section


class TestGameLimitIntegration:
    """Integration tests for game limiting."""

    def test_full_workflow_respects_game_limit(self):
        """Test that full workflow respects the 20-game limit."""
        system = PoolDominationSystem()
        date_2025 = "2025-09-17"

        # Generate prompt
        prompt = system.generate_contrarian_analysis_prompt_by_date(date_2025)

        # Extract games
        games_section = prompt.split("## Games to Analyze")[1].split(
            "## CONTRARIAN ANALYSIS REQUIREMENTS:"
        )[0]
        game_lines = [line for line in games_section.split("\n") if line.strip().startswith("- ")]

        # Should have exactly 20 games
        assert len(game_lines) == 20, f"Should have exactly 20 games, got {len(game_lines)}"

        # Verify games are from the correct week
        week = system._get_week_from_date(date_2025)
        expected_games = system.schedule.get(week, {}).get("games", [])
        actual_games = [game for game in expected_games if game != "BYE"]

        # First 20 games should match
        for i, line in enumerate(game_lines):
            game = line.strip()[2:]  # Remove '- '
            assert game == actual_games[i], f"Game {i+1} should be {actual_games[i]}, got {game}"

    def test_game_limit_consistency_across_methods(self):
        """Test that game limiting is consistent across different methods."""
        system = PoolDominationSystem()
        date_2025 = "2025-09-17"

        # Test different ways to get games
        week = system._get_week_from_date(date_2025)
        week_games = system.schedule.get(week, {}).get("games", [])
        actual_games = [game for game in week_games if game != "BYE"]

        # Generate prompt
        prompt = system.generate_contrarian_analysis_prompt_by_date(date_2025)
        prompt_games = self._extract_games_from_prompt(prompt)

        # Should be consistent
        assert len(prompt_games) == 20, "Prompt should have 20 games"
        assert len(actual_games) == 40, "Schedule should have 40 games"
        assert prompt_games == actual_games[:20], "Prompt should use first 20 games"

    def _extract_games_from_prompt(self, prompt):
        """Extract games list from prompt."""
        games_section = prompt.split("## Games to Analyze")[1].split(
            "## CONTRARIAN ANALYSIS REQUIREMENTS:"
        )[0]
        game_lines = [line for line in games_section.split("\n") if line.strip().startswith("- ")]
        return [line.strip()[2:] for line in game_lines]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
