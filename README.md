# OpenCraftShop

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.10+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/docker-required-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/OpenSCAD-2021.01+-orange.svg" alt="OpenSCAD">
</p>

I can't measure. This turns "I want a bookshelf" into an actual shopping list and plan.

## What It Actually Does

- **Generates bills of materials** - Tells you exactly what to buy at the lumber yard
- **Creates parametric designs** - Change dimensions, get new plans instantly  
- **Produces cut lists** - Which boards to cut and how (optimization is just a bonus)
- **Makes 3D models** - So you can see what you're building before you screw it up
- **Calculates costs** - Know how much money you're about to waste

The real value: It does the thinking so you can focus on the building (and subsequent fixing).

## Quick Start

```bash
git clone https://github.com/RoyceLeonD/opencraftshop.git
cd opencraftshop
make run

# Make specific furniture
make bookshelf
make bed
make storage-bench

# Custom dimensions
docker-compose run workbench-designer --type bookshelf --height 48 --width 24
```

## Web UI (New!)

For a visual design experience with real-time 3D preview:

```bash
# Start the web interface
./examples/run_web_ui.sh

# Or manually:
docker-compose up -d web
```

Then open http://localhost:5000 in your browser. Features:
- Interactive 3D model viewer
- Dropdown furniture selection
- Real-time dimension adjustments
- Download generated files directly
- No terminal ASCII art needed!

## Installation

Requires:
- Docker and docker-compose
- Git

```bash
git clone https://github.com/RoyceLeonD/opencraftshop.git
cd opencraftshop
make build
```

## Usage

```bash
# Default bookshelf
docker-compose run workbench-designer --type bookshelf

# Custom size
docker-compose run workbench-designer --type bed_frame --length 75 --width 54

# Skip visualization
docker-compose run workbench-designer --type workbench --no-visualize
```

### Options

| Option | What | Default |
|--------|------|---------|
| `--type` | Furniture type | workbench |
| `--length` | Length in inches | Varies |
| `--width` | Width in inches | Varies |
| `--height` | Height in inches | Varies |
| `--kerf` | Saw blade width | 0.125" |
| `--output-dir` | Output location | ./output |

## Output

Generates in `./output/`:
- `.stl` - 3D model
- `.scad` - OpenSCAD source
- `bill_of_materials.txt` - What to buy
- `cut_list.txt` - How to cut it
- `shopping_list.txt` - Take to store

## How It Works

Uses First-Fit Decreasing algorithm to minimize waste. Gets 70-85% material efficiency. Better than eyeballing it.

## Project Structure

```
opencraftshop/
├── src/
│   ├── templates/        # OpenSCAD furniture templates
│   ├── main.py          # Entry point
│   ├── optimize_cuts.py # Cut optimization
│   └── generate_bom.py  # Shopping lists
├── config/              # Lumber prices
├── output/              # Generated files
└── Dockerfile           # Container setup
```

## Testing

```bash
make test              # Run all tests
make test-dimensions   # Test sizing
make validate         # Check output files
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). New furniture templates welcome.

## License

MIT. See [LICENSE](LICENSE).

## Issues

Something broken? [File an issue](https://github.com/RoyceLeonD/opencraftshop/issues).

---

Made because I kept turning expensive wood into expensive firewood.