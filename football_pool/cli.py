"""
Command Line Interface for the Football Pool Domination System.

Provides a comprehensive CLI for managing weekly workflow.
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.table import Table

from .automation import AutomationConfig, WeeklyAutomation
from .core import PoolDominationSystem
from .excel_automation import ExcelAutomation
from .log_viewer import LogViewer
from .logging_config import logger
from .models import Pick

# Initialize Typer app
app = typer.Typer(
    name="football-pool",
    help="🏈 Football Pool Domination System - Maximize your success in confidence pools",
    add_completion=False,
    rich_markup_mode="rich",
)

# Initialize Rich console
console = Console()


@app.command()
def prompt(
    week: int = typer.Argument(..., help="Week number (3-18)"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Save prompt to file"),
    enhanced: bool = typer.Option(False, "--enhanced", help="Include real odds data in prompt"),
    force_refresh: bool = typer.Option(
        False, "--force-refresh", help="Force refresh odds data (uses API)"
    ),
):
    """Generate LLM research prompt for the specified week."""
    try:
        system = PoolDominationSystem()

        if enhanced:
            prompt_text = system.get_enhanced_llm_prompt(week, force_refresh)
            if force_refresh:
                console.print("🔄 Forced refresh of odds data (API call made)")
            else:
                console.print("🔗 Using enhanced prompt with odds data (cached if available)")
        else:
            prompt_text = system.generate_llm_research_prompt(week)

        if output_file:
            output_file.write_text(prompt_text)
            console.print(f"✅ Prompt saved to {output_file}")
        else:
            console.print(
                Panel(prompt_text, title=f"Week {week} Research Prompt", border_style="blue")
            )

    except Exception as e:
        console.print(f"❌ Error generating prompt: {e}")
        raise typer.Exit(1)


@app.command()
def contrarian_prompt(
    date: str = typer.Argument(..., help="Date for contrarian analysis (e.g., '2024-09-17')"),
    output_file: Optional[Path] = typer.Option(None, "--output", "-o", help="Save prompt to file"),
):
    """Generate contrarian analysis prompt for optimal strategy."""
    try:
        logger.log_command_start(
            "contrarian_prompt",
            {"date": date, "output_file": str(output_file) if output_file else None},
        )

        system = PoolDominationSystem()
        console.print(f"🎯 Generating CONTRARIAN ANALYSIS prompt for {date}")
        console.print("📊 Focus: Contrarian opportunities and value plays")

        # Log prompt generation
        logger.log_prompt_generation("contrarian_analysis", date)

        prompt_text = system.generate_contrarian_analysis_prompt_by_date(date)

        # Log prompt details
        logger.llm_logger.debug(f"Generated contrarian prompt: {len(prompt_text)} characters")
        logger.llm_logger.debug(f"Prompt preview: {prompt_text[:200]}...")

        if output_file:
            output_file.write_text(prompt_text)
            console.print(f"✅ Contrarian prompt saved to {output_file}")
            logger.excel_logger.info(f"Saved contrarian prompt to {output_file}")
        else:
            # Save to data/prompts directory
            os.makedirs("data/prompts", exist_ok=True)
            filename = f"data/prompts/{date}_contrarian_prompt.txt"
            with open(filename, "w") as f:
                f.write(prompt_text)
            console.print(f"💾 Contrarian prompt saved to {filename}")
            logger.excel_logger.info(f"Saved contrarian prompt to {filename}")

        # Display the prompt
        console.print(
            Panel(prompt_text, title=f"{date} Contrarian Analysis Prompt", border_style="green")
        )

        logger.log_command_end("contrarian_prompt", success=True)

    except Exception as e:
        logger.log_error(e, f"contrarian_prompt command with date {date}")
        console.print(f"❌ Error generating contrarian prompt: {e}")
        raise typer.Exit(1)


@app.command()
def import_llm(
    week: int = typer.Argument(..., help="Week number"),
    file_path: Path = typer.Argument(..., help="Path to LLM JSON file"),
    validate: bool = typer.Option(True, "--validate/--no-validate", help="Validate JSON structure"),
):
    """Import LLM analysis data for the specified week."""
    try:
        if not file_path.exists():
            console.print(f"❌ File not found: {file_path}")
            raise typer.Exit(1)

        with open(file_path) as f:
            llm_data = json.load(f)

        if validate:
            # Basic validation
            required_fields = ["games", "spreads", "public_percentages", "confidence_scores"]
            missing_fields = [field for field in required_fields if field not in llm_data]
            if missing_fields:
                console.print(f"❌ Missing required fields: {missing_fields}")
                raise typer.Exit(1)

        system = PoolDominationSystem()
        system.save_llm_data(week, llm_data)

        console.print(f"✅ LLM data imported for Week {week}")

    except json.JSONDecodeError as e:
        console.print(f"❌ Invalid JSON: {e}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"❌ Error importing LLM data: {e}")
        raise typer.Exit(1)


@app.command()
def picks(
    week: int = typer.Argument(..., help="Week number"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, csv, json"),
    strategy: Optional[str] = typer.Option(None, "--strategy", "-s", help="Override strategy"),
    save: bool = typer.Option(False, "--save", help="Save picks to database"),
):
    """Generate optimal picks for the specified week."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Generating optimal picks...", total=None)

            system = PoolDominationSystem()

            # Load LLM data if available
            llm_data = system.load_llm_data(week)

            # Generate picks
            picks = system.generate_optimal_picks(week, llm_data)

            if strategy:
                # Override strategy if specified
                picks = system.apply_strategy_override(picks, strategy)

            progress.update(task, description="✅ Picks generated!")

        # Display picks
        if format == "table":
            _display_picks_table(picks, week)
        elif format == "csv":
            _display_picks_csv(picks)
        elif format == "json":
            _display_picks_json(picks)
        else:
            console.print(f"❌ Unknown format: {format}")
            raise typer.Exit(1)

        # Save to database if requested
        if save:
            system.save_picks(picks)
            console.print("✅ Picks saved to database")

    except Exception as e:
        console.print(f"❌ Error generating picks: {e}")
        raise typer.Exit(1)


