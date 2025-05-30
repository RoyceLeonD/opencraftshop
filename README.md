# OpenCraftShop

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.10+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/docker-required-blue.svg" alt="Docker">
  <img src="https://img.shields.io/badge/OpenSCAD-2021.01+-orange.svg" alt="OpenSCAD">
</p>

I can't cut straight. This generates woodworking plans so I don't waste as much lumber.

## What It Does

- Generates cut lists and 3D models for basic furniture
- Optimizes material usage (because wood is expensive)
- Works for workbenches, storage benches, bed frames, bookshelves
- Terminal-based. No fancy UI.

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