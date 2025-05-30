#!/usr/bin/env python3
"""
OpenCraftShop - Cut Optimization Engine
Implements First-Fit Decreasing bin packing algorithm for lumber optimization

Copyright (c) 2024 OpenCraftShop Contributors
Licensed under the MIT License
"""

import json
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
import numpy as np

@dataclass
class CutPiece:
    length: float
    lumber_type: str
    quantity: int
    label: str

@dataclass
class Stock:
    length: float
    lumber_type: str
    cuts: List[Tuple[float, str]] = field(default_factory=list)
    
    @property
    def waste(self) -> float:
        used: float = sum(cut[0] for cut in self.cuts)
        return self.length - used

class CutOptimizer:
    def __init__(self, kerf: float = 0.125) -> None:
        self.kerf: float = kerf
        self.standard_lengths: List[int] = [96, 120, 144, 192]  # 8', 10', 12', 16'
        
    def optimize(self, cut_list: List[CutPiece]) -> Dict[str, List[Stock]]:
        """Optimize cuts using first-fit decreasing bin packing algorithm"""
        results: Dict[str, List[Stock]] = {}
        
        # Group by lumber type
        by_type: Dict[str, List[Tuple[float, str]]] = {}
        for piece in cut_list:
            if piece.lumber_type not in by_type:
                by_type[piece.lumber_type] = []
            for _ in range(piece.quantity):
                by_type[piece.lumber_type].append((piece.length, piece.label))
        
        # Optimize each lumber type
        for lumber_type, pieces in by_type.items():
            # Sort pieces by length (descending)
            pieces.sort(key=lambda x: x[0], reverse=True)
            
            stocks: List[Stock] = []
            for length, label in pieces:
                placed: bool = False
                
                # Try to fit in existing stock
                for stock in stocks:
                    if stock.waste >= length + self.kerf:
                        stock.cuts.append((length, label))
                        placed = True
                        break
                
                # If not placed, find optimal new stock
                if not placed:
                    for std_length in self.standard_lengths:
                        if std_length >= length + self.kerf:
                            new_stock: Stock = Stock(std_length, lumber_type)
                            new_stock.cuts.append((length, label))
                            stocks.append(new_stock)
                            break
            
            results[lumber_type] = stocks
        
        return results
    
    def generate_cut_list(self, optimized: Dict[str, List[Stock]]) -> Dict[str, Any]:
        """Generate detailed cut list with statistics"""
        cut_list: Dict[str, Any] = {}
        total_waste: float = 0
        total_cost: float = 0
        
        # Load prices
        with open('config/lumber_prices.json', 'r') as f:
            prices: Dict[str, Dict[str, float]] = json.load(f)['lumber_prices']
        
        for lumber_type, stocks in optimized.items():
            cut_list[lumber_type] = {
                'stocks': [],
                'total_stocks': len(stocks),
                'total_waste': 0,
                'total_cost': 0
            }
            
            for i, stock in enumerate(stocks):
                stock_info: Dict[str, Any] = {
                    'stock_number': i + 1,
                    'length': stock.length,
                    'length_feet': stock.length / 12,
                    'cuts': stock.cuts,
                    'waste': stock.waste,
                    'efficiency': (1 - stock.waste / stock.length) * 100
                }
                
                # Calculate cost
                length_feet: int = int(stock.length / 12)
                if lumber_type in prices and str(length_feet) in prices[lumber_type]:
                    stock_cost: float = prices[lumber_type][str(length_feet)]
                    stock_info['cost'] = stock_cost
                    cut_list[lumber_type]['total_cost'] += stock_cost
                
                cut_list[lumber_type]['stocks'].append(stock_info)
                cut_list[lumber_type]['total_waste'] += stock.waste
                total_waste += stock.waste
            
            total_cost += cut_list[lumber_type]['total_cost']
        
        cut_list['summary'] = {
            'total_waste_inches': total_waste,
            'total_waste_feet': total_waste / 12,
            'total_cost': total_cost,
            'efficiency': (1 - total_waste / sum(s.length for stocks in optimized.values() for s in stocks)) * 100
        }
        
        return cut_list