#!/usr/bin/env python3
import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_api():
    print("🧪 Testing OpenCraftShop Web UI API...\n")
    
    # Test 1: Check homepage
    print("1. Testing homepage...")
    response = requests.get(BASE_URL)
    if response.status_code == 200 and "OpenCraftShop" in response.text:
        print("   ✅ Homepage loads correctly")
    else:
        print("   ❌ Homepage failed to load")
    
    # Test 2: Test each furniture type
    furniture_types = ["workbench", "storage_bench", "bed_frame", "bookshelf"]
    
    for furniture_type in furniture_types:
        print(f"\n2. Testing {furniture_type} generation...")
        
        # Default dimensions for each type
        dimensions = {
            "workbench": {"length": 72, "width": 24, "height": 34},
            "storage_bench": {"length": 48, "width": 18, "height": 18},
            "bed_frame": {"length": 80, "width": 60, "height": 14},
            "bookshelf": {"length": 36, "width": 12, "height": 72}
        }
        
        payload = {
            "type": furniture_type,
            **dimensions[furniture_type]
        }
        
        response = requests.post(f"{BASE_URL}/api/generate", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Generated {furniture_type}")
            print(f"      - Assembled STL: {data['files']['stl_assembled']}")
            print(f"      - Exploded STL: {data['files']['stl_exploded']}")
            print(f"      - Cut list: {data['files']['cut_list']}")
            print(f"      - Shopping list: {data['files']['shopping_list']}")
            
            # Test file downloads
            for file_type, filename in data['files'].items():
                download_response = requests.get(f"{BASE_URL}/api/download/{filename}")
                if download_response.status_code == 200:
                    print(f"      ✅ Download works: {filename}")
                else:
                    print(f"      ❌ Download failed: {filename}")
                    
            # Check cut list content
            if 'cut_list_content' in data:
                lines = data['cut_list_content'].split('\n')
                print(f"      - Cut list has {len(lines)} lines")
                # Check for ASCII diagram elements
                if '├' in data['cut_list_content'] or '│' in data['cut_list_content']:
                    print(f"      ✅ Cut list contains ASCII diagrams")
                else:
                    print(f"      ℹ️  Cut list in table format")
        else:
            print(f"   ❌ Failed to generate {furniture_type}: {response.status_code}")
    
    print("\n✅ All API tests completed!")

if __name__ == "__main__":
    test_api()