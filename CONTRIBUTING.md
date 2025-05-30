# Contributing - Please Help!

I built this because I can't measure. Seriously, any help is appreciated.

## The Bar is Low (Limbo Low)

Can you:

- Read Python? You're qualified! Can't read python? Also Qualified. Seriously, just chatgpt your way though this.
- Run `make test` without crying? You're hired!
- Explain what you changed? You're a hero!
- Actually build furniture? Please teach me!

## What I Really Need Help With

### 🆘 SOS - Currently Failing At These

- **Better BOM generation** - The math is probably wrong
- **OpenSCAD parser** - Need to extract dimensions from ANY .scad file
- **Web interface** - I tried, I failed, I gave up
- **Tests that test things** - Current tests are... optimistic
- **Windows support** - Does it even work? No clue!

### 🎯 Would Make My Life Better

- **More furniture templates** - Got a design? Share it!
- **Metric support** - For the sane 95% of the world
- **"I have this wood already" mode** - Optimize for existing materials
- **Better error messages** - Current ones are useless
- **Documentation** - Explain what I did because I forgot

### 🚀 Dream Features (Help Me Dream)

- AI that turns sketches into cut lists
- "Will this wobble?" predictor
- Natural language: "I need a shelf for this corner"
- Integration with lumber yard inventory

## How to Contribute (It's Easy, I Promise)

### First Time? Start Here:

1. Find a typo? Fix it! (There are many)
2. Confused by something? Add a comment!
3. Built something? Add the template!
4. Found a bug? You probably did!

### For the Brave:

1. Pick something from the SOS list
2. Try to understand my code (sorry)
3. Make it less bad
4. Submit a PR
5. I'll love you forever

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/opencraftshop.git
cd opencraftshop

# Make a branch (name it anything)
git checkout -b fix-the-thing-that-broke

# Set up environment
make dev-setup  # Or just `pip install -r requirements.txt`

# Make changes, test them
make test  # Fingers crossed
python src/main.py --type bookshelf  # Manual test

# Submit PR
git push origin fix-the-thing-that-broke
```

## Code Guidelines (More Like Suggestions)

**The Current State:**

- Some files have types hints, some don't
- Some have tests, most don't
- Comments explain the confusing parts (everything)
- It works on my machine™

**What Would Be Nice:**

- Type hints (Future me will thank you)
- Tests (Any test > no test)
- Comments on the weird stuff
- Black formatter (or don't, I'm not picky)

**Example of Acceptable Code:**

```python
def calculate_boards_needed(length: float, count: int) -> int:
    """
    Calculate how many boards to buy.

    Add 20% because I'll definitely mess up at least one.
    """
    needed = length * count / 96  # 96" = 8ft board
    return int(needed * 1.2) + 1  # The +1 is hope
```

## Testing

```bash
# The prayer method:
make test

# What actually helps:
make test-unit      # If you wrote unit tests (hero!)
python src/main.py --type workbench  # Does it run?

# The real test:
Actually build the furniture and send pics!
```

## Pull Request Process

Your PR needs:

1. **A description** - What did you do and why?
2. **To not break everything** - Run at least one test
3. **Bonus points** - Update docs if you added features

Good PR example:

```
Fix bookshelf falling over bug

- Shelves were upside down in the BOM
- Added test to catch this
- Built one, it stands! (pic attached)
```

## Questions? Stuck? Confused?

- **Open an issue** - I'm confused too, we'll figure it out
- **Bug?** - Probably my fault, let me know
- **Feature idea?** - Yes! Tell me!
- **Built something?** - SHOW ME PICTURES

## Why Your Help Matters

Every contribution helps someone:

- Build furniture that doesn't wobble
- Save money on wood
- Feel less dumb about measuring wrong
- Actually finish a project

We're not building rockets here. We're helping people build shelves. Every little bit helps.

## The Philosophy

Perfect code < Working code < Code that helps someone build a bookshelf

The woodworking community is all about helping each other. This is just that, but with more Python and less splinters.

## Recognition

Contributors get:

- Your name in the contributors list
- My eternal gratitude
- The warm fuzzy feeling of helping fellow bad woodworkers
- Bragging rights at parties (if you go to those kinds of parties)

---

**Seriously, please help. Even fixing a typo helps. The bar is so low it's underground. Your code doesn't have to be perfect, it just has to be better than mine (not hard).**

P.S. - If you understand GitHub Actions, PLEASE fix the CI/CD. It's 90% copy-pasted from Stack Overflow.
