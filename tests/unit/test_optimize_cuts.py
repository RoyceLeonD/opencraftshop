"""Unit tests for cut optimization module."""
import pytest
from typing import List

from src.optimize_cuts import CutOptimizer, OptimizationResult
from src.generate_bom import CutPiece


class TestCutOptimizer:
    """Test cases for CutOptimizer class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.optimizer = CutOptimizer(kerf=0.125)
    
    def test_init_default_kerf(self):
        """Test default kerf width."""
        opt = CutOptimizer()
        assert opt.kerf == 0.125
    
    def test_init_custom_kerf(self):
        """Test custom kerf width."""
        opt = CutOptimizer(kerf=0.25)
        assert opt.kerf == 0.25
    
    def test_empty_pieces_list(self):
        """Test optimization with empty pieces list."""
        result = self.optimizer.optimize([])
        assert result.boards == []
        assert result.total_boards == 0
        assert result.total_waste == 0
        assert result.efficiency == 100.0
    
    def test_single_piece_fits(self):
        """Test single piece that fits in standard board."""
        pieces = [CutPiece("2x4", 48.0, 1, "Test")]
        result = self.optimizer.optimize(pieces)
        
        assert result.total_boards == 1
        assert len(result.boards) == 1
        assert result.boards[0]["length"] == 96
        assert len(result.boards[0]["pieces"]) == 1
    
    def test_multiple_pieces_one_board(self):
        """Test multiple pieces that fit in one board."""
        pieces = [
            CutPiece("2x4", 24.0, 1, "Piece 1"),
            CutPiece("2x4", 24.0, 1, "Piece 2"),
            CutPiece("2x4", 24.0, 1, "Piece 3"),
        ]
        result = self.optimizer.optimize(pieces)
        
        assert result.total_boards == 1
        # Account for kerf: 24 + 24 + 24 + (2 * 0.125) = 72.25 < 96
    
    def test_kerf_consideration(self):
        """Test that kerf is properly considered."""
        # Two 48" pieces with kerf should not fit in 96" board
        pieces = [
            CutPiece("2x4", 48.0, 1, "Piece 1"),
            CutPiece("2x4", 48.0, 1, "Piece 2"),
        ]
        result = self.optimizer.optimize(pieces)
        
        # 48 + 48 + 0.125 = 96.125 > 96, so need 2 boards
        assert result.total_boards == 2
    
    def test_sorting_by_length(self):
        """Test that pieces are sorted by length (FFD algorithm)."""
        pieces = [
            CutPiece("2x4", 24.0, 1, "Small"),
            CutPiece("2x4", 72.0, 1, "Large"),
            CutPiece("2x4", 48.0, 1, "Medium"),
        ]
        result = self.optimizer.optimize(pieces)
        
        # Largest piece should be placed first
        first_board = result.boards[0]
        assert first_board["pieces"][0]["length"] == 72.0
    
    def test_very_long_piece(self):
        """Test piece longer than standard board lengths."""
        pieces = [CutPiece("2x4", 200.0, 1, "Very long")]
        
        with pytest.raises(ValueError, match="exceeds maximum"):
            self.optimizer.optimize(pieces)
    
    def test_efficiency_calculation(self):
        """Test waste and efficiency calculations."""
        # One 48" piece from 96" board = 50% efficiency
        pieces = [CutPiece("2x4", 48.0, 1, "Half board")]
        result = self.optimizer.optimize(pieces)
        
        assert result.total_waste == 48.0
        assert result.efficiency == 50.0
    
    def test_multiple_lumber_types(self):
        """Test optimization with different lumber types."""
        pieces = [
            CutPiece("2x4", 48.0, 1, "2x4 piece"),
            CutPiece("2x6", 48.0, 1, "2x6 piece"),
            CutPiece("2x4", 24.0, 1, "Another 2x4"),
        ]
        result = self.optimizer.optimize(pieces)
        
        # Should group by lumber type
        boards_2x4 = [b for b in result.boards if b["lumber_type"] == "2x4"]
        boards_2x6 = [b for b in result.boards if b["lumber_type"] == "2x6"]
        
        assert len(boards_2x4) >= 1
        assert len(boards_2x6) >= 1
    
    def test_optimal_board_length_selection(self):
        """Test selection of optimal board lengths."""
        # 120" of cuts might fit better in 144" board than two 96" boards
        pieces = [
            CutPiece("2x4", 60.0, 1, "Piece 1"),
            CutPiece("2x4", 60.0, 1, "Piece 2"),
        ]
        result = self.optimizer.optimize(pieces)
        
        # Should use one 144" board instead of two 96" boards
        assert result.total_boards == 1
        assert result.boards[0]["length"] == 144