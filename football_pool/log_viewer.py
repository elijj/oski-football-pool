"""
Log Viewer Utility for Football Pool Domination System.

Provides tools to view, analyze, and search through log files.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table


class LogViewer:
    """Utility for viewing and analyzing log files."""

    def __init__(self, log_dir: str = "logs"):
        """Initialize the log viewer."""
        self.log_dir = Path(log_dir)
        self.console = Console()

    def list_log_files(self) -> list[dict[str, Any]]:
        """List all available log files with metadata."""
        if not self.log_dir.exists():
            return []

        log_files = []
        for log_file in self.log_dir.glob("*.log"):
            stat = log_file.stat()
            log_files.append(
                {
                    "name": log_file.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime),
                    "path": str(log_file),
                }
            )

        return sorted(log_files, key=lambda x: x["modified"], reverse=True)

    def show_log_summary(self):
        """Display a summary of all log files."""
        log_files = self.list_log_files()

        if not log_files:
            self.console.print("📁 No log files found in logs/ directory")
            return

        table = Table(title="📊 Log Files Summary")
        table.add_column("File", style="cyan")
        table.add_column("Size", style="green")
        table.add_column("Modified", style="yellow")
        table.add_column("Path", style="dim")

        total_size = 0
        for log_file in log_files:
            size_mb = log_file["size"] / (1024 * 1024)
            total_size += log_file["size"]
            table.add_row(
                log_file["name"],
                f"{size_mb:.2f} MB",
                log_file["modified"].strftime("%Y-%m-%d %H:%M:%S"),
                log_file["path"],
            )

        self.console.print(table)
        self.console.print(f"\n📈 Total log size: {total_size / (1024 * 1024):.2f} MB")

    def tail_log(self, log_file: str, lines: int = 50):
        """Show the last N lines of a log file."""
        log_path = self.log_dir / log_file
        if not log_path.exists():
            self.console.print(f"❌ Log file not found: {log_file}")
            return

        try:
            with open(log_path, encoding="utf-8") as f:
                all_lines = f.readlines()
                tail_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines

                self.console.print(
                    Panel(
                        "".join(tail_lines),
                        title=f"📄 Last {len(tail_lines)} lines of {log_file}",
                        border_style="blue",
                    )
                )
        except Exception as e:
            self.console.print(f"❌ Error reading log file: {e}")

    def search_logs(self, query: str, log_file: Optional[str] = None, case_sensitive: bool = False):
        """Search for a query in log files."""
        search_files = [self.log_dir / log_file] if log_file else list(self.log_dir.glob("*.log"))
        results = []

        for log_path in search_files:
            if not log_path.exists():
                continue

            try:
                with open(log_path, encoding="utf-8") as f:
                    for line_num, line in enumerate(f, 1):
                        search_line = line if case_sensitive else line.lower()
                        search_query = query if case_sensitive else query.lower()

                        if search_query in search_line:
                            results.append(
                                {
                                    "file": log_path.name,
                                    "line": line_num,
                                    "content": line.strip(),
                                    "timestamp": self._extract_timestamp(line),
                                }
                            )
            except Exception as e:
                self.console.print(f"❌ Error reading {log_path.name}: {e}")

        if not results:
            self.console.print(f"🔍 No results found for query: '{query}'")
            return

        # Display results
        table = Table(title=f"🔍 Search Results for '{query}'")
        table.add_column("File", style="cyan")
        table.add_column("Line", style="green")
        table.add_column("Timestamp", style="yellow")
        table.add_column("Content", style="white")

        for result in results[:20]:  # Limit to 20 results
            table.add_row(
                result["file"],
                str(result["line"]),
                result["timestamp"] or "N/A",
                result["content"][:100] + "..."
                if len(result["content"]) > 100
                else result["content"],
            )

        self.console.print(table)
        if len(results) > 20:
            self.console.print(f"\n📊 Showing first 20 of {len(results)} results")

    def analyze_llm_interactions(self):
        """Analyze LLM interaction patterns from logs."""
        llm_log = self.log_dir / "llm_interactions.log"
        if not llm_log.exists():
            self.console.print("❌ No LLM interaction log found")
            return

        try:
            with open(llm_log, encoding="utf-8") as f:
                lines = f.readlines()

            # Analyze patterns
            requests = [line for line in lines if "LLM Request" in line]
            responses = [line for line in lines if "LLM Response" in line]
            errors = [line for line in lines if "ERROR" in line or "WARNING" in line]

            self.console.print(
                Panel(
                    f"🤖 LLM Interactions Analysis\n\n"
                    f"📤 Total Requests: {len(requests)}\n"
                    f"📥 Total Responses: {len(responses)}\n"
                    f"❌ Errors/Warnings: {len(errors)}\n"
                    f"📊 Success Rate: {len(responses)/len(requests)*100:.1f}%"
                    if requests
                    else "N/A",
                    title="LLM Analysis",
                    border_style="green",
                )
            )

        except Exception as e:
            self.console.print(f"❌ Error analyzing LLM logs: {e}")

    def analyze_api_usage(self):
        """Analyze API usage patterns from logs."""
        api_log = self.log_dir / "api_calls.log"
        if not api_log.exists():
            self.console.print("❌ No API call log found")
            return

        try:
            with open(api_log, encoding="utf-8") as f:
                lines = f.readlines()

            # Count API calls by service
            services = {}
            total_calls = 0

            for line in lines:
                if "API Call:" in line:
                    total_calls += 1
                    # Extract service name
                    if "OpenRouter" in line:
                        services["OpenRouter"] = services.get("OpenRouter", 0) + 1
                    elif "Odds" in line:
                        services["The Odds API"] = services.get("The Odds API", 0) + 1
                    elif "Exa" in line:
                        services["Exa"] = services.get("Exa", 0) + 1

            self.console.print(
                Panel(
                    f"🌐 API Usage Analysis\n\n"
                    f"📊 Total API Calls: {total_calls}\n\n"
                    + "\n".join(
                        [f"• {service}: {count} calls" for service, count in services.items()]
                    ),
                    title="API Analysis",
                    border_style="blue",
                )
            )

        except Exception as e:
            self.console.print(f"❌ Error analyzing API logs: {e}")

    def _extract_timestamp(self, line: str) -> Optional[str]:
        """Extract timestamp from log line."""
        try:
            # Look for timestamp pattern: YYYY-MM-DD HH:MM:SS
            import re

            match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", line)
            return match.group(1) if match else None
        except:
            return None

    def clear_logs(self, confirm: bool = False):
        """Clear all log files."""
        if not confirm:
            self.console.print("⚠️  This will delete all log files. Use --confirm to proceed.")
            return

        try:
            for log_file in self.log_dir.glob("*.log"):
                log_file.unlink()
            self.console.print("✅ All log files cleared")
        except Exception as e:
            self.console.print(f"❌ Error clearing logs: {e}")


def main():
    """CLI for log viewer."""
    import typer

    app = typer.Typer()
    viewer = LogViewer()

    @app.command()
    def summary():
        """Show log files summary."""
        viewer.show_log_summary()

    @app.command()
    def tail(log_file: str, lines: int = 50):
        """Show last N lines of a log file."""
        viewer.tail_log(log_file, lines)

    @app.command()
    def search(query: str, log_file: str = None, case_sensitive: bool = False):
        """Search for query in log files."""
        viewer.search_logs(query, log_file, case_sensitive)

    @app.command()
    def analyze_llm():
        """Analyze LLM interaction patterns."""
        viewer.analyze_llm_interactions()

    @app.command()
    def analyze_api():
        """Analyze API usage patterns."""
        viewer.analyze_api_usage()

    @app.command()
    def clear(confirm: bool = False):
        """Clear all log files."""
        viewer.clear_logs(confirm)

    app()


if __name__ == "__main__":
    main()