@app.command()
def results(
    week: int = typer.Argument(..., help="Week number"),
    import_file: Optional[Path] = typer.Option(
        None, "--import", "-i", help="Import results from JSON file"
    ),
    manual: bool = typer.Option(False, "--manual", help="Enter results manually"),
):
    """Track and import game results."""
    try:
        system = PoolDominationSystem()

        if import_file:
            if not import_file.exists():
                console.print(f"❌ File not found: {import_file}")
                raise typer.Exit(1)

            with open(import_file) as f:
                results = json.load(f)

            system.track_results(week, results)
            console.print(f"✅ Results imported for Week {week}")

        elif manual:
            console.print(f"Entering results for Week {week} (press Enter to skip a game)")
            results = {}

            # Get current week's games
            picks = system.get_picks(week)
            games = list(set(pick.game for pick in picks))

            for game in games:
                winner = Prompt.ask(f"Winner of {game}", default="")
                if winner:
                    results[game] = winner

            if results:
                system.track_results(week, results)
                console.print(f"✅ Results saved for Week {week}")
            else:
                console.print("❌ No results entered")

        else:
            console.print("❌ Specify either --import or --manual")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"❌ Error processing results: {e}")
        raise typer.Exit(1)


@app.command()
def report(
    week: Optional[int] = typer.Option(None, "--week", "-w", help="Week number (default: latest)"),
    format: str = typer.Option("table", "--format", "-f", help="Output format: table, json"),
):
    """Generate weekly performance report."""
    try:
        system = PoolDominationSystem()

        if week is None:
            # Get latest week with data
            picks = system.get_all_picks()
            week = max(pick.week for pick in picks) if picks else 3

        report_data = system.generate_weekly_report(week)

        if format == "table":
            _display_report_table(report_data, week)
        elif format == "json":
            console.print(json.dumps(report_data, indent=2, default=str))
        else:
            console.print(f"❌ Unknown format: {format}")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"❌ Error generating report: {e}")
        raise typer.Exit(1)


@app.command()
def stats():
    """Display overall performance statistics."""
    try:
        system = PoolDominationSystem()
        stats = system.get_performance_stats()

        # Create stats table
        table = Table(title="📊 Performance Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Total Picks", str(stats["total_picks"]))
        table.add_row("Correct Picks", str(stats["correct_picks"]))
        table.add_row("Win Rate", f"{stats['win_rate']:.1f}%")
        table.add_row("Total Points", str(stats["total_points"]))
        table.add_row("Avg Correct Confidence", f"{stats['avg_correct_confidence']:.1f}")
        table.add_row("Avg Wrong Confidence", f"{stats['avg_wrong_confidence']:.1f}")

        console.print(table)

        # Strategy performance
        if stats["strategy_performance"]:
            console.print("\n📈 Strategy Performance:")
            strategy_table = Table()
            strategy_table.add_column("Strategy", style="cyan")
            strategy_table.add_column("Uses", style="green")
            strategy_table.add_column("Wins", style="green")
            strategy_table.add_column("Win Rate", style="green")
            strategy_table.add_column("Avg Points", style="green")

            for strategy, perf in stats["strategy_performance"].items():
                strategy_table.add_row(
                    strategy,
                    str(perf["uses"]),
                    str(perf["wins"]),
                    f"{perf['win_rate']:.1f}%",
                    f"{perf['avg_points']:.1f}",
                )

            console.print(strategy_table)

    except Exception as e:
        console.print(f"❌ Error getting stats: {e}")
        raise typer.Exit(1)


@app.command()
def competitors(
    week: int = typer.Argument(..., help="Week number"),
    name: str = typer.Argument(..., help="Competitor name"),
    file_path: Path = typer.Argument(..., help="Path to competitor picks JSON file"),
):
    """Track competitor picks for analysis."""
    try:
        if not file_path.exists():
            console.print(f"❌ File not found: {file_path}")
            raise typer.Exit(1)

        with open(file_path) as f:
            picks_data = json.load(f)

        system = PoolDominationSystem()
        system.track_competitor_picks(week, name, picks_data)

        console.print(f"✅ Competitor picks tracked for {name} in Week {week}")

    except Exception as e:
        console.print(f"❌ Error tracking competitor picks: {e}")
        raise typer.Exit(1)


@app.command()
def analyze():
    """Analyze competitor patterns and personal edges."""
    try:
        system = PoolDominationSystem()

        # Competitor patterns
        patterns = system.analyze_competitor_patterns()
        if patterns:
            console.print("🔍 Competitor Analysis:")
            for name, pattern in patterns.items():
                console.print(
                    f"  {name}: {pattern['strategy_type']} ({pattern['total_weeks']} weeks)"
                )

        # Personal edges
        edges = system.identify_personal_edges()
        if edges:
            console.print("\n🎯 Your Personal Edges:")
            console.print(f"  Strengths: {', '.join(edges.get('strengths', []))}")
            console.print(f"  Weaknesses: {', '.join(edges.get('weaknesses', []))}")

    except Exception as e:
        console.print(f"❌ Error analyzing patterns: {e}")
        raise typer.Exit(1)


@app.command()
def project():
    """Project season finish based on current performance."""
    try:
        system = PoolDominationSystem()
        projection = system.project_season_finish()

        console.print("🔮 Season Projection:")
        console.print(f"  Current Rank: {projection['current_rank']}/{projection['total_players']}")
        console.print(f"  Projected Final Rank: {projection['projected_final_rank']}")
        console.print(f"  Win Probability: {projection['win_probability']:.1f}%")
        console.print(f"  Expected Final Score: {projection['expected_final_score']:.1f}")

    except Exception as e:
        console.print(f"❌ Error projecting season: {e}")
        raise typer.Exit(1)


