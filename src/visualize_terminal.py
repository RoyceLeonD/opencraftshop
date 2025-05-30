#!/usr/bin/env python3
from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text
from rich.layout import Layout
from rich import box
import json

class TerminalVisualizer:
    def __init__(self) -> None:
        self.console: Console = Console()
    
    def draw_ascii_furniture(self, furniture_type: str, length: float, width: float, height: float) -> str:
        """Create simple ASCII representation of furniture"""
        if furniture_type == 'workbench':
            return self.draw_ascii_workbench(length, width, height)
        elif furniture_type == 'storage_bench':
            return self.draw_ascii_storage_bench(length, width, height)
        elif furniture_type == 'bed_frame':
            return self.draw_ascii_bed(length, width, height)
        elif furniture_type == 'bookshelf':
            return self.draw_ascii_bookshelf(length, width, height)
        else:
            return self.draw_ascii_workbench(length, width, height)
    
    def draw_ascii_workbench(self, length: float, width: float, height: float) -> str:
        """Create simple ASCII representation of workbench"""
        # Scale factors for ASCII art
        scale_l: int = int(length / 10)
        scale_w: int = int(width / 8)
        scale_h: int = int(height / 10)
        
        # Create ASCII art
        lines: List[str] = []
        lines.append("WORKBENCH - TOP VIEW")
        lines.append("=" * (scale_l + 4))
        
        # Top view
        for _ in range(scale_w):
            lines.append("|" + " " * scale_l + "|")
        lines.append("=" * (scale_l + 4))
        
        lines.append(f"\nDimensions: {length}\" L x {width}\" W x {height}\" H")
        
        # Side view
        lines.append("\nWORKBENCH - SIDE VIEW")
        lines.append("_" * scale_l)
        lines.append("|" + "_" * (scale_l - 2) + "|")
        for _ in range(scale_h - 1):
            lines.append("|" + " " * (scale_l - 2) + "|")
        lines.append("|_" + "_" * (scale_l - 3) + "_|")
        
        return "\n".join(lines)
    
    def draw_ascii_storage_bench(self, length: float, width: float, height: float) -> str:
        """Create ASCII representation of storage bench"""
        scale_l: int = int(length / 8)
        scale_w: int = int(width / 6)
        scale_h: int = int(height / 6)
        
        lines: List[str] = []
        lines.append("STORAGE BENCH - TOP VIEW")
        lines.append("┌" + "─" * scale_l + "┐")
        for _ in range(scale_w):
            lines.append("│" + " " * scale_l + "│")
        lines.append("└" + "─" * scale_l + "┘")
        
        lines.append(f"\nDimensions: {length}\" L x {width}\" W x {height}\" H")
        lines.append("Features: Lift-top storage compartment")
        
        return "\n".join(lines)
    
    def draw_ascii_bed(self, length: float, width: float, height: float) -> str:
        """Create ASCII representation of bed frame"""
        scale_l: int = int(length / 10)
        scale_w: int = int(width / 10)
        
        lines: List[str] = []
        lines.append("BED FRAME - TOP VIEW")
        lines.append("╔" + "═" * scale_l + "╗")
        lines.append("║" + "█" * scale_l + "║  <- Headboard")
        for _ in range(scale_w - 2):
            lines.append("║" + " " * scale_l + "║")
        lines.append("╚" + "═" * scale_l + "╝")
        
        lines.append(f"\nDimensions: {length}\" L x {width}\" W x {height}\" H")
        lines.append("Features: Headboard, center support, slat system")
        
        return "\n".join(lines)
    
    def draw_ascii_bookshelf(self, length: float, width: float, height: float) -> str:
        """Create ASCII representation of bookshelf"""
        scale_w: int = int(length / 6)
        scale_h: int = int(height / 10)
        
        lines: List[str] = []
        lines.append("BOOKSHELF - FRONT VIEW")
        lines.append("┌" + "─" * scale_w + "┐")
        
        # Draw shelves
        shelf_spacing: int = max(1, scale_h // 5)
        for i in range(scale_h):
            if i % shelf_spacing == 0:
                lines.append("├" + "─" * scale_w + "┤")
            else:
                lines.append("│" + " " * scale_w + "│")
        
        lines.append("└" + "─" * scale_w + "┘")
        
        lines.append(f"\nDimensions: {length}\" W x {width}\" D x {height}\" H")
        lines.append(f"Shelves: {max(3, min(8, int(height / 12)))}")
        
        return "\n".join(lines)
    
    def display_cut_list(self, cut_list: Dict[str, Any]) -> None:
        """Display optimized cut list in a formatted table"""
        self.console.print("\n[bold cyan]OPTIMIZED CUT LIST[/bold cyan]\n")
        
        for lumber_type, data in cut_list.items():
            if lumber_type == 'summary':
                continue
                
            table = Table(title=f"{lumber_type} Cuts", box=box.ROUNDED)
            table.add_column("Stock #", style="cyan")
            table.add_column("Length", style="green")
            table.add_column("Cuts", style="yellow")
            table.add_column("Waste", style="red")
            table.add_column("Efficiency", style="magenta")
            
            for stock in data['stocks']:
                cuts_str: str = "\n".join([f"{cut[0]}\" - {cut[1]}" for cut in stock['cuts']])
                table.add_row(
                    str(stock['stock_number']),
                    f"{stock['length']}\" ({stock['length_feet']}\')",
                    cuts_str,
                    f"{stock['waste']:.2f}\"",
                    f"{stock['efficiency']:.1f}%"
                )
            
            self.console.print(table)
            self.console.print(f"Total {lumber_type} waste: {data['total_waste']:.2f}\" | Cost: ${data['total_cost']:.2f}\n")
    
    def display_shopping_list(self, shopping_list: Dict[str, Any]) -> None:
        """Display shopping list in a formatted table"""
        self.console.print("\n[bold green]SHOPPING LIST[/bold green]\n")
        
        # Lumber table
        table = Table(title="Lumber Required", box=box.ROUNDED)
        table.add_column("Item", style="cyan")
        table.add_column("Quantity", style="yellow")
        table.add_column("Unit Price", style="green")
        table.add_column("Subtotal", style="magenta")
        
        for item in shopping_list['items']:
            table.add_row(
                item['description'],
                str(item['quantity']),
                f"${item['unit_price']:.2f}",
                f"${item['subtotal']:.2f}"
            )
        
        table.add_row("", "", "[bold]Total:[/bold]", f"[bold]${shopping_list['total_cost']:.2f}[/bold]")
        self.console.print(table)
        
        # Other supplies
        self.console.print("\n[bold]Other Supplies:[/bold]")
        for supply in shopping_list['other_supplies']:
            self.console.print(f"  • {supply['item']}: {supply['quantity']} (~${supply['est_cost']:.2f})")
        
        self.console.print(f"\n[bold green]ESTIMATED TOTAL: ${shopping_list['estimated_total']:.2f}[/bold green]")
    
    def display_summary(self, cut_list: Dict[str, Any], dimensions: Dict[str, Any]) -> None:
        """Display project summary"""
        summary: Dict[str, Any] = cut_list.get('summary', {})
        furniture_type: str = dimensions.get('type', 'workbench')
        display_name: str = furniture_type.replace('_', ' ').title()
        
        panel_content: str = f"""[bold]{display_name} Design Summary[/bold]
        
Type: {display_name}
Dimensions: {dimensions['length']}\" L x {dimensions['width']}\" W x {dimensions['height']}\" H

[bold]Material Efficiency:[/bold]
Total Waste: {summary.get('total_waste_inches', 0):.2f}\" ({summary.get('total_waste_feet', 0):.2f}')
Overall Efficiency: {summary.get('efficiency', 0):.1f}%
Total Material Cost: ${summary.get('total_cost', 0):.2f}
"""
        
        self.console.print(Panel(panel_content, title="Project Summary", border_style="blue"))
    
    def display_cut_diagram(self, optimized_cuts: Dict[str, Any]) -> None:
        """Display ASCII cut diagrams for each stock piece"""
        self.console.print("\n[bold yellow]CUT DIAGRAMS[/bold yellow]\n")
        
        for lumber_type, data in optimized_cuts.items():
            if lumber_type == 'summary':
                continue
                
            self.console.print(f"[bold]{lumber_type}:[/bold]")
            
            # Get the stocks list from the data dictionary
            stocks: List[Dict[str, Any]] = data.get('stocks', [])
            
            for stock in stocks:
                if isinstance(stock, dict):
                    length = stock['length']
                    cuts = stock['cuts']
                    stock_num = stock['stock_number']
                else:
                    length = stock.length
                    cuts = stock.cuts
                    stock_num = stocks.index(stock) + 1
                
                # Create ASCII diagram
                scale: int = 60  # characters for full length
                scale_factor: float = scale / length
                
                diagram: str = f"Stock #{stock_num} ({length}\" / {int(length/12)}')\n"
                diagram += "├" + "─" * scale + "┤\n"
                
                # Draw cuts
                cut_line: str = "│"
                label_line: str = " "
                pos: float = 0
                
                for cut_length, label in cuts:
                    cut_chars: int = int(cut_length * scale_factor)
                    cut_line += "█" * cut_chars + "│"
                    
                    # Center label
                    label_text: str = f"{cut_length}\""
                    padding: int = (cut_chars - len(label_text)) // 2
                    label_line += " " * padding + label_text + " " * (cut_chars - padding - len(label_text)) + " "
                    
                    pos += cut_length
                
                # Add waste
                waste: float = length - pos
                if waste > 0:
                    waste_chars: int = scale - len(cut_line) + 1
                    cut_line += "░" * waste_chars + "│"
                    label_line += f" waste: {waste:.1f}\""
                
                diagram += cut_line + "\n"
                diagram += label_line + "\n\n"
                
                self.console.print(diagram)