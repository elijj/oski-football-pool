#!/usr/bin/env python3
"""
Advanced Multi-Analysis Combiner

Combines multiple LLM analyses using sophisticated strategies:
1. Model Weighting (based on historical performance)
2. Confidence Weighting (higher confidence = more weight)
3. Consensus Detection (agreement across models)
4. Contrarian Edge Detection (differentiation opportunities)
"""

import json
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@dataclass
class PickAnalysis:
    """Individual pick analysis from one model."""

    game: str
    team: str
    confidence: int
    reasoning: str
    model: str
    contrarian_edge: str = ""
    value_play: str = ""


class AdvancedAnalysisCombiner:
    """Advanced combiner for multiple LLM analyses."""

    def __init__(self):
        # Model performance weights (adjust based on your experience)
        self.model_weights = {
            "gpt-4": 1.0,
            "claude-3": 0.95,
            "gpt-3.5": 0.85,
            "moonshotai/kimi-k2:free": 0.8,
            "deepseek/deepseek-chat-v3.1:free": 0.75,
            "qwen/qwen3-235b-a22b:free": 0.7,
            "openai/gpt-oss-20b:free": 0.65,
        }

        # Confidence level weights
        self.confidence_weights = {
            20: 1.0,
            19: 0.95,
            18: 0.9,
            17: 0.85,
            16: 0.8,
            15: 0.75,
            14: 0.7,
            13: 0.65,
            12: 0.6,
            11: 0.55,
            10: 0.5,
            9: 0.45,
            8: 0.4,
            7: 0.35,
            6: 0.3,
            5: 0.25,
            4: 0.2,
            3: 0.15,
            2: 0.1,
            1: 0.05,
        }

    def load_analysis(self, file_path: str, model_name: str = "unknown") -> list[PickAnalysis]:
        """Load analysis from JSON file."""
        with open(file_path) as f:
            data = json.load(f)

        picks = []
        if "optimal_picks" in data:
            for pick in data["optimal_picks"]:
                picks.append(
                    PickAnalysis(
                        game=pick.get("game", ""),
                        team=pick.get("team", ""),
                        confidence=pick.get("confidence", 0),
                        reasoning=pick.get("reasoning", ""),
                        model=model_name,
                        contrarian_edge=pick.get("contrarian_edge", ""),
                        value_play=pick.get("value_play", ""),
                    )
                )

        return picks

    def calculate_weighted_score(self, pick: PickAnalysis) -> float:
        """Calculate weighted score for a pick."""
        model_weight = self.model_weights.get(pick.model, 0.5)
        confidence_weight = self.confidence_weights.get(pick.confidence, 0.1)

        return model_weight * confidence_weight

    def find_consensus_picks(self, all_picks: list[PickAnalysis]) -> dict[str, list[PickAnalysis]]:
        """Find picks where multiple models agree."""
        game_picks = defaultdict(list)

        for pick in all_picks:
            game_picks[pick.game].append(pick)

        consensus = {}
        for game, picks in game_picks.items():
            if len(picks) > 1:  # Multiple models picked this game
                consensus[game] = picks

        return consensus

    def detect_contrarian_opportunities(self, all_picks: list[PickAnalysis]) -> list[PickAnalysis]:
        """Detect contrarian opportunities (picks that differentiate from crowd)."""
        contrarian_picks = []

        for pick in all_picks:
            # Look for contrarian indicators
            if any(
                keyword in pick.contrarian_edge.lower()
                for keyword in ["contrarian", "public wrong", "crowd", "different", "value"]
            ):
                contrarian_picks.append(pick)

        return contrarian_picks

    def combine_analyses(self, analysis_files: list[tuple[str, str]]) -> dict[str, Any]:
        """Combine multiple analyses using advanced strategies."""
        all_picks = []

        # Load all analyses
        for file_path, model_name in analysis_files:
            try:
                picks = self.load_analysis(file_path, model_name)
                all_picks.extend(picks)
                console.print(f"✅ Loaded {len(picks)} picks from {model_name}")
            except Exception as e:
                console.print(f"❌ Error loading {file_path}: {e}")

        # Find consensus picks
        consensus = self.find_consensus_picks(all_picks)

        # Detect contrarian opportunities
        contrarian_picks = self.detect_contrarian_opportunities(all_picks)

        # Calculate weighted scores
        weighted_picks = []
        for pick in all_picks:
            weighted_score = self.calculate_weighted_score(pick)
            weighted_picks.append((pick, weighted_score))

        # Sort by weighted score
        weighted_picks.sort(key=lambda x: x[1], reverse=True)

        # Create final picks (top 20 by weighted score)
        final_picks = []
        used_games = set()

        for pick, score in weighted_picks:
            if len(final_picks) >= 20:
                break

            if pick.game not in used_games:
                final_picks.append(
                    {
                        "game": pick.game,
                        "team": pick.team,
                        "confidence": pick.confidence,
                        "reasoning": pick.reasoning,
                        "weighted_score": round(score, 3),
                        "model": pick.model,
                        "contrarian_edge": pick.contrarian_edge,
                        "value_play": pick.value_play,
                    }
                )
                used_games.add(pick.game)

        return {
            "final_picks": final_picks,
            "consensus_picks": {
                game: [p.__dict__ for p in picks] for game, picks in consensus.items()
            },
            "contrarian_opportunities": [p.__dict__ for p in contrarian_picks],
            "analysis_summary": {
                "total_models": len(set(p.model for p in all_picks)),
                "total_picks": len(all_picks),
                "consensus_games": len(consensus),
                "contrarian_opportunities": len(contrarian_picks),
            },
        }

    def display_results(self, results: dict[str, Any]):
        """Display results in a formatted way."""
        console.print(Panel("🎯 Advanced Multi-Analysis Results", style="bold blue"))

        # Summary
        summary = results["analysis_summary"]
        console.print(f"📊 Models Analyzed: {summary['total_models']}")
        console.print(f"📊 Total Picks: {summary['total_picks']}")
        console.print(f"📊 Consensus Games: {summary['consensus_games']}")
        console.print(f"📊 Contrarian Opportunities: {summary['contrarian_opportunities']}")

        # Final picks table
        table = Table(title="🏆 Final Weighted Picks")
        table.add_column("Confidence", style="cyan")
        table.add_column("Game", style="green")
        table.add_column("Team", style="yellow")
        table.add_column("Score", style="magenta")
        table.add_column("Model", style="blue")

        for pick in results["final_picks"]:
            table.add_row(
                str(pick["confidence"]),
                pick["game"],
                pick["team"],
                f"{pick['weighted_score']:.3f}",
                pick["model"],
            )

        console.print(table)

        # Consensus picks
        if results["consensus_picks"]:
            console.print(Panel("🤝 Consensus Picks (Multiple Models Agree)", style="bold green"))
            for game, picks in results["consensus_picks"].items():
                models = [p["model"] for p in picks]
                console.print(f"🎯 {game}: {', '.join(set(models))}")

        # Contrarian opportunities
        if results["contrarian_opportunities"]:
            console.print(Panel("🎲 Contrarian Opportunities", style="bold red"))
            for pick in results["contrarian_opportunities"]:
                console.print(f"🎯 {pick['game']} - {pick['contrarian_edge']}")


def main():
    """Main function for command-line usage."""
    if len(sys.argv) < 2:
        console.print(
            "Usage: python advanced_analysis_combiner.py <file1:model1> <file2:model2> ..."
        )
        console.print(
            "Example: python advanced_analysis_combiner.py manual_chatgpt.json:gpt-4 manual_claude.json:claude-3"
        )
        sys.exit(1)

    # Parse arguments
    analysis_files = []
    for arg in sys.argv[1:]:
        if ":" in arg:
            file_path, model_name = arg.split(":", 1)
            analysis_files.append((file_path, model_name))
        else:
            analysis_files.append((arg, "unknown"))

    # Combine analyses
    combiner = AdvancedAnalysisCombiner()
    results = combiner.combine_analyses(analysis_files)

    # Display results
    combiner.display_results(results)

    # Save results
    output_file = "advanced_combined_analysis.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    console.print(f"💾 Results saved to {output_file}")


if __name__ == "__main__":
    main()