# Helper functions for display formatting


def _display_picks_table(picks: list[Pick], week: int):
    """Display picks in a formatted table."""
    table = Table(title=f"Week {week} Optimal Picks")
    table.add_column("Pts", style="cyan", justify="right")
    table.add_column("Game", style="white")
    table.add_column("Pick", style="green")
    table.add_column("Conf", style="yellow", justify="right")
    table.add_column("Strategy", style="blue")

    for pick in sorted(picks, key=lambda x: x.confidence_points, reverse=True):
        table.add_row(
            str(pick.confidence_points),
            pick.game,
            pick.predicted_winner,
            f"{pick.conf:.1f}%" if pick.conf else "N/A",
            pick.strategy_tag or "N/A",
        )

    console.print(table)


def _display_picks_csv(picks: list[Pick]):
    """Display picks in CSV format."""
    print("Game,Pick,Points")
    for pick in sorted(picks, key=lambda x: x.confidence_points, reverse=True):
        print(f"{pick.game},{pick.predicted_winner},{pick.confidence_points}")


def _display_picks_json(picks: list[Pick]):
    """Display picks in JSON format."""
    picks_data = []
    for pick in picks:
        picks_data.append(
            {
                "game": pick.game,
                "predicted_winner": pick.predicted_winner,
                "confidence_points": pick.confidence_points,
                "confidence": pick.conf,
                "strategy": pick.strategy_tag,
            }
        )

    console.print(json.dumps(picks_data, indent=2))


def _display_report_table(report_data: dict[str, Any], week: int):
    """Display weekly report in table format."""
    console.print(f"\n📊 Week {week} Performance Report")

    # Key metrics
    if "performance" in report_data:
        perf = report_data["performance"]
        table = Table(title="Performance Summary")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Weekly Score", str(perf.get("weekly_score", "N/A")))
        table.add_row("Correct Picks", str(perf.get("correct_picks", "N/A")))
        table.add_row("Win Rate", f"{perf.get('win_rate', 0):.1f}%")
        table.add_row("Strategy Used", perf.get("strategy_used", "N/A"))

        console.print(table)

    # Insights
    if "insights" in report_data:
        console.print("\n💡 Key Insights:")
        for insight in report_data["insights"]:
            console.print(f"  • {insight}")


@app.command()
def api_usage():
    """Check API usage and limits."""
    try:
        system = PoolDominationSystem()
        stats = system.usage_tracker.get_usage_stats()

        console.print("\n[bold blue]API Usage Statistics[/bold blue]")

        for api_name, data in stats.items():
            # Color coding based on usage percentage
            if data["percentage"] >= 90:
                color = "red"
                status = "🔴 CRITICAL"
            elif data["percentage"] >= 75:
                color = "yellow"
                status = "🟡 WARNING"
            elif data["percentage"] >= 50:
                color = "orange"
                status = "🟠 CAUTION"
            else:
                color = "green"
                status = "🟢 SAFE"

            console.print(f"\n[bold]{api_name.upper()}[/bold] - {status}")
            console.print(f"  Used: {data['used']}/{data['limit']} ({data['percentage']:.1f}%)")
            console.print(f"  Remaining: {data['remaining']}")
            console.print(f"  Current Month: {data['current_month']}")
            if data["last_reset"]:
                console.print(f"  Last Reset: {data['last_reset']}")

    except Exception as e:
        console.print(f"❌ Error checking API usage: {e}")
        raise typer.Exit(1)


@app.command()
def clear_cache():
    """Clear API cache files."""
    try:
        import glob
        from pathlib import Path

        # Find and remove cache files
        cache_files = glob.glob("cache_odds_week_*.json")
        cache_files.extend(glob.glob("api_usage.json"))

        removed_count = 0
        for cache_file in cache_files:
            try:
                Path(cache_file).unlink()
                removed_count += 1
                console.print(f"🗑️  Removed {cache_file}")
            except Exception as e:
                console.print(f"⚠️  Could not remove {cache_file}: {e}")

        if removed_count == 0:
            console.print("ℹ️  No cache files found to remove")
        else:
            console.print(f"✅ Removed {removed_count} cache files")

    except Exception as e:
        console.print(f"❌ Error clearing cache: {e}")
        raise typer.Exit(1)


@app.command()
def test_web_search(
    week: int = typer.Argument(..., help="Week number to test"),
    team: Optional[str] = typer.Option(
        None, "--team", "-t", help="Team to search for (e.g., KC, BALT)"
    ),
):
    """Test web search functionality."""
    try:
        system = PoolDominationSystem()

        if team:
            # Test team-specific search
            console.print(f"🔍 Testing web search for {team} in Week {week}")
            results = system.web_search.search_team_news(team, week)

            if results:
                console.print(f"✅ Found {len(results)} results for {team}")
                for i, result in enumerate(results[:3], 1):
                    console.print(f"{i}. {result.get('title', 'No title')}")
                    console.print(f"   {result.get('text', 'No content')[:100]}...")
            else:
                console.print(f"⚠️  No results found for {team}")
        else:
            # Test general web search context
            console.print(f"🔍 Testing web search context for Week {week}")
            context = system._get_web_search_context(week)

            if context:
                console.print("✅ Web search context generated:")
                console.print(Panel(context, title="Web Search Context", border_style="blue"))
            else:
                console.print("⚠️  No web search context generated")

        # Show cost summary
        cost_summary = system.web_search.web_search.get_cost_summary()
        console.print(
            f"\n💰 Cost Summary: ${cost_summary['total_cost']:.3f} ({cost_summary['searches_performed']} searches)"
        )

    except Exception as e:
        console.print(f"❌ Error testing web search: {e}")
        raise typer.Exit(1)


