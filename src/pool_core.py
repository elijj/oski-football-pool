"""
pool_core.py - Core Football Pool System
Handles database, tracking, and base functionality
"""

import json
import logging
import sqlite3
from collections import defaultdict
from dataclasses import dataclass

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class GamePick:
    """Data class for tracking individual game picks"""

    game: str
    week: int
    confidence_points: int
    predicted_winner: str
    actual_winner: str = None
    spread: float = 0
    public_pct: float = 50
    strategy_used: str = ""
    confidence_score: float = 50
    hit: bool = None
    points_earned: int = 0


class PoolDatabase:
    """Handles all database operations"""

    def __init__(self, db_path: str = "pool_tracker.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for tracking everything"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create tables
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS picks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER,
                game TEXT,
                confidence_points INTEGER,
                predicted_winner TEXT,
                actual_winner TEXT,
                spread REAL,
                public_pct REAL,
                strategy_used TEXT,
                confidence_score REAL,
                hit BOOLEAN,
                points_earned INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS strategies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER,
                strategy_name TEXT,
                variance_level TEXT,
                pool_position_rank INTEGER,
                pool_position_total INTEGER,
                weekly_score INTEGER,
                cumulative_score INTEGER,
                success_rate REAL,
                notes TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS competitors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER,
                competitor_name TEXT,
                picks_data TEXT,
                weekly_score INTEGER,
                cumulative_score INTEGER,
                strategy_detected TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS game_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week INTEGER,
                game TEXT,
                winner TEXT,
                score_home INTEGER,
                score_away INTEGER,
                spread_result REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        conn.commit()
        conn.close()

    def save_picks(self, picks: list[GamePick]) -> bool:
        """Save picks to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            for pick in picks:
                cursor.execute(
                    """
                    INSERT INTO picks (week, game, confidence_points, predicted_winner,
                                     spread, public_pct, strategy_used, confidence_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        pick.week,
                        pick.game,
                        pick.confidence_points,
                        pick.predicted_winner,
                        pick.spread,
                        pick.public_pct,
                        pick.strategy_used,
                        pick.confidence_score,
                    ),
                )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error saving picks: {e}")
            return False

    def save_competitor_picks(
        self, week: int, competitor_name: str, picks: list[dict], weekly_score: int = 0
    ) -> bool:
        """Save competitor picks for pattern analysis"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            picks_json = json.dumps(picks)
            cursor.execute(
                """
                INSERT INTO competitors (week, competitor_name, picks_data, weekly_score)
                VALUES (?, ?, ?, ?)
            """,
                (week, competitor_name, picks_json, weekly_score),
            )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error saving competitor picks: {e}")
            return False

    def update_results(self, week: int, results: dict[str, str]) -> bool:
        """Update game results and calculate scores"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Save game results
            for game, winner in results.items():
                cursor.execute(
                    """
                    INSERT INTO game_results (week, game, winner)
                    VALUES (?, ?, ?)
                """,
                    (week, game, winner),
                )

                # Update picks with results
                cursor.execute(
                    """
                    UPDATE picks
                    SET actual_winner = ?,
                        hit = (predicted_winner = ?),
                        points_earned = CASE
                            WHEN predicted_winner = ? THEN confidence_points
                            ELSE 0
                        END
                    WHERE week = ? AND game = ?
                """,
                    (winner, winner, winner, week, game),
                )

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error updating results: {e}")
            return False

    def get_performance_stats(self) -> dict:
        """Get overall performance statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Overall stats
        cursor.execute(
            """
            SELECT
                COUNT(*) as total_picks,
                SUM(hit) as correct_picks,
                SUM(points_earned) as total_points,
                AVG(CASE WHEN hit = 1 THEN confidence_points ELSE NULL END) as avg_correct_confidence,
                AVG(CASE WHEN hit = 0 THEN confidence_points ELSE NULL END) as avg_wrong_confidence
            FROM picks WHERE actual_winner IS NOT NULL
        """
        )

        row = cursor.fetchone()
        stats = {
            "total_picks": row[0] or 0,
            "correct_picks": row[1] or 0,
            "total_points": row[2] or 0,
            "avg_correct_confidence": row[3] or 0,
            "avg_wrong_confidence": row[4] or 0,
            "win_rate": (row[1] / row[0] * 100) if row[0] else 0,
        }

        # Strategy performance
        cursor.execute(
            """
            SELECT
                strategy_used,
                COUNT(*) as uses,
                SUM(hit) as wins,
                AVG(points_earned) as avg_points
            FROM picks
            WHERE actual_winner IS NOT NULL AND strategy_used != ''
            GROUP BY strategy_used
        """
        )

        strategy_stats = {}
        for row in cursor.fetchall():
            strategy_stats[row[0]] = {
                "uses": row[1],
                "wins": row[2],
                "win_rate": (row[2] / row[1] * 100) if row[1] else 0,
                "avg_points": row[3] or 0,
            }

        stats["strategy_performance"] = strategy_stats

        conn.close()
        return stats

    def get_competitor_patterns(self) -> dict:
        """Analyze competitor picking patterns"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT competitor_name, picks_data, weekly_score
            FROM competitors
            ORDER BY week
        """
        )

        patterns = defaultdict(
            lambda: {
                "total_weeks": 0,
                "avg_score": 0,
                "total_score": 0,
                "pick_tendencies": defaultdict(int),
            }
        )

        for row in cursor.fetchall():
            name = row[0]
            picks = json.loads(row[1]) if row[1] else []
            score = row[2] or 0

            patterns[name]["total_weeks"] += 1
            patterns[name]["total_score"] += score

            # Analyze pick tendencies
            for pick in picks:
                if pick.get("points", 0) >= 15:
                    patterns[name]["pick_tendencies"]["high_confidence"] += 1
                elif pick.get("points", 0) <= 5:
                    patterns[name]["pick_tendencies"]["low_confidence"] += 1

        # Calculate averages
        for name, data in patterns.items():
            if data["total_weeks"] > 0:
                data["avg_score"] = data["total_score"] / data["total_weeks"]

        conn.close()
        return dict(patterns)


class ScheduleManager:
    """Manages the complete season schedule"""

    @staticmethod
    def get_schedule() -> dict:
        """Returns the complete 2025-2026 schedule"""
        return {
            1: {"dates": "9/4-9/8", "games": ["BYE", "BYE"]},
            2: {"dates": "9/11-9/15", "games": ["BYE", "BYE"]},
            3: {
                "dates": "9/18-9/22",
                "games": [
                    "CAL@SDSU",
                    "STAN@VA",
                    "UW@WSU",
                    "FLA@Mia,F",
                    "MIA@BUFF",
                    "ATL@CAR",
                    "GB@CLEV",
                    "HOU@JAC",
                    "CINC@MINN",
                    "PITT@NE",
                    "LAR@PHIL",
                    "NYJ@TB",
                    "IND@TENN",
                    "LV@WASH",
                    "DEN@LAC",
                    "NO@SEA",
                    "DAL@CHI",
                    "ARIZ@SF",
                    "KC@NYG",
                    "DET@BALT",
                ],
            },
            4: {
                "dates": "9/25-9/29",
                "games": [
                    "CAL@BC",
                    "SJSU@STAN",
                    "ORE@PSU",
                    "ALA@GEO",
                    "SEA@ARIZ",
                    "MINN@PITT",
                    "WASH@ATL",
                    "NO@BUFF",
                    "CLEV@DET",
                    "TENN@HOU",
                    "CAR@NE",
                    "LAC@NYG",
                    "PHIL@TB",
                    "IND@LAR",
                    "JAC@SF",
                    "BALT@KC",
                    "CHI@LV",
                    "GB@DAL",
                    "NYJ@MIA",
                    "CINC@DEN",
                ],
            },
            5: {
                "dates": "10/2-10/6",
                "games": [
                    "DUKE@CAL",
                    "Mia,F@FSU",
                    "BSU@ND",
                    "TEX@FLA",
                    "KSU@BAY",
                    "OSU@UA",
                    "SF@LAR",
                    "MINN@CLEV",
                    "HOU@BALT",
                    "MIA@CAR",
                    "LV@IND",
                    "NYG@NO",
                    "DAL@NYJ",
                    "DEN@PHIL",
                    "TENN@ARIZ",
                    "TB@SEA",
                    "DET@CINC",
                    "WASH@LAC",
                    "NE@BUFF",
                    "KC@IND",
                ],
            },
            6: {
                "dates": "10/9-10/13",
                "games": [
                    "STAN@SMU",
                    "OSU@ILL",
                    "MICH@USC",
                    "Scar@LSU",
                    "UCLA@MSU",
                    "PHIL@NYG",
                    "DEN@NYJ",
                    "LAR@BALT",
                    "DAL@CAR",
                    "ARIZ@IND",
                    "SEA@JAC",
                    "LAC@MIA",
                    "CLEV@PITT",
                    "SF@TB",
                    "TENN@LV",
                    "CINC@GB",
                    "NE@NO",
                    "DET@KC",
                    "BUFF@ATL",
                    "CHI@WASH",
                ],
            },
            7: {
                "dates": "10/16-10/20",
                "games": [
                    "NC@CAL",
                    "FSU@STAN",
                    "USC@ND",
                    "UT@ALA",
                    "TexT@ASU",
                    "PITT@CINC",
                    "LAR@JAC",
                    "NO@CHI",
                    "MIA@CLEV",
                    "LV@KC",
                    "PHIL@MINN",
                    "CAR@NYJ",
                    "NE@TENN",
                    "NYG@DEN",
                    "IND@LAC",
                    "GB@ARIZ",
                    "WASH@DAL",
                    "ATL@SF",
                    "TB@DET",
                    "HOU@SEA",
                ],
            },
            8: {
                "dates": "10/23-10/27",
                "games": [
                    "CAL@VT",
                    "STAN@Mia,F",
                    "KSU@KAN",
                    "BYU@ISU",
                    "ALA@Scar",
                    "OSU@TexT",
                    "ILL@UW",
                    "MINN@LAC",
                    "MIA@ATL",
                    "CHI@BALT",
                    "BUFF@CAR",
                    "NYJ@CINC",
                    "SF@HOU",
                    "CLEV@NE",
                    "NYG@PHIL",
                    "TB@NO",
                    "DAL@DEN",
                    "TENN@IND",
                    "GB@PITT",
                    "WASH@KC",
                ],
            },
            9: {
                "dates": "10/30-11/3",
                "games": [
                    "VA@CAL",
                    "UPITT@STAN",
                    "PSU@OSU",
                    "ASU@ISU",
                    "USC@NEB",
                    "GEO@FLA",
                    "BALT@MIA",
                    "CHI@CINC",
                    "MINN@DET",
                    "CAR@GB",
                    "DEN@HOU",
                    "ATL@NE",
                    "SF@NYG",
                    "IND@PITT",
                    "LAC@TENN",
                    "NO@LAR",
                    "JAC@LV",
                    "KC@BUFF",
                    "SEA@WASH",
                    "ARIZ@DAL",
                ],
            },
            10: {
                "dates": "11/6-11/10",
                "games": [
                    "CAL@LOU",
                    "STAN@NC",
                    "LSU@ALA",
                    "UIND@PSU",
                    "NEB@UCLA",
                    "FSU@CLEM",
                    "LV@DEN",
                    "ATL@IND",
                    "NO@CAR",
                    "NYG@CHI",
                    "JAC@HOU",
                    "BUFF@MIA",
                    "BALT@MINN",
                    "CLEV@NYJ",
                    "NE@TB",
                    "ARIZ@SEA",
                    "LAR@SF",
                    "DET@WASH",
                    "PITT@LAC",
                    "PHIL@GB",
                ],
            },
            11: {
                "dates": "11/13-11/17",
                "games": [
                    "TEX@GEO",
                    "WISC@UIND",
                    "BSU@SDSU",
                    "FLA@MISS",
                    "IA@USC",
                    "NYJ@NE",
                    "WASH@MIA",
                    "CAR@ATL",
                    "TB@BUFF",
                    "LAC@JAC",
                    "CHI@MINN",
                    "GB@NYG",
                    "CINC@PITT",
                    "HOU@TENN",
                    "SF@ARIZ",
                    "SEA@LAR",
                    "BALT@CLEV",
                    "KC@DEN",
                    "DET@PHIL",
                    "DAL@LV",
                ],
            },
            12: {
                "dates": "11/20-11/24",
                "games": [
                    "CAL@STAN",
                    "LOU@SMU",
                    "USC@ORE",
                    "UT@FLA",
                    "KSU@UTAH",
                    "UW@UCLA",
                    "BUFF@HOU",
                    "NYJ@BALT",
                    "PITT@CHI",
                    "NE@CINC",
                    "NYG@DET",
                    "MINN@GB",
                    "IND@KC",
                    "SEA@TENN",
                    "JAC@ARIZ",
                    "CLEV@LV",
                    "PHIL@DAL",
                    "ATL@NO",
                    "TB@LAR",
                    "CAR@SF",
                ],
            },
            13: {
                "dates": "11/27-12/1",
                "games": [
                    "SMU@CAL",
                    "ND@STAN",
                    "OSU@MICH",
                    "UCLA@USC",
                    "GB@DET",
                    "KC@DAL",
                    "CINC@BALT",
                    "CHI@PHIL",
                    "LAR@CAR",
                    "SF@CLEV",
                    "HOU@IND",
                    "NO@MIA",
                    "ATL@NYJ",
                    "ARIZ@TB",
                    "JAC@TENN",
                    "MINN@SEA",
                    "LV@LAC",
                    "BUFF@PITT",
                    "DEN@WASH",
                    "NYG@NE",
                ],
            },
            14: {
                "dates": "12/4-12/8",
                "games": [
                    "Big10 Champ",
                    "SEC Champ",
                    "ACC Champ",
                    "Big12 Champ",
                    "AAC Champ",
                    "MW Champ",
                    "DAL@DET",
                    "SEA@ATL",
                    "PITT@BALT",
                    "TENN@CLEV",
                    "CHI@GB",
                    "IND@JAC",
                    "WASH@MINN",
                    "MIA@NYJ",
                    "NO@TB",
                    "DEN@LV",
                    "LAR@ARIZ",
                    "CINC@BUFF",
                    "HOU@KC",
                    "PHIL@LAC",
                ],
            },
            15: {
                "dates": "12/11-12/15",
                "games": [
                    "ARMY@NAVY",
                    "ATL@TB",
                    "CLEV@CHI",
                    "BALT@CINC",
                    "ARIZ@HOU",
                    "NYJ@JAC",
                    "LAC@KC",
                    "BUFF@NE",
                    "WASH@NYG",
                    "LV@PHIL",
                    "GB@DEN",
                    "DET@LAR",
                    "CAR@NO",
                    "IND@SEA",
                    "TENN@SF",
                    "MINN@DAL",
                    "MIA@PITT",
                ],
            },
            16: {
                "dates": "12/18-12/22",
                "games": [
                    "LAR@SEA",
                    "GB@CHI",
                    "PHIL@WASH",
                    "NE@BALT",
                    "TB@CAR",
                    "BUFF@CLEV",
                    "LAC@DAL",
                    "NYJ@NO",
                    "MINN@NYG",
                    "KC@TENN",
                    "ATL@ARIZ",
                    "JAC@DEN",
                    "PITT@DET",
                    "LV@HOU",
                    "CINC@MIA",
                    "SF@IND",
                ],
            },
            17: {
                "dates": "12/25-12/29",
                "games": [
                    "DAL@WASH",
                    "DET@MINN",
                    "DEN@KC",
                    "SEA@CAR",
                    "ARIZ@CINC",
                    "BALT@GB",
                    "HOU@LAC",
                    "NYG@LV",
                    "PITT@CLEV",
                    "JAC@IND",
                    "TB@MIA",
                    "NE@NYJ",
                    "NO@TENN",
                    "PHIL@BUFF",
                    "CHI@SF",
                    "LAR@ATL",
                ],
            },
            18: {
                "dates": "1/1-1/4",
                "games": [
                    "NO@ATL",
                    "NYJ@BUFF",
                    "DET@CHI",
                    "CLEV@CINC",
                    "LAC@DEN",
                    "IND@HOU",
                    "TENN@JAC",
                    "ARIZ@LAR",
                    "KC@LV",
                    "GB@MINN",
                    "MIA@NE",
                    "DAL@NYG",
                    "WASH@PHIL",
                    "BALT@PITT",
                    "SEA@SF",
                    "CAR@TB",
                ],
            },
        }
