#!/usr/bin/env python3
"""
Extract the actual contrarian picks from the analysis file.
"""

import json


def extract_contrarian_picks():
    """Extract contrarian picks from the analysis file."""
    try:
        with open("week_1_contrarian_analysis.json") as f:
            data = json.load(f)

        picks = []
        for pick in data["optimal_picks"]:
            picks.append({"team": pick["team"], "confidence": pick["confidence"]})

        # Sort by confidence (highest first)
        picks.sort(key=lambda x: x["confidence"], reverse=True)

        print("🎯 CONTRARIAN PICKS FROM ANALYSIS:")
        print("=" * 50)
        for pick in picks:
            print(f"Confidence {pick['confidence']:2d}: {pick['team']}")

        # Save to file
        output_data = {"picks": picks}
        with open("week_1_actual_contrarian_picks.json", "w") as f:
            json.dump(output_data, f, indent=2)

        print(f"\n✅ Extracted {len(picks)} contrarian picks")
        print("📁 Saved to: week_1_actual_contrarian_picks.json")

        return picks

    except Exception as e:
        print(f"❌ Error extracting picks: {e}")
        return []


if __name__ == "__main__":
    extract_contrarian_picks()