@app.command()
def analyze_llm(
    week: int = typer.Argument(..., help="Week number to analyze"),
    model: Optional[str] = typer.Option(
        None, "--model", "-m", help="Specific model to use (optional)"
    ),
    save: bool = typer.Option(True, "--save/--no-save", help="Save analysis to file"),
):
    """Get LLM analysis directly using OpenRouter models."""
    try:
        system = PoolDominationSystem()

        console.print(f"🤖 Getting LLM analysis for Week {week}")

        # Check if we have API key
        if not system.openrouter_api_key:
            console.print("❌ No OpenRouter API key found. Please set OPENROUTER_API_KEY in .env")
            raise typer.Exit(1)

        # Call OpenRouter API directly
        console.print("🚀 Calling OpenRouter API...")
        analysis = system.call_openrouter_api(week)

        if analysis:
            console.print("✅ LLM analysis completed!")

            # Display results
            console.print("\n📊 Analysis Results:")
            console.print(
                Panel(json.dumps(analysis, indent=2), title="LLM Analysis", border_style="green")
            )

            # Save to file if requested
            if save:
                filename = f"week_{week}_llm_analysis.json"
                with open(filename, "w") as f:
                    json.dump(analysis, f, indent=2)
                console.print(f"💾 Analysis saved to {filename}")

                # Also import into system
                console.print("📥 Importing analysis into system...")
                success = system.save_llm_data(week, analysis)
                if success:
                    console.print("✅ Analysis imported successfully!")
                else:
                    console.print("⚠️  Analysis saved but not imported")

            # Show API usage
            stats = system.usage_tracker.get_usage_stats()
            console.print(
                f"\n💰 API Usage: {stats['openrouter']['used']}/{stats['openrouter']['limit']} requests"
            )

        else:
            console.print("❌ Failed to get LLM analysis")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"❌ Error getting LLM analysis: {e}")
        raise typer.Exit(1)


@app.command()
def combine_analyses(
    week: int = typer.Argument(..., help="Week number to analyze"),
    automated: bool = typer.Option(
        True, "--automated/--no-automated", help="Run automated OpenRouter analysis"
    ),
    manual_files: Optional[list[str]] = typer.Option(
        None, "--manual", "-m", help="Path to manual LLM analysis file (can be used multiple times)"
    ),
    combine_method: str = typer.Option(
        "average", "--method", help="Combination method: average, weighted, or best"
    ),
):
    """Combine automated and manual LLM analyses for enhanced insights."""
    try:
        system = PoolDominationSystem()
        console.print(f"🔄 Combining analyses for Week {week}")

        analyses = []

        # Get automated analysis if requested
        if automated:
            if not system.openrouter_api_key:
                console.print("⚠️  No OpenRouter API key found. Skipping automated analysis.")
            else:
                console.print("🤖 Getting automated analysis...")
                auto_analysis = system.call_openrouter_api(week)
                if auto_analysis:
                    analyses.append(("automated", auto_analysis))
                    console.print("✅ Automated analysis completed!")
                else:
                    console.print("❌ Automated analysis failed")

        # Get manual analyses if provided
        if manual_files:
            for i, manual_file in enumerate(manual_files):
                if not os.path.exists(manual_file):
                    console.print(f"❌ Manual analysis file not found: {manual_file}")
                    raise typer.Exit(1)

                console.print(f"📁 Loading manual analysis {i+1} from {manual_file}...")
                with open(manual_file) as f:
                    manual_analysis = json.load(f)
                analyses.append((f"manual_{i+1}", manual_analysis))
                console.print(f"✅ Manual analysis {i+1} loaded!")

        if not analyses:
            console.print("❌ No analyses to combine. Use --automated and/or --manual")
            raise typer.Exit(1)

        # Combine analyses
        console.print(f"🔀 Combining {len(analyses)} analyses using {combine_method} method...")
        combined_analysis = system.combine_llm_analyses(analyses, method=combine_method)

        if combined_analysis:
            console.print("✅ Analyses combined successfully!")

            # Display combined results
            console.print("\n📊 Combined Analysis Results:")
            console.print(
                Panel(
                    json.dumps(combined_analysis, indent=2),
                    title="Combined Analysis",
                    border_style="blue",
                )
            )

            # Save combined analysis
            filename = f"week_{week}_combined_analysis.json"
            with open(filename, "w") as f:
                json.dump(combined_analysis, f, indent=2)
            console.print(f"💾 Combined analysis saved to {filename}")

            # Import into system
            console.print("📥 Importing combined analysis into system...")
            success = system.save_llm_data(week, combined_analysis)
            if success:
                console.print("✅ Combined analysis imported successfully!")
            else:
                console.print("⚠️  Combined analysis saved but not imported")

            # Show what was combined
            console.print("\n🔗 Combined analyses:")
            for name, _ in analyses:
                console.print(f"  - {name.title()}")

        else:
            console.print("❌ Failed to combine analyses")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"❌ Error combining analyses: {e}")
        raise typer.Exit(1)


