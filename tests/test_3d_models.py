#!/usr/bin/env python3
"""Test 3D model generation and STL file validity"""
import os
import struct
import sys
from typing import Tuple, Dict

def read_stl_stats(filepath: str) -> Tuple[bool, Dict]:
    """Read STL file and return statistics"""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
        # Check if it's ASCII STL
        if content.startswith('solid'):
            # Count facets in ASCII STL
            num_triangles = content.count('facet normal')
            actual_size = os.path.getsize(filepath)
            
            return True, {
                'triangles': num_triangles,
                'size': actual_size,
                'valid': True,  # ASCII STL files don't have strict size requirements
                'format': 'ASCII'
            }
        else:
            # Binary STL
            with open(filepath, 'rb') as f:
                # Read header (80 bytes)
                header = f.read(80)
                
                # Read number of triangles
                num_triangles = struct.unpack('I', f.read(4))[0]
                
                # Calculate expected file size
                expected_size = 80 + 4 + (num_triangles * 50)
                actual_size = os.path.getsize(filepath)
                
                return True, {
                    'triangles': num_triangles,
                    'size': actual_size,
                    'valid': actual_size == expected_size,
                    'format': 'Binary'
                }
    except Exception as e:
        return False, {'error': str(e)}

def test_stl_files():
    """Test all generated STL files"""
    print("🧪 3D Model Test Suite")
    print("=" * 50)
    
    output_dir = "/app/output"
    stl_files = [f for f in os.listdir(output_dir) if f.endswith('.stl')]
    
    if not stl_files:
        print("❌ No STL files found in output directory")
        return 1
    
    print(f"\n📦 Found {len(stl_files)} STL files")
    
    results = []
    for stl_file in sorted(stl_files):
        filepath = os.path.join(output_dir, stl_file)
        success, stats = read_stl_stats(filepath)
        
        if success:
            valid = stats['valid']
            format_str = stats.get('format', 'Unknown')
            results.append((stl_file, valid))
            status = '✅' if valid else '⚠️'
            print(f"\n{status} {stl_file}")
            print(f"   Format: {format_str}")
            print(f"   Triangles: {stats['triangles']:,}")
            print(f"   Size: {stats['size']:,} bytes")
            print(f"   Valid: {'Yes' if valid else 'No (size mismatch)'}")
        else:
            results.append((stl_file, False))
            print(f"\n❌ {stl_file}")
            print(f"   Error: {stats['error']}")
    
    # Check assembled vs exploded
    print("\n📊 Model Comparison")
    print("-" * 30)
    
    for base_name in ['workbench', 'bookshelf', 'bed_frame', 'storage_bench']:
        assembled = f"{base_name}.stl"
        exploded = f"{base_name}_exploded.stl"
        
        if assembled in stl_files and exploded in stl_files:
            _, stats_a = read_stl_stats(os.path.join(output_dir, assembled))
            _, stats_e = read_stl_stats(os.path.join(output_dir, exploded))
            
            if 'triangles' in stats_a and 'triangles' in stats_e:
                print(f"\n{base_name}:")
                print(f"  Assembled: {stats_a['triangles']:,} triangles")
                print(f"  Exploded:  {stats_e['triangles']:,} triangles")
                print(f"  Difference: {abs(stats_a['triangles'] - stats_e['triangles']):,}")
    
    # Summary
    valid_count = sum(1 for _, valid in results if valid)
    print("\n" + "=" * 50)
    print(f"Valid STL files: {valid_count}/{len(results)}")
    
    return 0 if valid_count == len(results) else 1

if __name__ == "__main__":
    sys.exit(test_stl_files())