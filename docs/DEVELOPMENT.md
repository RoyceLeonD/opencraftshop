# Development Guide for Fellow Code Monkeys 🐒

Welcome to the developer docs! If you're reading this, you're either contributing (THANK YOU!) or you're trying to figure out what the heck I did here. Either way, let me explain this beautiful mess.

## 🏗️ Architecture (Using That Word Loosely)

Here's how this Frankenstein's monster works:

```
User: "I want a bookshelf"
  ↓
CLI (main.py): "Roger that, let me ask the boys"
  ↓
OpenSCAD: "I'll make it 3D and perfect"
  ↓
Optimizer: "I'll make sure you don't waste wood like usual"
  ↓
Terminal UI: "I'll draw pretty pictures"
  ↓
User: "Wow, it's actually straight!" 🎉
```

## 🗂️ Project Structure Explained

```
opencraftshop/
├── src/
│   ├── main.py              # The boss - orchestrates everything
│   ├── templates/           # OpenSCAD files (the actual furniture)
│   │   ├── bookshelf.scad   # My nemesis turned friend
│   │   ├── workbench.scad   # Where I make other mistakes
│   │   └── ...              # More furniture I can't build IRL
│   ├── optimize_cuts.py     # The math wizard (saves money!)
│   ├── generate_bom.py      # Shopping list generator
│   ├── visualize_terminal.py # ASCII art because why not
│   └── utils.py             # Random helpful stuff
├── config/
│   ├── lumber_prices.json   # Prepare to cry at these prices
│   └── furniture_dimensions.json # Default sizes (adjustable!)
├── tests/                   # Proof it works (sometimes)
├── output/                  # Your golden tickets appear here
└── Dockerfile              # Container magic for consistency
```

## 🛠️ Setting Up Your Dev Environment

### The Easy Way (Docker)

```bash
# Just use Docker like I do
make build
make shell  # Hop into the container
```

### The Hard Way (Local)

```bash
# Install Python 3.10+ (I use 3.10 because I'm scared of change)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install OpenSCAD (this is the fun part)
# Mac: brew install openscad
# Linux: sudo apt-get install openscad
# Windows: Download from openscad.org and pray
```

## 🧪 Testing (Yes, I Actually Write Tests Now)

After breaking production one too many times, I learned my lesson:

```bash
# Run all tests
make test

# Run specific test file
python -m pytest tests/test_optimizer.py

# Run with coverage (impress your friends)
python -m pytest --cov=src tests/

# Quick smoke test
make quick-test
```

### Test Categories

- **Unit Tests**: Test individual functions (when I remember to write them)
- **Integration Tests**: Make sure pieces work together
- **Dimension Tests**: Ensure we don't create 90-foot bookshelves
- **Output Tests**: Verify files actually appear

## 🔧 Core Components Deep Dive

### 1. The CLI (main.py)

This is where the magic starts. It's basically a fancy argument parser:

```python
# How it works (simplified because the real code is messier)
def main():
    args = parse_args()  # What does the user want?
    validate_dimensions(args)  # Are they insane?
    generate_scad(args)  # Make the 3D model
    optimize_cuts(args)  # Save some trees
    create_outputs(args)  # Make all the files
    celebrate()  # We did it!
```

### 2. OpenSCAD Templates

These define the actual furniture. Example structure:

```scad
// bookshelf.scad - My first success story
module bookshelf(width, height, depth, shelf_count) {
    // Magic happens here
    // Lots of cubes and transforms
    // Somehow it works
}
```

Tips for writing templates:
- Start simple (box with shelves)
- Test with default dimensions first
- Use parameters for EVERYTHING
- Comment like your life depends on it

### 3. The Optimizer (optimize_cuts.py)

This is where I pretend to be smart:

```python
def optimize_cuts(pieces, board_length, kerf_width):
    """
    Uses First-Fit Decreasing algorithm.
    
    I spent 3 days on this after wasting $200 on wood.
    It's not perfect but it's better than eyeballing it.
    """
    # Sort pieces by size (revolutionary!)
    pieces.sort(reverse=True)
    
    # Pack them into boards
    boards = []
    for piece in pieces:
        # Find a board it fits on
        placed = False
        for board in boards:
            if board.can_fit(piece + kerf_width):
                board.add(piece)
                placed = True
                break
        
        if not placed:
            # Need a new board (cha-ching!)
            new_board = Board(board_length)
            new_board.add(piece)
            boards.append(new_board)
    
    return boards
```

### 4. Terminal Visualizer

Because ASCII art makes everything better:

```python
def draw_furniture(dimensions):
    """
    Makes pretty pictures in your terminal.
    
    Way harder than it should be, but looks cool.
    """
    # Lots of box-drawing characters
    # Math to scale things properly
    # Prayer that it aligns correctly
```

