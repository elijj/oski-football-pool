#!/usr/bin/env python3
"""
Demonstration script to recreate the contrarian analysis output.
"""

import os
import subprocess
import sys


def run_command(cmd, description):
    """Run a command and show the result."""
    print(f"\n🎯 {description}")
    print(f"Command: {cmd}")
    print("-" * 60)

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Success!")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ Error!")
            if result.stderr:
                print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False


def main():
    """Demonstrate how to recreate the contrarian analysis output."""
    print("🏈 CONTRARIAN ANALYSIS OUTPUT RECREATION")
    print("=" * 60)
    print("This script demonstrates how to recreate the contrarian analysis")
    print("output that was generated for Pool Week 1.")
    print()

    # Check if we're in the right directory
    if not os.path.exists("football_pool"):
        print("❌ Please run this script from the project root directory")
        print("   cd /path/to/oski-football-pool")
        sys.exit(1)

    # Step 1: Generate contrarian prompt
    success1 = run_command(
        "football-pool contrarian-prompt 2024-09-17", "Step 1: Generate Contrarian Analysis Prompt"
    )

    if not success1:
        print("❌ Failed to generate contrarian prompt")
        return

    # Step 2: Check if contrarian analysis file exists
    if os.path.exists("week_1_contrarian_analysis.json"):
        print("\n✅ Contrarian analysis file found!")

        # Step 3: Update Excel with contrarian picks
        success3 = run_command(
            "football-pool excel-update 1 --date '2024-09-17' --analysis week_1_contrarian_analysis.json",
            "Step 3: Update Excel File with Contrarian Picks",
        )

        if success3:
            print("\n✅ Excel file updated with contrarian picks!")

            # Step 4: Check if summary file exists
            if os.path.exists("Pool_Week_1_Contrarian_Analysis_Summary.md"):
                print("\n✅ Summary file found!")
                print("\n🎉 CONTRARIAN ANALYSIS OUTPUT SUCCESSFULLY RECREATED!")
                print("\nFiles generated:")
                print("- 2024-09-17_contrarian_prompt.txt")
                print("- week_1_contrarian_analysis.json")
                print("- Dawgpac25_2024-09-17.xlsx")
                print("- Pool_Week_1_Contrarian_Analysis_Summary.md")
            else:
                print("\n⚠️  Summary file not found - run: football-pool report 1 --date 2024-09-17")
        else:
            print("\n❌ Failed to update Excel file")
    else:
        print("\n⚠️  Contrarian analysis file not found")
        print("   You need to:")
        print("   1. Copy the generated prompt to ChatGPT/Claude")
        print("   2. Get the JSON response")
        print("   3. Save as 'week_1_contrarian_analysis.json'")
        print("   4. Run this script again")


if __name__ == "__main__":
    main()
