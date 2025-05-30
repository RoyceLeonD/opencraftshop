#!/usr/bin/env python3
"""
OpenCraftShop - CLI for generating furniture plans
MIT License
"""

import click
import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from optimize_cuts import CutOptimizer, CutPiece
from generate_bom import BOMGenerator
from visualize_terminal import TerminalVisualizer
from rich.console import Console

console: Console = Console()

# The banner of shame and hope
BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║   ___                  ___            __ _   ___  _            ║
║  / _ \\ _ __   ___ _ _ / __|_ _ __ _ / _| |_/ __|| |_  ___ _ _ ║
║ | (_) | '_ \\ / -_) ' \\| (__| '_/ _` |  _|  _\\__ \\| ' \\/ _ \\ '_ \\║
║  \\___/| .__/ \\___|_||_|\\___|_| \\__,_|_|  \\__|___/|_||_\\___/ .__/║
║       |_|                                                  |_|  ║
║                                                                ║
║  "Computers cut straighter than you" ™            ║
╚═══════════════════════════════════════════════════════════════╝
"""

def get_furniture_defaults(furniture_type: str) -> Dict[str, int]:
    """Get default dimensions for different furniture types"""
    defaults: Dict[str, Dict[str, int]] = {
        'workbench': {'length': 72, 'width': 24, 'height': 34},
        'storage_bench': {'length': 48, 'width': 18, 'height': 18},
        'bed_frame': {'length': 80, 'width': 60, 'height': 14},
        'bookshelf': {'length': 36, 'width': 12, 'height': 72}
    }
    return defaults.get(furniture_type, defaults['workbench'])

@click.command()
@click.option('--type', 'furniture_type', default='workbench', 
              type=click.Choice(['workbench', 'storage_bench', 'bed_frame', 'bookshelf']), 
              help='Furniture type')
@click.option('--length', type=int, help='Length in inches')
@click.option('--width', type=int, help='Width in inches')
@click.option('--height', type=int, help='Height in inches')
@click.option('--kerf', default=0.125, help='Saw blade width (default: 1/8")')
@click.option('--output-dir', default='./output', help='Output directory')
@click.option('--visualize/--no-visualize', default=True, help='Show terminal visualization')
def design_furniture(furniture_type: str, length: Optional[int], width: Optional[int], 
                   height: Optional[int], kerf: float, output_dir: str, visualize: bool) -> None:
    """Generate furniture design and cut lists"""
    
    # Show our banner of shame
    if visualize:
        console.print(BANNER, style="bright_blue")
    
    # Get default dimensions for furniture type
    defaults: Dict[str, int] = get_furniture_defaults(furniture_type)
    if length is None:
        length = defaults['length']
    if width is None:
        width = defaults['width']
    if height is None:
        height = defaults['height']
    
    console.print(f"\nGenerating {furniture_type.replace('_', ' ')}")
    console.print(f"Dimensions: {length}\" x {width}\" x {height}\"")
    console.print(f"Kerf: {kerf}\"")
    
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load design parameters
    with open('config/design_params.json', 'r') as f:
        design_params = json.load(f)
    
    # Validate dimensions based on furniture type
    # Note: Different furniture types might have different constraints
    max_length = 96 if furniture_type != 'bed_frame' else 120
    max_width = 60 if furniture_type == 'bed_frame' else 36
    max_height = 80 if furniture_type == 'bookshelf' else 40
    
    if not (12 <= length <= max_length):
        console.print(f"\n[red]Length must be between 12 and {max_length} inches[/red]")
        return
    if not (8 <= width <= max_width):
        console.print(f"\n[red]Width must be between 8 and {max_width} inches[/red]")
        return
    if not (8 <= height <= max_height):
        console.print(f"\n[red]Height must be between 8 and {max_height} inches[/red]")
        return
    
    # Generate bill of materials based on furniture type
    console.print("\nCalculating materials...")
    bom_gen: BOMGenerator = BOMGenerator()
    
    # Call appropriate BOM generator method based on furniture type
    cut_pieces: List[CutPiece]
    if furniture_type == 'workbench':
        cut_pieces = bom_gen.generate_workbench_bom(length, width, height)
    elif furniture_type == 'storage_bench':
        cut_pieces = bom_gen.generate_storage_bench_bom(length, width, height)
    elif furniture_type == 'bed_frame':
        cut_pieces = bom_gen.generate_bed_frame_bom(length, width, height)
    elif furniture_type == 'bookshelf':
        cut_pieces = bom_gen.generate_bookshelf_bom(length, width, height)
    
    # Save BOM
    bom_text: str = bom_gen.format_bom_text()
    with open(f"{output_dir}/bill_of_materials.txt", 'w') as f:
        f.write(bom_text)
    
    # Optimize cuts
    console.print("Optimizing cuts...")
    optimizer: CutOptimizer = CutOptimizer(kerf=kerf)
    optimized: Dict[str, List] = optimizer.optimize(cut_pieces)
    cut_list: Dict[str, Any] = optimizer.generate_cut_list(optimized)
    
    # Save cut list
    with open(f"{output_dir}/cut_list.json", 'w') as f:
        json.dump(cut_list, f, indent=2)
    
    # Generate shopping list
    console.print("Creating shopping list...")
    shopping_list: Dict[str, Any] = bom_gen.generate_shopping_list(optimized)
    
    # Adjust supplies based on furniture type
    if furniture_type == 'bed_frame':
        shopping_list['other_supplies'] = [
            {'item': 'Bed rail brackets', 'quantity': '4 sets', 'est_cost': 25.00},
            {'item': 'Wood screws (3" and 2")', 'quantity': '2 lbs', 'est_cost': 15.00},
            {'item': 'Wood glue', 'quantity': '1 bottle', 'est_cost': 8.00},
            {'item': 'Sandpaper (120, 220 grit)', 'quantity': '1 pack each', 'est_cost': 10.00},
            {'item': 'Wood stain or finish', 'quantity': '1 quart', 'est_cost': 25.00}
        ]
    elif furniture_type == 'bookshelf':
        shopping_list['other_supplies'] = [
            {'item': 'Wood screws (1.5" and 2")', 'quantity': '1 lb', 'est_cost': 10.00},
            {'item': 'Shelf pins', 'quantity': '20', 'est_cost': 5.00},
            {'item': 'Wood glue', 'quantity': '1 bottle', 'est_cost': 8.00},
            {'item': 'Sandpaper (120, 220 grit)', 'quantity': '1 pack each', 'est_cost': 10.00},
            {'item': 'Wood finish', 'quantity': '1 quart', 'est_cost': 20.00}
        ]
    
    shopping_list['estimated_total'] = shopping_list['total_cost'] + sum(
        item['est_cost'] for item in shopping_list['other_supplies']
    )
    
    # Save shopping list
    with open(f"{output_dir}/shopping_list.json", 'w') as f:
        json.dump(shopping_list, f, indent=2)
    
    # Create text versions
    with open(f"{output_dir}/cut_list.txt", 'w') as f:
        f.write(f"OPTIMIZED CUT LIST - {furniture_type.upper().replace('_', ' ')}\n")
        f.write("=" * 50 + "\n\n")
        for lumber_type, data in cut_list.items():
            if lumber_type == 'summary':
                continue
            f.write(f"{lumber_type}:\n")
            for stock in data['stocks']:
                f.write(f"  Stock #{stock['stock_number']} ({stock['length']}\" / {stock['length_feet']}')\n")
                for cut in stock['cuts']:
                    f.write(f"    - {cut[0]}\" ({cut[1]})\n")
                f.write(f"    Waste: {stock['waste']:.2f}\" (Efficiency: {stock['efficiency']:.1f}%)\n\n")
        
        summary = cut_list['summary']
        f.write(f"\nSUMMARY:\n")
        f.write(f"Total waste: {summary['total_waste_inches']:.2f}\" ({summary['total_waste_feet']:.2f}')\n")
        f.write(f"Overall efficiency: {summary['efficiency']:.1f}%\n")
        f.write(f"Total cost: ${summary['total_cost']:.2f}\n")
    
    with open(f"{output_dir}/shopping_list.txt", 'w') as f:
        f.write(f"SHOPPING LIST - {furniture_type.upper().replace('_', ' ')}\n")
        f.write("=" * 50 + "\n\n")
        f.write("LUMBER:\n")
        for item in shopping_list['items']:
            f.write(f"  {item['quantity']}x {item['description']} @ ${item['unit_price']:.2f} = ${item['subtotal']:.2f}\n")
        f.write(f"\nLumber Total: ${shopping_list['total_cost']:.2f}\n\n")
        
        f.write("OTHER SUPPLIES:\n")
        for supply in shopping_list['other_supplies']:
            f.write(f"  - {supply['item']}: {supply['quantity']} (~${supply['est_cost']:.2f})\n")
        f.write(f"\nESTIMATED TOTAL: ${shopping_list['estimated_total']:.2f}\n")
    
    # Generate OpenSCAD model
    console.print("Generating 3D model...")
    
    # Get appropriate template file
    template_file: str = f'src/templates/{furniture_type}.scad'
    
    # Generate parameters based on furniture type
    scad_params: str
    if furniture_type == 'workbench':
        scad_params = f"""
// Generated parameters
bench_length = {length};
bench_width = {width};
bench_height = {height};
top_thickness = 3;
"""
    elif furniture_type == 'storage_bench':
        scad_params = f"""
// Generated parameters
bench_length = {length};
bench_width = {width};
bench_height = {height};
storage_depth = {height - 4};
"""
    elif furniture_type == 'bed_frame':
        scad_params = f"""
// Generated parameters
bed_length = {length};
bed_width = {width};
bed_height = {height};
headboard_height = {min(48, height + 22)};
mattress_support_slats = {max(9, int(length / 8))};
"""
    elif furniture_type == 'bookshelf':
        num_shelves: int = max(3, min(8, int(height / 12)))
        scad_params = f"""
// Generated parameters
shelf_height = {height};
shelf_width = {length};
shelf_depth = {width};
num_shelves = {num_shelves};
shelf_thickness = "1x12";
"""
    
    # Read template and prepend parameters
    with open(template_file, 'r') as f:
        scad_content: str = f.read()
    
    # Remove default parameters and add new ones
    lines: List[str] = scad_content.split('\n')
    new_lines: List[str] = []
    skip_params: bool = False
    for line in lines:
        if line.strip().startswith('// Default parameters'):
            skip_params = True
            new_lines.append(line)
            new_lines.append(scad_params.strip())
        elif skip_params and line.strip() and not any(line.strip().startswith(p) for p in 
                ['bench_', 'top_', 'bed_', 'shelf_', 'storage_', 'headboard_', 'mattress_', 'num_']):
            skip_params = False
            new_lines.append(line)
        elif not skip_params:
            new_lines.append(line)
    
    # Save customized SCAD file
    custom_scad: str = '\n'.join(new_lines)
    output_scad_name: str = f"{furniture_type}_custom.scad"
    with open(f"{output_dir}/{output_scad_name}", 'w') as f:
        f.write(custom_scad)
    
    # Copy lumber_lib.scad to output directory
    import shutil
    shutil.copy('src/lumber_lib.scad', f'{output_dir}/lumber_lib.scad')
    
    # Generate STL files (both assembled and exploded views)
    for view_mode, suffix in [("assembled", ""), ("exploded", "_exploded")]:
        output_stl_name: str = f"{furniture_type}{suffix}.stl"
        try:
            # Create a temporary scad file with the view mode set
            temp_scad_content = custom_scad.replace('view_mode = "assembled";', f'view_mode = "{view_mode}";')
            temp_scad_name = f"{furniture_type}_custom_{view_mode}.scad"
            with open(f"{output_dir}/{temp_scad_name}", 'w') as f:
                f.write(temp_scad_content)
            
            subprocess.run([
                'openscad',
                '-o', output_stl_name,
                temp_scad_name
            ], check=True, capture_output=True, cwd=output_dir)
            console.print(f"[green]✓ Generated {output_stl_name} ({view_mode} view)[/green]")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]OpenSCAD error: {e.stderr.decode()}[/red]")
        except FileNotFoundError:
            console.print("[yellow]OpenSCAD not found. Install from openscad.org[/yellow]")
    
    # Terminal visualization
    if visualize:
        viz: TerminalVisualizer = TerminalVisualizer()
        
        # Display ASCII art (adapted for furniture type)
        console.print("\n")
        console.print(viz.draw_ascii_furniture(furniture_type, length, width, height))
        
        # Display summary
        dimensions: Dict[str, Any] = {
            'type': furniture_type,
            'length': length,
            'width': width,
            'height': height
        }
        viz.display_summary(cut_list, dimensions)
        
        # Display cut list
        viz.display_cut_list(cut_list)
        
        # Display cut diagrams
        viz.display_cut_diagram(cut_list)
        
        # Display shopping list
        viz.display_shopping_list(shopping_list)
    
    console.print(f"\n[green]Done. Files in {output_dir}/[/green]")
    console.print(f"\n{output_stl_name} - 3D model")
    console.print(f"{output_scad_name} - OpenSCAD source")
    console.print("bill_of_materials.txt - Parts list")
    console.print("cut_list.txt - Cut instructions")
    console.print("shopping_list.txt - Shopping list")

if __name__ == '__main__':
    design_furniture()