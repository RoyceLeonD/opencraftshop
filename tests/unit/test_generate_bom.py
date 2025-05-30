"""Unit tests for BOM generation module."""
import pytest
from typing import List

from src.generate_bom import BOMGenerator, CutPiece


class TestCutPiece:
    """Test cases for CutPiece class."""
    
    def test_cut_piece_creation(self):
        """Test CutPiece object creation."""
        piece = CutPiece("2x4", 48.0, 2, "Test legs")
        
        assert piece.lumber_type == "2x4"
        assert piece.length == 48.0
        assert piece.quantity == 2
        assert piece.purpose == "Test legs"
    
    def test_cut_piece_string_representation(self):
        """Test string representation of CutPiece."""
        piece = CutPiece("2x6", 72.0, 1, "Top rail")
        str_repr = str(piece)
        
        assert "2x6" in str_repr
        assert "72.0" in str_repr
        assert "Top rail" in str_repr


class TestBOMGenerator:
    """Test cases for BOMGenerator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = BOMGenerator()
    
    def test_init_empty_materials(self):
        """Test BOMGenerator starts with empty materials list."""
        assert self.generator.materials == []
    
    def test_actual_dimensions_mapping(self):
        """Test nominal to actual dimension conversion."""
        actual_dims = self.generator.ACTUAL_DIMENSIONS
        
        # Check common sizes
        assert actual_dims["2x4"] == (1.5, 3.5)
        assert actual_dims["2x6"] == (1.5, 5.5)
        assert actual_dims["1x4"] == (0.75, 3.5)
        assert actual_dims["4x4"] == (3.5, 3.5)
    
    def test_add_material(self):
        """Test adding materials to BOM."""
        self.generator.add_material("2x4", 48.0, 4, "Legs")
        
        assert len(self.generator.materials) == 1
        assert self.generator.materials[0].lumber_type == "2x4"
        assert self.generator.materials[0].quantity == 4
    
    def test_clear_materials(self):
        """Test clearing materials list."""
        self.generator.add_material("2x4", 48.0, 4, "Legs")
        self.generator.add_material("2x6", 60.0, 2, "Top")
        
        assert len(self.generator.materials) == 2
        
        self.generator.clear_materials()
        assert len(self.generator.materials) == 0
    
    def test_get_materials(self):
        """Test getting materials list."""
        self.generator.add_material("2x4", 48.0, 4, "Legs")
        materials = self.generator.get_materials()
        
        assert len(materials) == 1
        assert isinstance(materials[0], CutPiece)
    
    def test_workbench_bom_generation(self):
        """Test workbench BOM generation."""
        pieces = self.generator.generate_workbench_bom(60.0, 24.0, 36.0)
        
        # Check that we have pieces
        assert len(pieces) > 0
        
        # Check for expected components
        purposes = [p.purpose for p in pieces]
        assert any("leg" in p.lower() for p in purposes)
        assert any("stretcher" in p.lower() or "rail" in p.lower() for p in purposes)
        assert any("top" in p.lower() for p in purposes)
        
        # Check quantities make sense
        legs = [p for p in pieces if "leg" in p.purpose.lower()]
        assert sum(p.quantity for p in legs) == 4  # 4 legs for a workbench
    
    def test_storage_bench_bom_generation(self):
        """Test storage bench BOM generation."""
        pieces = self.generator.generate_storage_bench_bom(48.0, 18.0, 18.0)
        
        assert len(pieces) > 0
        
        # Check for storage bench specific components
        purposes = [p.purpose for p in pieces]
        assert any("leg" in p.lower() for p in purposes)
        assert any("panel" in p.lower() or "side" in p.lower() for p in purposes)
    
    def test_bed_frame_bom_generation(self):
        """Test bed frame BOM generation."""
        # Queen size bed
        pieces = self.generator.generate_bed_frame_bom(80.0, 60.0, 14.0)
        
        assert len(pieces) > 0
        
        # Check for bed frame components
        purposes = [p.purpose for p in pieces]
        assert any("rail" in p.lower() for p in purposes)
        assert any("slat" in p.lower() for p in purposes)
        
        # Bed should have multiple slats
        slats = [p for p in pieces if "slat" in p.purpose.lower()]
        assert len(slats) > 0
        assert sum(p.quantity for p in slats) >= 5  # At least 5 slats
    
    def test_bookshelf_bom_generation(self):
        """Test bookshelf BOM generation."""
        pieces = self.generator.generate_bookshelf_bom(36.0, 12.0, 72.0)
        
        assert len(pieces) > 0
        
        # Check for bookshelf components
        purposes = [p.purpose for p in pieces]
        assert any("side" in p.lower() or "panel" in p.lower() for p in purposes)
        assert any("shelf" in p.lower() for p in purposes)
        
        # Should have multiple shelves
        shelves = [p for p in pieces if "shelf" in p.purpose.lower()]
        total_shelves = sum(p.quantity for p in shelves)
        assert total_shelves >= 4  # At least 4 shelves including top/bottom
    
    def test_invalid_dimensions(self):
        """Test BOM generation with invalid dimensions."""
        # Negative dimensions should be handled gracefully
        pieces = self.generator.generate_workbench_bom(-60.0, 24.0, 36.0)
        # Should still generate something or raise appropriate error
        
        # Zero dimensions
        pieces = self.generator.generate_workbench_bom(60.0, 0.0, 36.0)
        # Should handle edge case
    
    def test_lumber_type_variety(self):
        """Test that different furniture uses appropriate lumber types."""
        workbench_pieces = self.generator.generate_workbench_bom(60.0, 24.0, 36.0)
        workbench_types = set(p.lumber_type for p in workbench_pieces)
        
        bookshelf_pieces = self.generator.generate_bookshelf_bom(36.0, 12.0, 72.0)
        bookshelf_types = set(p.lumber_type for p in bookshelf_pieces)
        
        # Different furniture should use different lumber combinations
        assert "2x4" in workbench_types  # Structural support
        assert "1x12" in bookshelf_types or "1x10" in bookshelf_types  # Shelving