@app.command()
def excel_prompt(
    date: str = typer.Argument(..., help="Date to analyze (e.g., '2024-09-18' or 'Week 3')"),
    enhanced: bool = typer.Option(
        False, "--enhanced", help="Include real odds data and web search context"
    ),
    force_refresh: bool = typer.Option(False, "--force-refresh", help="Force refresh of odds data"),
):
    """Generate LLM research prompt for the specified date."""
    try:
        system = PoolDominationSystem()

        if enhanced:
            console.print("🔗 Using enhanced prompt with odds data (cached if available)")
            prompt_text = system.get_enhanced_llm_prompt(date, force_refresh)
        else:
            console.print(f"📝 Generating basic research prompt for {date}")
            prompt_text = system.generate_llm_research_prompt_by_date(date)

        # Display the prompt
        console.print(Panel(prompt_text, title=f"{date} Research Prompt", border_style="blue"))

        # Save to data/prompts directory
        os.makedirs("data/prompts", exist_ok=True)
        safe_date = date.replace(" ", "_").replace("/", "-")
        filename = f"data/prompts/{safe_date}_prompt.txt"
        with open(filename, "w") as f:
            f.write(prompt_text)
        console.print(f"💾 Prompt saved to {filename}")

    except Exception as e:
        console.print(f"❌ Error generating prompt: {e}")
        raise typer.Exit(1)


@app.command()
def excel_update(
    week: int = typer.Argument(..., help="Week number (3-18)"),
    date: Optional[str] = typer.Option(
        None, "--date", "-d", help="Date suffix (e.g., '2024-09-18')"
    ),
    picks_file: Optional[str] = typer.Option(
        None, "--picks", "-p", help="JSON file with picks data"
    ),
    analysis_file: Optional[str] = typer.Option(
        None, "--analysis", "-a", help="Contrarian analysis JSON file"
    ),
    participant_name: str = typer.Option("Dawgpac", "--name", "-n", help="Participant name"),
):
    """Update Excel file with picks for the specified week."""
    try:
        excel = ExcelAutomation()

        # Load picks from file or generate them
        if analysis_file and os.path.exists(analysis_file):
            console.print(f"🎯 Loading contrarian analysis from {analysis_file}")
            picks = excel.load_contrarian_analysis(analysis_file)
            if not picks:
                console.print("❌ Failed to load contrarian analysis")
                raise typer.Exit(1)
            # Add week to each pick
            for pick in picks:
                pick["week"] = week
        elif picks_file and os.path.exists(picks_file):
            console.print(f"📁 Loading picks from {picks_file}")
            with open(picks_file) as f:
                picks_data = json.load(f)

            # Convert to the format expected by Excel automation
            picks = []
            if "picks" in picks_data:
                for pick in picks_data["picks"]:
                    picks.append(
                        {
                            "team": pick.get("team", ""),
                            "confidence": pick.get("confidence", 0),
                            "week": week,
                        }
                    )
            else:
                console.print("❌ Invalid picks file format")
                raise typer.Exit(1)
        else:
            # Generate picks using the system
            console.print(f"🎯 Generating picks for Week {week}")
            system = PoolDominationSystem()
            picks = system.generate_optimal_picks(week)

            # Convert Pick objects to dict format
            picks = [
                {"team": pick.predicted_winner, "confidence": pick.confidence_points, "week": week}
                for pick in picks
            ]

        # Convert team names to abbreviations
        picks = excel.convert_team_names(picks)

        # Validate picks
        validation = excel.validate_picks(picks)
        if not validation["valid"]:
            console.print("❌ Pick validation failed:")
            for error in validation["errors"]:
                console.print(f"  - {error}")
            raise typer.Exit(1)

        # Update Excel file
        console.print(f"📊 Updating Excel file for Week {week}")
        success = excel.update_picks(week, picks, date, participant_name)

        if success:
            console.print(f"✅ Excel file updated successfully for Week {week}")

            # Show summary
            summary = excel.create_submission_summary(week)
            console.print(Panel(summary, title="Picks Summary", border_style="green"))

            # Create backup
            backup_file = excel.backup_file(week)
            if backup_file:
                console.print(f"💾 Backup created: {backup_file}")
        else:
            console.print("❌ Failed to update Excel file")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"❌ Error updating Excel file: {e}")
        raise typer.Exit(1)


@app.command()
def excel_validate(
    week: int = typer.Argument(..., help="Week number (3-18)"),
    date: Optional[str] = typer.Option(
        None, "--date", "-d", help="Date suffix (e.g., '2024-09-18')"
    ),
):
    """Validate picks in Excel file for the specified week."""
    try:
        excel = ExcelAutomation()

        console.print(f"🔍 Validating picks for Week {week}")
        picks = excel.get_current_picks(week, date)

        if not picks:
            console.print("❌ No picks found for this week")
            raise typer.Exit(1)

        # Validate picks
        validation = excel.validate_picks(picks)

        if validation["valid"]:
            console.print("✅ All picks are valid!")
        else:
            console.print("❌ Validation failed:")
            for error in validation["errors"]:
                console.print(f"  - {error}")

        # Show current picks
        summary = excel.create_submission_summary(week)
        console.print(Panel(summary, title="Current Picks", border_style="blue"))

    except Exception as e:
        console.print(f"❌ Error validating Excel file: {e}")
        raise typer.Exit(1)


@app.command()
def excel_submit(
    week: int = typer.Argument(..., help="Week number (3-18)"),
    date: Optional[str] = typer.Option(
        None, "--date", "-d", help="Date suffix (e.g., '2024-09-18')"
    ),
    email: Optional[str] = typer.Option(None, "--email", "-e", help="Email address to send to"),
    subject: Optional[str] = typer.Option(None, "--subject", "-s", help="Email subject line"),
):
    """Prepare Excel file for submission."""
    try:
        excel = ExcelAutomation()

        console.print(f"📧 Preparing submission for Week {week}")

        # Validate picks first
        picks = excel.get_current_picks(week, date)
        if not picks:
            console.print("❌ No picks found for this week")
            raise typer.Exit(1)

        validation = excel.validate_picks(picks)
        if not validation["valid"]:
            console.print("❌ Picks validation failed. Please fix before submitting.")
            for error in validation["errors"]:
                console.print(f"  - {error}")
            raise typer.Exit(1)

        # Show submission summary
        summary = excel.create_submission_summary(week)
        console.print(Panel(summary, title="Submission Summary", border_style="green"))

        # Show file location
        if date:
            filename = f"Dawgpac25_{date}.xlsx"
        else:
            filename = f"Dawgpac25_Week{week}.xlsx"
        console.print(f"📁 Excel file: {filename}")

        if email:
            console.print(f"📧 Email: {email}")
            console.print("💡 Use your email client to attach the Excel file and send")
        else:
            console.print("💡 Attach the Excel file to your email and send to the pool organizer")

        if subject:
            console.print(f"📝 Suggested subject: {subject}")
        else:
            console.print(f"📝 Suggested subject: Week {week} Picks - Dawgpac")

    except Exception as e:
        console.print(f"❌ Error preparing submission: {e}")
        raise typer.Exit(1)


