#!/usr/bin/env python3
"""
Test various dimension combinations to ensure they work correctly
"""

import subprocess
import json
import sys
from pathlib import Path

# Test cases for different furniture types
TEST_CASES = [
    # (furniture_type, length, width, height, expected_success)
    ("workbench", 72, 24, 34, True),      # Standard
    ("workbench", 36, 18, 28, True),      # Minimum
    ("workbench", 96, 36, 40, True),      # Maximum
    ("workbench", 200, 24, 34, False),    # Too long
    
    ("bookshelf", 36, 12, 72, True),      # Standard
    ("bookshelf", 24, 8, 48, True),       # Small
    ("bookshelf", 48, 16, 84, True),      # Large
    
    ("bed_frame", 80, 60, 14, True),      # Queen
    ("bed_frame", 75, 54, 14, True),      # Full
    ("bed_frame", 75, 38, 14, True),      # Twin
    
    ("storage_bench", 48, 18, 18, True),  # Standard
    ("storage_bench", 36, 14, 16, True),  # Small
    ("storage_bench", 72, 24, 20, True),  # Large
]

def run_test(furniture_type, length, width, height):
    """Run a single test case"""
    cmd = [
        "docker-compose", "run", "--rm", "opencraftshop",
        "--type", furniture_type,
        "--length", str(length),
        "--width", str(width),
        "--height", str(height),
        "--no-visualize"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False

def main():
    """Run all dimension tests"""
    print("OpenCraftShop Dimension Tests")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for furniture_type, length, width, height, expected in TEST_CASES:
        print(f"\nTesting {furniture_type}: {length}x{width}x{height}...", end=" ")
        
        success = run_test(furniture_type, length, width, height)
        
        if success == expected:
            print("✓ PASS")
            passed += 1
        else:
            print("✗ FAIL")
            failed += 1
            if expected:
                print(f"  Expected success but failed")
            else:
                print(f"  Expected failure but succeeded")
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    # Save results
    results = {
        "total": len(TEST_CASES),
        "passed": passed,
        "failed": failed,
        "success_rate": f"{(passed/len(TEST_CASES)*100):.1f}%"
    }
    
    with open("tests/results/dimension_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return failed == 0

if __name__ == "__main__":
    sys.exit(0 if main() else 1)