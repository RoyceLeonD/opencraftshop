#!/usr/bin/env python3
import json
from typing import List, Dict, Any
from dataclasses import dataclass
from optimize_cuts import CutPiece

@dataclass
class Material:
    lumber_type: str
    length: float
    quantity: int
    purpose: str

class BOMGenerator:
    def __init__(self) -> None:
        self.materials: List[Material] = []
        
    def add_material(self, lumber_type: str, length: float, quantity: int, purpose: str) -> None:
        """Add material to bill of materials"""
        self.materials.append(Material(lumber_type, length, quantity, purpose))
    
    def clear_materials(self) -> None:
        """Clear existing materials"""
        self.materials = []
    
    def generate_workbench_bom(self, length: float, width: float, height: float) -> List[CutPiece]:
        """Generate bill of materials for workbench"""
        self.clear_materials()
        
        # Legs - 4x4
        self.add_material("4x4", height, 4, "Legs")
        
        # Top boards - 2x6
        num_top_boards = int(width / 5.5) + (1 if width % 5.5 > 0 else 0)
        self.add_material("2x6", length, num_top_boards, "Top")
        
        # Long stretchers - 2x4
        stretcher_length = length - 8  # Account for leg insets
        self.add_material("2x4", stretcher_length, 4, "Long stretchers")
        
        # Short stretchers - 2x4
        short_stretcher_length = width - 8
        self.add_material("2x4", short_stretcher_length, 4, "Short stretchers")
        
        return self._convert_to_cut_pieces()
    
    def generate_storage_bench_bom(self, length: float, width: float, height: float) -> List[CutPiece]:
        """Generate bill of materials for storage bench"""
        self.clear_materials()
        
        # Frame - 2x4
        self.add_material("2x4", height, 4, "Corner posts")
        self.add_material("2x4", length, 4, "Long frame pieces")
        self.add_material("2x4", width - 7, 4, "Short frame pieces")
        
        # Top - 1x6
        num_top_boards = int(width / 5.5) + (1 if width % 5.5 > 0 else 0)
        self.add_material("1x6", length, num_top_boards, "Top boards")
        
        # Optional divider
        if length > 36:
            self.add_material("1x4", width - 7, 1, "Center divider")
        
        return self._convert_to_cut_pieces()
    
    def generate_bed_frame_bom(self, length: float, width: float, height: float) -> List[CutPiece]:
        """Generate bill of materials for bed frame"""
        self.clear_materials()
        
        # Posts - 4x4
        self.add_material("4x4", height + 10, 2, "Foot posts")  # Regular height
        self.add_material("4x4", min(48, height + 22), 2, "Head posts")  # Taller for headboard
        
        # Rails - 2x10
        self.add_material("2x10", length - 7, 2, "Side rails")
        self.add_material("2x10", width - 7, 2, "Head/foot rails")
        
        # Center support - 2x6
        self.add_material("2x6", length - 7, 1, "Center support beam")
        
        # Slats - 1x4
        num_slats = max(9, int(length / 8))
        self.add_material("1x4", width - 7, num_slats, "Support slats")
        
        # Headboard
        self.add_material("2x4", min(48, height + 22), 2, "Headboard posts")
        self.add_material("2x6", width, 3, "Headboard rails")
        self.add_material("1x4", min(48, height + 22) - 7, 5, "Headboard slats")
        
        return self._convert_to_cut_pieces()
    
    def generate_bookshelf_bom(self, length: float, width: float, height: float) -> List[CutPiece]:
        """Generate bill of materials for bookshelf"""
        self.clear_materials()
        
        # Sides - 1x12
        self.add_material("1x12", height, 2, "Side panels")
        
        # Shelves - 1x12
        num_shelves = max(3, min(8, int(height / 12)))
        self.add_material("1x12", length - 1.5, num_shelves, "Shelves")
        
        # Back support - 1x4
        self.add_material("1x4", height, 2, "Back vertical supports")
        self.add_material("1x4", length - 1.5, 2, "Back horizontal supports")
        
        # Face frame (optional for tall shelves)
        if height > 48:
            self.add_material("1x2", length, 2, "Face frame rails")
        
        return self._convert_to_cut_pieces()
    
    def _convert_to_cut_pieces(self) -> List[CutPiece]:
        """Convert materials to cut pieces"""
        cut_pieces = []
        for mat in self.materials:
            cut_pieces.append(CutPiece(
                length=mat.length,
                lumber_type=mat.lumber_type,
                quantity=mat.quantity,
                label=mat.purpose
            ))
        
        return cut_pieces
    
    def generate_shopping_list(self, optimized_cuts: Dict[str, List]) -> Dict[str, Any]:
        """Generate shopping list from optimized cuts"""
        shopping_list: Dict[str, Any] = {
            'lumber': {},
            'total_cost': 0,
            'items': []
        }
        
        # Load prices
        with open('config/lumber_prices.json', 'r') as f:
            prices = json.load(f)['lumber_prices']
        
        # Count required boards by type and length
        for lumber_type, stocks in optimized_cuts.items():
            if lumber_type not in shopping_list['lumber']:
                shopping_list['lumber'][lumber_type] = {}
            
            for stock in stocks:
                length_feet = int(stock.length / 12)
                length_key = f"{length_feet}'"
                
                if length_key not in shopping_list['lumber'][lumber_type]:
                    shopping_list['lumber'][lumber_type][length_key] = {
                        'quantity': 0,
                        'unit_price': prices[lumber_type][str(length_feet)],
                        'subtotal': 0
                    }
                
                shopping_list['lumber'][lumber_type][length_key]['quantity'] += 1
        
        # Calculate totals and create item list
        for lumber_type, lengths in shopping_list['lumber'].items():
            for length, info in lengths.items():
                info['subtotal'] = info['quantity'] * info['unit_price']
                shopping_list['total_cost'] += info['subtotal']
                
                shopping_list['items'].append({
                    'description': f"{lumber_type} x {length}",
                    'quantity': info['quantity'],
                    'unit_price': info['unit_price'],
                    'subtotal': info['subtotal']
                })
        
        # Add other supplies
        shopping_list['other_supplies'] = [
            {'item': 'Wood screws (3" deck screws)', 'quantity': '2 lbs', 'est_cost': 15.00},
            {'item': 'Wood glue', 'quantity': '1 bottle', 'est_cost': 8.00},
            {'item': 'Sandpaper (80, 120, 220 grit)', 'quantity': '1 pack each', 'est_cost': 12.00},
            {'item': 'Wood finish/polyurethane', 'quantity': '1 quart', 'est_cost': 20.00}
        ]
        
        shopping_list['estimated_total'] = shopping_list['total_cost'] + sum(
            item['est_cost'] for item in shopping_list['other_supplies']
        )
        
        return shopping_list
    
    def format_bom_text(self) -> str:
        """Format bill of materials as text"""
        lines: List[str] = ["BILL OF MATERIALS", "=" * 50, ""]
        
        # Group by lumber type
        by_type: Dict[str, List[Material]] = {}
        for mat in self.materials:
            if mat.lumber_type not in by_type:
                by_type[mat.lumber_type] = []
            by_type[mat.lumber_type].append(mat)
        
        # Format each group
        for lumber_type, materials in by_type.items():
            lines.append(f"{lumber_type}:")
            for mat in materials:
                lines.append(f"  {mat.quantity}x @ {mat.length}\" - {mat.purpose}")
            lines.append("")
        
        return "\n".join(lines)