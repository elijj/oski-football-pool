"""
Database management for the Football Pool Domination System.

Handles SQLite database operations, schema management, and migrations.
"""

import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from .models import CompetitorPick, Pick, StrategyPerformance

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database operations and migrations."""

    def __init__(self, db_path: str = "pool_tracker.db"):
        self.db_path = Path(db_path)
        self.init_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable dict-like access
        try:
            yield conn
        finally:
            conn.close()

    def init_database(self):
        """Initialize database with schema and run migrations."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Create schema version table
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY,
                    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Get current schema version
            cursor.execute("SELECT MAX(version) FROM schema_version")
            current_version = cursor.fetchone()[0] or 0

            # Run migrations
            self._run_migrations(conn, current_version)

            conn.commit()

    def _run_migrations(self, conn: sqlite3.Connection, current_version: int):
        """Run database migrations."""
        migrations = [
            self._migration_001_initial_schema,
            self._migration_002_add_indexes,
            self._migration_003_add_competitor_analysis,
        ]

        for i, migration in enumerate(migrations, 1):
            if i > current_version:
                logger.info(f"Running migration {i}")
                migration(conn)
                conn.execute("INSERT INTO schema_version (version) VALUES (?)", (i,))

    def _migration_001_initial_schema(self, conn: sqlite3.Connection):
        """Initial database schema."""
        cursor = conn.cursor()

        # Picks table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS picks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER NOT NULL,
                game TEXT NOT NULL,
                predicted_winner TEXT NOT NULL,
                confidence_points INTEGER NOT NULL,
                conf REAL,
                strategy_tag TEXT,
                spread REAL,
                public_pct REAL,
                actual_winner TEXT,
                hit BOOLEAN,
                points_earned INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Results table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER NOT NULL,
                game TEXT NOT NULL,
                winner TEXT NOT NULL,
                score_home INTEGER,
                score_away INTEGER,
                spread_result REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Strategies table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS strategies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER NOT NULL,
                strategy_name TEXT NOT NULL,
                variance_level TEXT NOT NULL,
                pool_position_rank INTEGER,
                pool_position_total INTEGER,
                weekly_score INTEGER,
                cumulative_score INTEGER,
                success_rate REAL,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Competitors table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS competitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER NOT NULL,
                competitor_name TEXT NOT NULL,
                game TEXT NOT NULL,
                pick TEXT NOT NULL,
                points INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # LLM data table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS llm_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER NOT NULL,
                data_json TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

    def _migration_002_add_indexes(self, conn: sqlite3.Connection):
        """Add database indexes for performance."""
        cursor = conn.cursor()

        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_picks_week ON picks(week)",
            "CREATE INDEX IF NOT EXISTS idx_picks_game ON picks(game)",
            "CREATE INDEX IF NOT EXISTS idx_results_week ON results(week)",
            "CREATE INDEX IF NOT EXISTS idx_strategies_week ON strategies(week)",
            "CREATE INDEX IF NOT EXISTS idx_competitors_week ON competitors(week)",
            "CREATE INDEX IF NOT EXISTS idx_competitors_name ON competitors(competitor_name)",
            "CREATE INDEX IF NOT EXISTS idx_llm_data_week ON llm_data(week)",
        ]

        for index_sql in indexes:
            cursor.execute(index_sql)

    def _migration_003_add_competitor_analysis(self, conn: sqlite3.Connection):
        """Add competitor analysis tables."""
        cursor = conn.cursor()

        # Competitor patterns table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS competitor_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                competitor_name TEXT NOT NULL,
                pattern_type TEXT NOT NULL,
                pattern_data TEXT NOT NULL,
                confidence REAL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Weekly reports table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS weekly_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER NOT NULL,
                report_json TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

    # ============= PICKS OPERATIONS =============

    def save_picks(self, picks: list[Pick]) -> bool:
        """Save picks to database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                for pick in picks:
                    cursor.execute(
                        """
                        INSERT INTO picks (
                            week, game, predicted_winner, confidence_points,
                            conf, strategy_tag, spread, public_pct
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            pick.week,
                            pick.game,
                            pick.predicted_winner,
                            pick.confidence_points,
                            pick.conf,
                            pick.strategy_tag,
                            pick.spread,
                            pick.public_pct,
                        ),
                    )

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving picks: {e}")
            return False

    def get_picks(self, week: Optional[int] = None) -> list[Pick]:
        """Get picks from database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            if week:
                cursor.execute(
                    "SELECT * FROM picks WHERE week = ? ORDER BY confidence_points DESC", (week,)
                )
            else:
                cursor.execute("SELECT * FROM picks ORDER BY week DESC, confidence_points DESC")

            rows = cursor.fetchall()
            picks = []

            for row in rows:
                pick = Pick(
                    game=row["game"],
                    predicted_winner=row["predicted_winner"],
                    confidence_points=row["confidence_points"],
                    conf=row["conf"],
                    strategy_tag=row["strategy_tag"],
                    week=row["week"],
                    spread=row["spread"],
                    public_pct=row["public_pct"],
                    actual_winner=row["actual_winner"],
                    hit=bool(row["hit"]) if row["hit"] is not None else None,
                    points_earned=row["points_earned"],
                )
                picks.append(pick)

            return picks

    def update_pick_results(self, week: int, results: dict[str, str]) -> bool:
        """Update picks with actual results."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                for game, winner in results.items():
                    # Save game result
                    cursor.execute(
                        """
                        INSERT OR REPLACE INTO results (week, game, winner)
                        VALUES (?, ?, ?)
                    """,
                        (week, game, winner),
                    )

                    # Update picks
                    cursor.execute(
                        """
                        UPDATE picks
                        SET actual_winner = ?,
                            hit = (predicted_winner = ?),
                            points_earned = CASE
                                WHEN predicted_winner = ? THEN confidence_points
                                ELSE 0
                            END,
                            updated_at = CURRENT_TIMESTAMP
                        WHERE week = ? AND game = ?
                    """,
                        (winner, winner, winner, week, game),
                    )

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error updating pick results: {e}")
            return False

    # ============= COMPETITOR OPERATIONS =============

    def save_competitor_picks(
        self, week: int, competitor_name: str, picks: list[dict[str, Any]]
    ) -> bool:
        """Save competitor picks."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                for pick_data in picks:
                    cursor.execute(
                        """
                        INSERT INTO competitors (week, competitor_name, game, pick, points)
                        VALUES (?, ?, ?, ?, ?)
                    """,
                        (
                            week,
                            competitor_name,
                            pick_data["game"],
                            pick_data["pick"],
                            pick_data["points"],
                        ),
                    )

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving competitor picks: {e}")
            return False

    def get_competitor_picks(
        self, week: Optional[int] = None, competitor: Optional[str] = None
    ) -> list[CompetitorPick]:
        """Get competitor picks."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM competitors WHERE 1=1"
            params = []

            if week:
                query += " AND week = ?"
                params.append(week)

            if competitor:
                query += " AND competitor_name = ?"
                params.append(competitor)

            query += " ORDER BY week DESC, competitor_name, points DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()

            picks = []
            for row in rows:
                pick = CompetitorPick(
                    week=row["week"],
                    competitor_name=row["competitor_name"],
                    game=row["game"],
                    pick=row["pick"],
                    points=row["points"],
                    timestamp=datetime.fromisoformat(row["created_at"]),
                )
                picks.append(pick)

            return picks

    # ============= STRATEGY OPERATIONS =============

    def save_strategy_performance(self, performance: StrategyPerformance) -> bool:
        """Save strategy performance data."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO strategies (
                        week, strategy_name, variance_level, pool_position_rank,
                        pool_position_total, weekly_score, cumulative_score,
                        success_rate, notes
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        performance.week,
                        performance.strategy_name,
                        performance.variance_level,
                        performance.pool_position_rank,
                        performance.pool_position_total,
                        performance.weekly_score,
                        performance.cumulative_score,
                        performance.success_rate,
                        performance.notes,
                    ),
                )

                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving strategy performance: {e}")
            return False

    def get_strategy_performance(self, week: Optional[int] = None) -> list[StrategyPerformance]:
        """Get strategy performance data."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            if week:
                cursor.execute("SELECT * FROM strategies WHERE week = ?", (week,))
            else:
                cursor.execute("SELECT * FROM strategies ORDER BY week DESC")

            rows = cursor.fetchall()
            performances = []

            for row in rows:
                performance = StrategyPerformance(
                    strategy_name=row["strategy_name"],
                    week=row["week"],
                    variance_level=row["variance_level"],
                    pool_position_rank=row["pool_position_rank"],
                    pool_position_total=row["pool_position_total"],
                    weekly_score=row["weekly_score"],
                    cumulative_score=row["cumulative_score"],
                    success_rate=row["success_rate"],
                    notes=row["notes"],
                    timestamp=datetime.fromisoformat(row["created_at"]),
                )
                performances.append(performance)

            return performances

    # ============= ANALYTICS =============

    def get_performance_stats(self) -> dict[str, Any]:
        """Get overall performance statistics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Overall stats
            cursor.execute(
                """
                SELECT
                    COUNT(*) as total_picks,
                    SUM(CASE WHEN hit = 1 THEN 1 ELSE 0 END) as correct_picks,
                    SUM(points_earned) as total_points,
                    AVG(CASE WHEN hit = 1 THEN confidence_points ELSE NULL END) as avg_correct_confidence,
                    AVG(CASE WHEN hit = 0 THEN confidence_points ELSE NULL END) as avg_wrong_confidence
                FROM picks
                WHERE actual_winner IS NOT NULL
            """
            )

            row = cursor.fetchone()
            stats = {
                "total_picks": row["total_picks"] or 0,
                "correct_picks": row["correct_picks"] or 0,
                "total_points": row["total_points"] or 0,
                "avg_correct_confidence": row["avg_correct_confidence"] or 0,
                "avg_wrong_confidence": row["avg_wrong_confidence"] or 0,
                "win_rate": (row["correct_picks"] / row["total_picks"] * 100)
                if row["total_picks"]
                else 0,
            }

            # Strategy performance
            cursor.execute(
                """
                SELECT
                    strategy_tag,
                    COUNT(*) as uses,
                    SUM(CASE WHEN hit = 1 THEN 1 ELSE 0 END) as wins,
                    AVG(points_earned) as avg_points
                FROM picks
                WHERE actual_winner IS NOT NULL AND strategy_tag IS NOT NULL
                GROUP BY strategy_tag
            """
            )

            strategy_stats = {}
            for row in cursor.fetchall():
                strategy_stats[row["strategy_tag"]] = {
                    "uses": row["uses"],
                    "wins": row["wins"],
                    "win_rate": (row["wins"] / row["uses"] * 100) if row["uses"] else 0,
                    "avg_points": row["avg_points"] or 0,
                }

            stats["strategy_performance"] = strategy_stats

            return stats

    def get_competitor_patterns(self) -> dict[str, Any]:
        """Analyze competitor patterns."""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    competitor_name,
                    COUNT(DISTINCT week) as total_weeks,
                    AVG(points) as avg_points,
                    COUNT(*) as total_picks,
                    SUM(CASE WHEN points >= 15 THEN 1 ELSE 0 END) as high_confidence_picks,
                    SUM(CASE WHEN points <= 5 THEN 1 ELSE 0 END) as low_confidence_picks
                FROM competitors
                GROUP BY competitor_name
            """
            )

            patterns = {}
            for row in cursor.fetchall():
                patterns[row["competitor_name"]] = {
                    "total_weeks": row["total_weeks"],
                    "avg_points": row["avg_points"] or 0,
                    "total_picks": row["total_picks"],
                    "high_confidence_picks": row["high_confidence_picks"],
                    "low_confidence_picks": row["low_confidence_picks"],
                    "strategy_type": self._classify_competitor_strategy(row),
                }

            return patterns

    def _classify_competitor_strategy(self, row) -> str:
        """Classify competitor strategy based on patterns."""
        high_conf_ratio = (
            row["high_confidence_picks"] / row["total_picks"] if row["total_picks"] else 0
        )
        low_conf_ratio = (
            row["low_confidence_picks"] / row["total_picks"] if row["total_picks"] else 0
        )

        if high_conf_ratio > 0.4:
            return "aggressive"
        elif low_conf_ratio > 0.3:
            return "conservative"
        else:
            return "balanced"
