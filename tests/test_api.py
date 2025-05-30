#!/usr/bin/env python3
"""API tests for OpenCraftShop web service"""
import requests
import json
import sys
import time
from typing import Dict, List, Tuple

BASE_URL = "http://web:5000"

def test_homepage() -> Tuple[bool, str]:
    """Test if homepage loads correctly"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200 and "OpenCraftShop" in response.text:
            return True, "Homepage loads correctly"
        return False, f"Homepage failed: status={response.status_code}"
    except Exception as e:
        return False, f"Homepage error: {str(e)}"

def test_furniture_generation(furniture_type: str, dimensions: Dict[str, int]) -> Tuple[bool, str]:
    """Test furniture generation for a specific type"""
    payload = {"type": furniture_type, **dimensions}
    
    try:
        response = requests.post(f"{BASE_URL}/api/generate", json=payload, timeout=30)
        
        if response.status_code != 200:
            return False, f"Generation failed with status {response.status_code}"
        
        data = response.json()
        
        # Check required fields
        required_fields = ['files', 'cut_list_content', 'shopping_list_content', 'success']
        for field in required_fields:
            if field not in data:
                return False, f"Missing field: {field}"
        
        # Check files
        required_files = ['stl_assembled', 'stl_exploded', 'cut_list', 'shopping_list']
        for file_type in required_files:
            if file_type not in data['files']:
                return False, f"Missing file: {file_type}"
        
        # Test file downloads
        for file_type, filename in data['files'].items():
            download_response = requests.get(f"{BASE_URL}/api/download/{filename}", timeout=5)
            if download_response.status_code != 200:
                return False, f"Download failed for {filename}"
        
        # Check cut list format
        cut_content = data.get('cut_list_content', '')
        has_table = '│' in cut_content or '┌' in cut_content
        
        return True, f"Generated successfully (files: {len(data['files'])}, table format: {has_table})"
        
    except Exception as e:
        return False, f"Generation error: {str(e)}"

def run_tests():
    """Run all API tests"""
    print("🧪 OpenCraftShop API Test Suite")
    print("=" * 50)
    
    # Define test cases
    furniture_tests = [
        ("workbench", {"length": 72, "width": 24, "height": 34}),
        ("storage_bench", {"length": 48, "width": 18, "height": 18}),
        ("bed_frame", {"length": 80, "width": 60, "height": 14}),
        ("bookshelf", {"length": 36, "width": 12, "height": 72})
    ]
    
    results = []
    
    # Test 1: Homepage
    print("\n📍 Testing homepage...")
    success, message = test_homepage()
    results.append(("Homepage", success, message))
    print(f"   {'✅' if success else '❌'} {message}")
    
    # Test 2: Furniture generation
    print("\n📐 Testing furniture generation...")
    for furniture_type, dimensions in furniture_tests:
        print(f"\n   Testing {furniture_type}...")
        success, message = test_furniture_generation(furniture_type, dimensions)
        results.append((f"{furniture_type} generation", success, message))
        print(f"   {'✅' if success else '❌'} {message}")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for test_name, success, message in results:
        status = "PASS" if success else "FAIL"
        print(f"{status:4} | {test_name:25} | {message}")
    
    print("=" * 50)
    print(f"Total: {passed}/{total} passed ({passed/total*100:.0f}%)")
    
    # Exit with appropriate code
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(run_tests())