@app.command()
def auto_workflow(
    date: str = typer.Argument(..., help="Date for the week (YYYY-MM-DD format)"),
    week: int = typer.Argument(..., help="Week number (3-18)"),
    config_file: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to automation config file"
    ),
):
    """Run the complete automated weekly workflow."""
    try:
        console.print(f"🤖 Starting automated workflow for Week {week} ({date})")

        # Load configuration
        config = AutomationConfig()
        if config_file and os.path.exists(config_file):
            with open(config_file) as f:
                config_data = json.load(f)
                config = AutomationConfig(**config_data)

        # Initialize automation
        automation = WeeklyAutomation(config)

        # Run workflow
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Running automated workflow...", total=None)

            results = automation.run_weekly_workflow(date, week)

            progress.update(task, description="Workflow completed!")

        # Display results
        if results["status"] == "completed":
            console.print("✅ Automated workflow completed successfully!")

            # Show summary
            console.print("\n📊 Workflow Summary:")
            console.print(f"  - Week: {results['week']}")
            console.print(f"  - Date: {results['date']}")
            console.print(f"  - Monday: {results['monday']['picks_generated']} picks generated")
            console.print(f"  - Tuesday: {results['tuesday']['picks_optimized']} picks optimized")
            console.print(
                f"  - Wednesday: {'✅' if results['wednesday']['final_validation']['valid'] else '❌'} validation"
            )

            # Show Excel file
            excel_file = f"Dawgpac25_{date}.xlsx"
            if os.path.exists(excel_file):
                console.print(f"📁 Excel file: {excel_file}")
                console.print("💡 Ready for submission!")
            else:
                console.print("⚠️  Excel file not found")
        else:
            console.print(f"❌ Workflow failed: {results.get('error', 'Unknown error')}")
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"❌ Error running automated workflow: {e}")
        raise typer.Exit(1)


@app.command()
def create_config(output_file: str = typer.Argument(..., help="Output file for automation config")):
    """Create an automation configuration file."""
    try:
        config = AutomationConfig(
            auto_email=False,
            email_recipient="",
            smtp_server="",
            smtp_port=587,
            smtp_username="",
            smtp_password="",
            backup_enabled=True,
            notifications_enabled=True,
        )

        # Convert to dict for JSON serialization
        config_dict = {
            "auto_email": config.auto_email,
            "email_recipient": config.email_recipient,
            "smtp_server": config.smtp_server,
            "smtp_port": config.smtp_port,
            "smtp_username": config.smtp_username,
            "smtp_password": config.smtp_password,
            "backup_enabled": config.backup_enabled,
            "notifications_enabled": config.notifications_enabled,
        }

        with open(output_file, "w") as f:
            json.dump(config_dict, f, indent=2)

        console.print(f"✅ Configuration file created: {output_file}")
        console.print("💡 Edit the file to configure automation settings")

    except Exception as e:
        console.print(f"❌ Error creating configuration: {e}")
        raise typer.Exit(1)


@app.command()
def schedule_workflow(
    date: str = typer.Argument(..., help="Date for the week (YYYY-MM-DD format)"),
    week: int = typer.Argument(..., help="Week number (3-18)"),
    config_file: Optional[str] = typer.Option(
        None, "--config", "-c", help="Path to automation config file"
    ),
):
    """Schedule automated workflow for a specific week."""
    try:
        console.print(f"📅 Scheduling automated workflow for Week {week} ({date})")

        # Create cron job or scheduled task
        # This is a placeholder - would need to implement actual scheduling
        console.print("⚠️  Scheduling not yet implemented")
        console.print("💡 For now, run 'football-pool auto-workflow' manually")

    except Exception as e:
        console.print(f"❌ Error scheduling workflow: {e}")
        raise typer.Exit(1)


@app.command()
def logs(
    action: str = typer.Argument(
        "summary", help="Action: summary, tail, search, analyze-llm, analyze-api, clear"
    ),
    log_file: str = typer.Option(None, "--file", "-f", help="Log file name (for tail/search)"),
    query: str = typer.Option(None, "--query", "-q", help="Search query"),
    lines: int = typer.Option(50, "--lines", "-n", help="Number of lines to show"),
    confirm: bool = typer.Option(False, "--confirm", help="Confirm destructive actions"),
):
    """View and analyze log files."""
    try:
        viewer = LogViewer()

        if action == "summary":
            viewer.show_log_summary()
        elif action == "tail":
            if not log_file:
                console.print("❌ Log file required for tail action")
                raise typer.Exit(1)
            viewer.tail_log(log_file, lines)
        elif action == "search":
            if not query:
                console.print("❌ Query required for search action")
                raise typer.Exit(1)
            viewer.search_logs(query, log_file)
        elif action == "analyze-llm":
            viewer.analyze_llm_interactions()
        elif action == "analyze-api":
            viewer.analyze_api_usage()
        elif action == "clear":
            viewer.clear_logs(confirm)
        else:
            console.print(f"❌ Unknown action: {action}")
            console.print(
                "💡 Available actions: summary, tail, search, analyze-llm, analyze-api, clear"
            )
            raise typer.Exit(1)

    except Exception as e:
        console.print(f"❌ Error with logs command: {e}")
        raise typer.Exit(1)