## 📝 Adding New Furniture Types

Want to add a new furniture type? Here's the playbook:

### 1. Create the Template

```scad
// src/templates/coffee_table.scad
module coffee_table(length, width, height, has_shelf) {
    // Start with a top
    cube([length, width, 1]);
    
    // Add legs (4 usually works)
    leg_size = 2;
    translate([0, 0, -height])
        cube([leg_size, leg_size, height]);
    // ... more legs ...
    
    // Optional shelf
    if (has_shelf) {
        translate([0, 0, -height/2])
            cube([length-4, width-4, 0.75]);
    }
}
```

### 2. Add to Configuration

```json
// config/furniture_dimensions.json
{
    "furniture_types": {
        "coffee_table": {
            "display_name": "Coffee Table",
            "default_dimensions": {
                "length": 48,
                "width": 24,
                "height": 18
            },
            "required_pieces": {
                "top": {"length": 48, "width": 24, "thickness": 1, "quantity": 1},
                "legs": {"length": 17, "width": 2, "thickness": 2, "quantity": 4},
                "shelf": {"length": 44, "width": 20, "thickness": 0.75, "quantity": 1}
            }
        }
    }
}
```

### 3. Update the CLI

Add it to the choices in `main.py`. That's it. Seriously.

### 4. Test It!

```bash
# Generate with defaults
python src/main.py --type coffee_table

# Try edge cases
python src/main.py --type coffee_table --height 6  # Tiny table
python src/main.py --type coffee_table --width 60  # Wide boy
```

## 🐛 Debugging Tips

When things go wrong (and they will):

### Common Issues I've Hit

1. **OpenSCAD fails silently**
   - Check the .scad file manually
   - Run `openscad -o test.stl yourfile.scad` directly
   - Usually it's a missing semicolon (always is)

2. **Optimizer gives weird results**
   - Print the pieces list
   - Check your kerf width
   - Make sure dimensions make sense

3. **Terminal UI looks drunk**
   - Terminal size matters
   - Some terminals hate Unicode
   - When in doubt, `--no-visualize`

### Debug Mode

```bash
# Verbose output
python src/main.py --type bookshelf --debug

# Skip optimization (see raw requirements)
python src/main.py --type bookshelf --no-optimize

# Save intermediate files
python src/main.py --type bookshelf --save-debug-files
```

## 🚀 Performance Considerations

This isn't exactly high-performance computing, but:

- OpenSCAD can be slow for complex models
- Optimization is O(n log n) - good enough
- Terminal drawing is instant (unless your terminal is from 1995)

If things are slow:
1. Simplify the OpenSCAD model
2. Use `--no-visualize`
3. Buy a faster computer (worked for me)

## 🤝 Git Workflow

Here's how I work (feel free to improve):

```bash
# Feature branch
git checkout -b add-dining-table

# Make changes
# Write tests (I forget this step a lot)
# Test locally

# Commit with meaningful message
git add .
git commit -m "Add dining table template with extending leaves support"

# Push and PR
git push origin add-dining-table
```

## 📚 Resources & References

Stuff that helped me build this:

- [OpenSCAD Documentation](https://openscad.org/documentation.html) - Lifesaver
- [Bin Packing Algorithms](https://en.wikipedia.org/wiki/Bin_packing_problem) - Math is cool
- [Python Click Library](https://click.palletsprojects.com/) - Makes CLIs easy
- [Rich Library](https://github.com/Textualize/rich) - Terminal prettiness
- Stack Overflow - Obviously

## 🎯 Future Architecture Plans

Things I want to do when I'm feeling ambitious:

- [ ] Plugin system for furniture types
- [ ] Web UI (FastAPI maybe?)
- [ ] Database for cut history
- [ ] AI to suggest optimizations (buzzword compliance)
- [ ] 3D preview in terminal (because why not)

## 💡 Pro Developer Tips

1. **Start simple** - I began with a box. It was crooked, but it was a start.

2. **Test with real dimensions** - Use measurements from actual furniture.

3. **Document everything** - Future you is dumb (trust me, I know).

4. **Make mistakes** - I made plenty. The code got better each time.

5. **Ask for help** - The woodworking subreddits are surprisingly helpful about code.

## 🆘 When You're Stuck

- Check the tests - They show how things should work
- Read the comments - I over-comment because I forget stuff
- Open an issue - I'll help if I can
- Try the Discord - Oh wait, we don't have one. Maybe we should?

Remember: This whole project exists because I'm bad at woodworking. Your code doesn't need to be perfect - it just needs to be better than cutting by hand (low bar).

Happy coding! May your furniture be square and your tests be green! 🟩

---

*P.S. - If you make this better (which shouldn't be hard), please share. I'm always learning, and apparently, I have a lot to learn.*