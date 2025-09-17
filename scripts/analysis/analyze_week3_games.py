#!/usr/bin/env python3
"""
Analyze Week 3 games to determine optimal 20 picks from 40 available games.
"""

from football_pool.core import PoolDominationSystem


def analyze_week3_games():
    """Analyze all Week 3 games and suggest optimal picks."""
    system = PoolDominationSystem()
    week3_games = system.schedule.get(3, {}).get("games", [])

    print("🏈 Week 3 Games Analysis (Pool Week 1)")
    print("=" * 60)
    print(f"Total games available: {len(week3_games)}")
    print("Picks needed: 20")
    print(f"Selection rate: {20/len(week3_games)*100:.1f}%")
    print()

    # Categorize games
    nfl_games = []
    cfb_games = []

    for game in week3_games:
        if any(
            team in game
            for team in [
                "KC",
                "BAL",
                "LAR",
                "DAL",
                "GB",
                "PHI",
                "SF",
                "BUF",
                "MIA",
                "DET",
                "NO",
                "TB",
                "ATL",
                "CAR",
                "ARI",
                "SEA",
                "LAC",
                "LV",
                "DEN",
                "PIT",
                "NYG",
                "CLEV",
                "HOU",
                "JAC",
                "CINC",
                "MINN",
                "NE",
                "IND",
                "TENN",
                "WASH",
                "CHI",
            ]
        ):
            nfl_games.append(game)
        else:
            cfb_games.append(game)

    print("📊 Game Categories:")
    print(f"NFL Games: {len(nfl_games)}")
    print(f"CFB Games: {len(cfb_games)}")
    print()

    print("🏈 NFL Games:")
    for i, game in enumerate(nfl_games, 1):
        print(f"  {i:2d}. {game}")
    print()

    print("🎓 CFB Games:")
    for i, game in enumerate(cfb_games, 1):
        print(f"  {i:2d}. {game}")
    print()

    # Suggest optimal picks (top 20 games)
    print("🎯 Suggested Top 20 Picks (High Confidence to Low):")
    print("=" * 60)

    # Prioritize NFL games with clear favorites
    suggested_picks = [
        ("KC", 20, "KC@NYG - Chiefs are heavy favorites"),
        ("BAL", 19, "DET@BALT - Ravens at home"),
        ("LAR", 18, "LAR@PHIL - Rams strong offense"),
        ("DAL", 17, "DAL@CHI - Cowboys favored"),
        ("GB", 16, "GB@CLEV - Packers experience"),
        ("PHI", 15, "PHIL@DAL - Eagles rivalry"),
        ("SF", 14, "ARIZ@SF - 49ers at home"),
        ("BUF", 13, "MIA@BUFF - Bills home field"),
        ("MIA", 12, "MIA@BUFF - Dolphins offense"),
        ("DET", 11, "DET@BALT - Lions momentum"),
        ("NO", 10, "NO@SEA - Saints defense"),
        ("TB", 9, "TB@LAR - Bucs experience"),
        ("ATL", 8, "ATL@CAR - Falcons youth"),
        ("CAR", 7, "CAR@SF - Panthers rebuild"),
        ("ARI", 6, "ARIZ@SF - Cardinals road"),
        ("SEA", 5, "NO@SEA - Seahawks home"),
        ("LAC", 4, "DEN@LAC - Chargers offense"),
        ("LV", 3, "LV@WASH - Raiders road"),
        ("DEN", 2, "DEN@LAC - Broncos defense"),
        ("PIT", 1, "PITT@NE - Steelers road"),
    ]

    for i, (team, conf, reason) in enumerate(suggested_picks, 1):
        print(f"{conf:2d}. {team:4s} - {reason}")

    print()
    print("💡 Strategy Notes:")
    print("- Focus on NFL games with clear favorites")
    print("- Use CFB games for lower confidence picks if needed")
    print("- Consider home field advantage")
    print("- Factor in team momentum and injuries")
    print("- Balance risk vs reward across confidence levels")


if __name__ == "__main__":
    analyze_week3_games()
