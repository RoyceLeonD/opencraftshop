# OpenCraftShop Architecture

## System Overview

OpenCraftShop is a parametric woodworking design system that combines 3D modeling, optimization algorithms, and cost estimation to help woodworkers plan projects efficiently.

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Input    │────▶│   Main CLI       │────▶│   Outputs       │
│  (dimensions)   │     │   (main.py)      │     │  (.scad, .txt)  │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │ BOM Generator│      │OpenSCAD      │
             │(generate_bom)│      │Templates     │
             └──────────────┘      └──────────────┘
                    │                     │
                    ▼                     ▼
             ┌──────────────┐      ┌──────────────┐
             │Cut Optimizer │      │3D Model      │
             │(optimize_cuts)│      │(.stl export) │
             └──────────────┘      └──────────────┘
                    │
                    ▼
             ┌──────────────┐
             │ Visualizer   │
             │(ASCII output)│
             └──────────────┘
```

## Core Components

### 1. Main CLI (`src/main.py`)
**Purpose**: Orchestrates the entire workflow
- Parses command-line arguments
- Loads configuration files
- Coordinates between components
- Manages output generation

**Key Functions**:
- `generate_design()`: Main entry point
- Parameter validation and defaults
- File I/O management

### 2. BOM Generator (`src/generate_bom.py`)
**Purpose**: Creates bill of materials for furniture projects
- Calculates required lumber pieces
- Accounts for actual vs nominal dimensions
- Supports multiple furniture types

**Key Classes**:
- `CutPiece`: Represents a single piece of lumber
- `BOMGenerator`: Main class with furniture-specific methods

**Algorithms**:
- Lumber dimension mapping (nominal to actual)
- Material requirement calculation
- Part grouping and naming

### 3. Cut Optimizer (`src/optimize_cuts.py`)
**Purpose**: Minimizes waste when cutting lumber
- Implements First-Fit Decreasing (FFD) bin packing
- Accounts for saw kerf (blade width)
- Optimizes for standard lumber lengths

**Key Classes**:
- `CutOptimizer`: Main optimization class
- `OptimizationResult`: Results container

**Algorithm Details**:
```python
# FFD Bin Packing Algorithm
1. Sort pieces by length (descending)
2. For each piece:
   a. Try to fit in existing boards
   b. If no fit, use new board
3. Calculate waste and efficiency
```

### 4. Terminal Visualizer (`src/visualize_terminal.py`)
**Purpose**: Provides rich terminal output
- ASCII art diagrams
- Color-coded cut lists
- Progress indicators
- Summary statistics

**Key Features**:
- Rich library integration
- Responsive table layouts
- Visual cut diagrams

### 5. OpenSCAD Templates (`src/templates/`)
**Purpose**: Parametric 3D models
- Modular design components
- Accurate lumber dimensions
- Exportable to STL/DXF

**Template Structure**:
```scad
include <lumber_lib.scad>
// Parameters
length = 60;
width = 24;
height = 36;
// Model generation
```

## Data Flow

1. **Input Stage**
   - User provides dimensions via CLI
   - Configuration loaded from JSON/YAML
   - Parameters validated

2. **Generation Stage**
   - BOM created based on furniture type
   - Cut optimization performed
   - OpenSCAD file generated

3. **Output Stage**
   - Terminal visualization displayed
   - Files written to output directory
   - Summary statistics calculated

## Configuration

### Lumber Prices (`config/lumber_prices.json`)
```json
{
  "2x4": {"price_per_foot": 0.70},
  "2x6": {"price_per_foot": 1.10}
}
```

### Design Parameters (`config/design_params.json`)
```json
{
  "workbench": {
    "default_length": 60,
    "default_width": 24,
    "default_height": 36
  }
}
```

## Docker Integration

The system runs in a Docker container to ensure consistency:
- Python 3.11 base image
- OpenSCAD installed via apt
- Minimal dependencies
- Volume mounting for output

## Performance Considerations

1. **Cut Optimization**: O(n log n) for FFD algorithm
2. **Memory Usage**: Minimal, all calculations in-memory
3. **File I/O**: Buffered writes for large outputs
4. **OpenSCAD Rendering**: Can be slow for complex models

## Extension Points

1. **New Furniture Types**
   - Add template to `src/templates/`
   - Add BOM method to `BOMGenerator`
   - Update CLI choices

2. **New Optimization Algorithms**
   - Implement new class following `CutOptimizer` interface
   - Add algorithm selection to CLI

3. **Export Formats**
   - Add new output handlers
   - Integrate with external tools

## Error Handling

- Input validation at CLI level
- Graceful fallbacks for missing configs
- Detailed error messages
- Non-zero exit codes for scripts

## Testing Strategy

1. **Unit Tests**: Component-level testing
2. **Integration Tests**: Full workflow validation
3. **Dimension Tests**: Boundary condition checking
4. **Performance Tests**: Optimization benchmarks