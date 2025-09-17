#!/usr/bin/env python3
"""
Test runner for Excel automation tests.
"""

import sys
from pathlib import Path

import pytest

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_excel_tests():
    """Run Excel automation tests."""
    print("🧪 Running Excel Automation Tests...")

    # Run the tests
    test_file = Path(__file__).parent / "test_excel_automation.py"
    result = pytest.main([str(test_file), "-v", "--tb=short"])

    if result == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")

    return result


if __name__ == "__main__":
    exit_code = run_excel_tests()
    sys.exit(exit_code)