@app.command()
def strategy_report(
    week: int = typer.Argument(..., help="Week number"),
    date: str = typer.Argument(..., help="Date (YYYY-MM-DD)"),
    analysis_file: str = typer.Option(
        None, "--analysis", "-a", help="Path to analysis JSON file"
    ),
    picks_file: str = typer.Option(
        None, "--picks", "-p", help="Path to picks JSON file"
    ),
    output_dir: str = typer.Option(
        "reports", "--output", "-o", help="Output directory for reports"
    ),
):
    """Generate comprehensive strategy report in markdown format."""
    try:
        from .report_generator import StrategyReportGenerator

        # Set default analysis file if not provided
        if not analysis_file:
            analysis_file = f"data/json/week_{week}_complete_contrarian_analysis.json"

        # Check if analysis file exists
        if not os.path.exists(analysis_file):
            console.print(f"❌ Analysis file not found: {analysis_file}")
            console.print("💡 Generate analysis first with: football-pool contrarian-prompt")
            raise typer.Exit(1)

        # Initialize report generator
        generator = StrategyReportGenerator()

        # Generate report
        console.print(f"📊 Generating strategy report for Week {week}...")
        report_path = generator.generate_weekly_strategy_report(
            week=week,
            date=date,
            analysis_file=analysis_file,
            picks_file=picks_file
        )

        console.print(f"✅ Strategy report generated: {report_path}")
        console.print(f"📁 Report saved to: {report_path}")

        # Show preview of report
        with open(report_path, 'r') as f:
            content = f.read()
            lines = content.split('\n')
            preview_lines = lines[:20]  # First 20 lines

        console.print("\n📋 Report Preview:")
        console.print(Panel('\n'.join(preview_lines), title="Strategy Report Preview", border_style="blue"))

        logger.log_command_end("strategy_report", success=True)

    except Exception as e:
        logger.log_error(e, f"strategy_report command for week {week}")
        console.print(f"❌ Error generating strategy report: {e}")
        raise typer.Exit(1)


@app.command()
def enhanced_report(
    week: int = typer.Argument(..., help="Week number"),
    date: str = typer.Argument(..., help="Date (YYYY-MM-DD)"),
    analysis_file: str = typer.Option(
        None, "--analysis", "-a", help="Path to analysis JSON file"
    ),
    use_llm: bool = typer.Option(
        True, "--llm/--no-llm", help="Use LLM for enhanced analysis"
    ),
):
    """Generate LLM-enhanced strategy report with next week considerations."""
    try:
        from .report_generator import StrategyReportGenerator

        # Set default analysis file if not provided
        if not analysis_file:
            analysis_file = f"data/json/week_{week}_complete_contrarian_analysis.json"

        # Check if analysis file exists
        if not os.path.exists(analysis_file):
            console.print(f"❌ Analysis file not found: {analysis_file}")
            console.print("💡 Generate analysis first with: football-pool contrarian-prompt")
            raise typer.Exit(1)

        # Initialize report generator
        generator = StrategyReportGenerator()

        # Get API key if LLM is requested
        openrouter_api_key = None
        if use_llm:
            openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
            if not openrouter_api_key:
                console.print("⚠️ OPENROUTER_API_KEY not found, generating standard report")
                use_llm = False

        # Generate enhanced report
        console.print(f"📊 Generating {'LLM-enhanced ' if use_llm else ''}strategy report for Week {week}...")

        if use_llm:
            report_content = generator.generate_llm_enhanced_report(
                week=week,
                date=date,
                analysis_file=analysis_file,
                openrouter_api_key=openrouter_api_key
            )
        else:
            report_content = generator._build_report_content(
                week=week,
                date=date,
                analysis_data=generator._load_analysis_data(analysis_file),
                picks_data=None
            )

        # Save report
        report_filename = f"Week_{week}_Enhanced_Strategy_Report_{date}.md"
        report_path = Path("reports") / report_filename
        report_path.parent.mkdir(exist_ok=True)

        with open(report_path, 'w') as f:
            f.write(report_content)

        console.print(f"✅ Enhanced strategy report generated: {report_path}")
        console.print(f"📁 Report saved to: {report_path}")

        # Show preview of report
        lines = report_content.split('\n')
        preview_lines = lines[:25]  # First 25 lines

        console.print("\n📋 Report Preview:")
        console.print(Panel('\n'.join(preview_lines), title="Enhanced Strategy Report Preview", border_style="green"))

        logger.log_command_end("enhanced_report", success=True)

    except Exception as e:
        logger.log_error(e, f"enhanced_report command for week {week}")
        console.print(f"❌ Error generating enhanced strategy report: {e}")
        raise typer.Exit(1)


