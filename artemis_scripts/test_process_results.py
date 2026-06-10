#!/usr/bin/env python3
"""
Test suite for process_results.py
Tests both valid and invalid JSON structures to ensure defensive programming works correctly.
"""

import json
import os
import subprocess
import sys
import tempfile


def run_process_results(json_data, test_name):
    """
    Run process_results.py with the given JSON data and capture output.
    Returns (exit_code, stderr, csv_output)
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Change to temp directory for test
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        
        try:
            # Write JSON input
            with open("artemis_raw.json", "w") as f:
                json.dump(json_data, f)
            
            # Run process_results.py
            result = subprocess.run(
                [sys.executable, os.path.join(original_dir, "process_results.py")],
                capture_output=True,
                text=True,
            )
            
            # Check if CSV was created
            csv_exists = os.path.exists("artemis_results.csv")
            csv_content = ""
            if csv_exists:
                with open("artemis_results.csv", "r") as f:
                    csv_content = f.read()
            
            return result.returncode, result.stderr, csv_content, csv_exists
        finally:
            os.chdir(original_dir)


def test_valid_json():
    """Test with valid JSON structure"""
    print("Test 1: Valid JSON structure... ", end="", flush=True)
    
    json_data = {
        "benchmarks": [
            {
                "stats": {
                    "data": [1.0, 2.0, 3.0, 4.0, 5.0],
                    "mean": 3.0,
                    "ops": 100
                }
            }
        ]
    }
    
    exit_code, stderr, csv_content, csv_exists = run_process_results(json_data, "valid")
    
    if exit_code == 0 and csv_exists and "3.0,100" in csv_content:
        print("✓ PASS")
        return True
    else:
        print(f"✗ FAIL (exit={exit_code}, csv_exists={csv_exists})")
        if stderr:
            print(f"  stderr: {stderr}")
        if csv_content:
            print(f"  csv: {csv_content}")
        return False


def test_missing_benchmarks_key():
    """Test with missing 'benchmarks' key"""
    print("Test 2: Missing 'benchmarks' key... ", end="", flush=True)
    
    json_data = {
        "other_key": []
    }
    
    exit_code, stderr, csv_content, csv_exists = run_process_results(json_data, "missing_benchmarks")
    
    if exit_code != 0 and "benchmarks" in stderr:
        print("✓ PASS")
        return True
    else:
        print(f"✗ FAIL (exit={exit_code}, contains 'benchmarks' in error: {'benchmarks' in stderr})")
        if stderr:
            print(f"  stderr: {stderr}")
        return False


def test_empty_benchmarks_list():
    """Test with empty benchmarks list"""
    print("Test 3: Empty 'benchmarks' list... ", end="", flush=True)
    
    json_data = {
        "benchmarks": []
    }
    
    exit_code, stderr, csv_content, csv_exists = run_process_results(json_data, "empty_benchmarks")
    
    if exit_code != 0 and "empty" in stderr.lower():
        print("✓ PASS")
        return True
    else:
        print(f"✗ FAIL (exit={exit_code}, contains 'empty': {'empty' in stderr.lower()})")
        if stderr:
            print(f"  stderr: {stderr}")
        return False


def test_missing_stats_key():
    """Test with missing 'stats' key in benchmark"""
    print("Test 4: Missing 'stats' key... ", end="", flush=True)
    
    json_data = {
        "benchmarks": [
            {
                "other_key": {}
            }
        ]
    }
    
    exit_code, stderr, csv_content, csv_exists = run_process_results(json_data, "missing_stats")
    
    if exit_code != 0 and "stats" in stderr:
        print("✓ PASS")
        return True
    else:
        print(f"✗ FAIL (exit={exit_code}, contains 'stats' in error: {'stats' in stderr})")
        if stderr:
            print(f"  stderr: {stderr}")
        return False


def test_missing_data_key():
    """Test with missing 'data' key in stats"""
    print("Test 5: Missing 'data' key in stats... ", end="", flush=True)
    
    json_data = {
        "benchmarks": [
            {
                "stats": {
                    "mean": 3.0,
                    "ops": 100
                }
            }
        ]
    }
    
    exit_code, stderr, csv_content, csv_exists = run_process_results(json_data, "missing_data")
    
    if exit_code != 0 and "data" in stderr:
        print("✓ PASS")
        return True
    else:
        print(f"✗ FAIL (exit={exit_code}, contains 'data' in error: {'data' in stderr})")
        if stderr:
            print(f"  stderr: {stderr}")
        return False


def test_empty_data_list():
    """Test with empty 'data' list"""
    print("Test 6: Empty 'data' list... ", end="", flush=True)
    
    json_data = {
        "benchmarks": [
            {
                "stats": {
                    "data": [],
                    "mean": 3.0,
                    "ops": 100
                }
            }
        ]
    }
    
    exit_code, stderr, csv_content, csv_exists = run_process_results(json_data, "empty_data")
    
    if exit_code != 0 and "empty" in stderr.lower():
        print("✓ PASS")
        return True
    else:
        print(f"✗ FAIL (exit={exit_code}, contains 'empty': {'empty' in stderr.lower()})")
        if stderr:
            print(f"  stderr: {stderr}")
        return False


def test_missing_mean_key():
    """Test with missing 'mean' key"""
    print("Test 7: Missing 'mean' key... ", end="", flush=True)
    
    json_data = {
        "benchmarks": [
            {
                "stats": {
                    "data": [1.0, 2.0, 3.0],
                    "ops": 100
                }
            }
        ]
    }
    
    exit_code, stderr, csv_content, csv_exists = run_process_results(json_data, "missing_mean")
    
    if exit_code != 0 and "mean" in stderr:
        print("✓ PASS")
        return True
    else:
        print(f"✗ FAIL (exit={exit_code}, contains 'mean' in error: {'mean' in stderr})")
        if stderr:
            print(f"  stderr: {stderr}")
        return False


def test_missing_ops_key():
    """Test with missing 'ops' key"""
    print("Test 8: Missing 'ops' key... ", end="", flush=True)
    
    json_data = {
        "benchmarks": [
            {
                "stats": {
                    "data": [1.0, 2.0, 3.0],
                    "mean": 2.0
                }
            }
        ]
    }
    
    exit_code, stderr, csv_content, csv_exists = run_process_results(json_data, "missing_ops")
    
    if exit_code != 0 and "ops" in stderr:
        print("✓ PASS")
        return True
    else:
        print(f"✗ FAIL (exit={exit_code}, contains 'ops' in error: {'ops' in stderr})")
        if stderr:
            print(f"  stderr: {stderr}")
        return False


def test_benchmarks_not_list():
    """Test when 'benchmarks' is not a list"""
    print("Test 9: 'benchmarks' is not a list... ", end="", flush=True)
    
    json_data = {
        "benchmarks": "not_a_list"
    }
    
    exit_code, stderr, csv_content, csv_exists = run_process_results(json_data, "benchmarks_not_list")
    
    if exit_code != 0 and "list" in stderr:
        print("✓ PASS")
        return True
    else:
        print(f"✗ FAIL (exit={exit_code}, contains 'list' in error: {'list' in stderr})")
        if stderr:
            print(f"  stderr: {stderr}")
        return False


def test_data_not_list():
    """Test when 'data' is not a list"""
    print("Test 10: 'data' is not a list... ", end="", flush=True)
    
    json_data = {
        "benchmarks": [
            {
                "stats": {
                    "data": "not_a_list",
                    "mean": 3.0,
                    "ops": 100
                }
            }
        ]
    }
    
    exit_code, stderr, csv_content, csv_exists = run_process_results(json_data, "data_not_list")
    
    if exit_code != 0 and "list" in stderr:
        print("✓ PASS")
        return True
    else:
        print(f"✗ FAIL (exit={exit_code}, contains 'list' in error: {'list' in stderr})")
        if stderr:
            print(f"  stderr: {stderr}")
        return False


def main():
    print("\n" + "="*60)
    print("Testing process_results.py defensive programming")
    print("="*60 + "\n")
    
    tests = [
        test_valid_json,
        test_missing_benchmarks_key,
        test_empty_benchmarks_list,
        test_missing_stats_key,
        test_missing_data_key,
        test_empty_data_list,
        test_missing_mean_key,
        test_missing_ops_key,
        test_benchmarks_not_list,
        test_data_not_list,
    ]
    
    results = [test() for test in tests]
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