@app.command()
def weekly_workflow(
    week: int = typer.Argument(..., help="Week number"),
    date: str = typer.Argument(..., help="Date (YYYY-MM-DD)"),
    use_llm: bool = typer.Option(
        True, "--llm/--no-llm", help="Use LLM for enhanced analysis"
    ),
    skip_picks: bool = typer.Option(
        False, "--skip-picks", help="Skip generating picks (use existing analysis)"
    ),
    analysis_file: str = typer.Option(
        None, "--analysis", "-a", help="Path to existing analysis JSON file"
    ),
):
    """🚀 COMPLETE WEEKLY WORKFLOW - Generate everything for the week in one command."""
    try:
        from .report_generator import StrategyReportGenerator

        console.print(f"🚀 Starting COMPLETE WEEKLY WORKFLOW for Week {week} ({date})")
        console.print("=" * 80)

        # Step 1: Generate contrarian prompt
        console.print("\n📝 Step 1: Generating contrarian analysis prompt...")
        try:
            from .core import PoolDominationSystem
            system = PoolDominationSystem()

            # Generate contrarian prompt
            prompt_text = system.generate_contrarian_analysis_prompt_by_date(date)

            # Save prompt
            os.makedirs("data/prompts", exist_ok=True)
            prompt_file = f"data/prompts/{date}_contrarian_prompt.txt"
            with open(prompt_file, "w") as f:
                f.write(prompt_text)

            console.print(f"✅ Contrarian prompt saved: {prompt_file}")
            console.print("💡 Copy this prompt to ChatGPT/Claude/Gemini and get JSON response")
            console.print("💡 Save the JSON response as: data/json/week_{week}_complete_contrarian_analysis.json")

        except Exception as e:
            console.print(f"⚠️ Warning: Could not generate contrarian prompt: {e}")

        # Step 2: Check for analysis file
        if not analysis_file:
            analysis_file = f"data/json/week_{week}_complete_contrarian_analysis.json"

        if not os.path.exists(analysis_file):
            console.print(f"\n⚠️ Analysis file not found: {analysis_file}")
            console.print("📋 MANUAL STEP REQUIRED:")
            console.print("1. Copy the contrarian prompt from data/prompts/")
            console.print("2. Paste into ChatGPT/Claude/Gemini")
            console.print("3. Get JSON response and save as the analysis file")
            console.print("4. Run this command again with --analysis path/to/your/analysis.json")
            console.print("\n🔄 Continuing with standard picks generation...")

            # Generate standard picks as fallback
            if not skip_picks:
                console.print("\n📊 Step 2: Generating standard picks...")
                try:
                    from .core import PoolDominationSystem
                    system = PoolDominationSystem()

                    # Generate picks
                    picks = system.generate_optimal_picks(week)
                    console.print("✅ Standard picks generated")

                except Exception as e:
                    console.print(f"⚠️ Warning: Could not generate standard picks: {e}")

            console.print("\n📋 WORKFLOW INCOMPLETE - Manual step required")
            console.print("💡 Run again after saving your analysis JSON file")
            return

        # Step 3: Update Excel with analysis
        console.print(f"\n📊 Step 2: Updating Excel with contrarian analysis...")
        try:
            from .excel_automation import ExcelAutomation
            excel = ExcelAutomation()

            # Update Excel with contrarian analysis
            success = excel.update_picks(week, [], date)
            if success:
                console.print(f"✅ Excel file updated: data/excel/Dawgpac25_{date}.xlsx")
            else:
                console.print("⚠️ Warning: Excel update failed")

        except Exception as e:
            console.print(f"⚠️ Warning: Could not update Excel: {e}")

        # Step 4: Generate strategy report
        console.print(f"\n📋 Step 3: Generating strategy report...")
        try:
            generator = StrategyReportGenerator()

            # Generate enhanced report
            if use_llm and os.getenv("OPENROUTER_API_KEY"):
                report_content = generator.generate_llm_enhanced_report(
                    week=week,
                    date=date,
                    analysis_file=analysis_file,
                    openrouter_api_key=os.getenv("OPENROUTER_API_KEY")
                )
                report_filename = f"Week_{week}_Enhanced_Strategy_Report_{date}.md"
            else:
                report_content = generator._build_report_content(
                    week=week,
                    date=date,
                    analysis_data=generator._load_analysis_data(analysis_file),
                    picks_data=None
                )
                report_filename = f"Week_{week}_Strategy_Report_{date}.md"

            # Save report
            report_path = Path("reports") / report_filename
            report_path.parent.mkdir(exist_ok=True)

            with open(report_path, 'w') as f:
                f.write(report_content)

            console.print(f"✅ Strategy report generated: {report_path}")

        except Exception as e:
            console.print(f"⚠️ Warning: Could not generate strategy report: {e}")

        # Step 5: Generate next week preview
        console.print(f"\n🔍 Step 4: Generating next week preview...")
        try:
            next_week_date = (datetime.strptime(date, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")
            preview_content = generator.generate_next_week_preview(week, date)

            preview_filename = f"Week_{week+1}_Preview_{next_week_date}.md"
            preview_path = Path("reports") / preview_filename
            preview_path.parent.mkdir(exist_ok=True)

            with open(preview_path, 'w') as f:
                f.write(preview_content)

            console.print(f"✅ Next week preview generated: {preview_path}")

        except Exception as e:
            console.print(f"⚠️ Warning: Could not generate next week preview: {e}")

        # Step 6: Summary
        console.print("\n" + "=" * 80)
        console.print("🎯 WEEKLY WORKFLOW COMPLETE!")
        console.print("=" * 80)

        # Show generated files
        console.print("\n📁 Generated Files:")
        console.print(f"  📝 Contrarian Prompt: data/prompts/{date}_contrarian_prompt.txt")
        console.print(f"  📊 Excel File: data/excel/Dawgpac25_{date}.xlsx")
        console.print(f"  📋 Strategy Report: reports/{report_filename}")
        console.print(f"  🔍 Next Week Preview: reports/Week_{week+1}_Preview_{next_week_date}.md")

        # Show next steps
        console.print("\n🚀 Next Steps:")
        console.print("1. Review the strategy report for your picks")
        console.print("2. Submit the Excel file to your pool")
        console.print("3. Use the next week preview for future planning")
        console.print("4. Track results and refine strategy")

        # Show competitive edge
        console.print("\n💰 Competitive Edge:")
        console.print("✅ Contrarian analysis for differentiation")
        console.print("✅ Value plays for maximum earnings")
        console.print("✅ Risk management with confidence points")
        console.print("✅ Future planning with next week insights")

        logger.log_command_end("weekly_workflow", success=True)

    except Exception as e:
        logger.log_error(e, f"weekly_workflow command for week {week}")
        console.print(f"❌ Error in weekly workflow: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
