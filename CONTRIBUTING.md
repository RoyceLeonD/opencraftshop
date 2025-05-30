# Contributing

Look, I made this for myself but I guess you can help if you want.

## Getting Started

1. Fork the repo
2. Clone your fork
3. Make a branch: `git checkout -b whatever`
4. Change stuff
5. Test it: `make test`
6. Push it
7. Open a PR

If it breaks, fix it. If you can't, at least tell me what broke.

## What You Can Add

### New Furniture
Stick a new template in `src/templates/`. Copy an existing one. Change it until it looks right. Add the config to `config/furniture_dimensions.json`.

### Bug Fixes
Found something broken? Fix it or file an issue. Be specific. "It doesn't work" tells me nothing.

### Better Algorithms
The optimization in `src/optimize_cuts.py` works but could be better. Have at it.

## Testing

```bash
make test           # Run everything
make quick-test     # Just check if it runs
make validate       # Check output files exist
```

Tests fail sometimes. That's normal.

## Code Style

- Python: Use Black formatter. I don't care about your preferences.
- Comments: Write them. Future you will need them.
- Variables: Name them what they are. `board_length` not `bl`.

## Pull Requests

1. Make sure tests pass
2. Update docs if you changed how things work
3. Describe what you did. One line is fine.

Good PR titles:
- "Add dining table template"
- "Fix 30% wood waste bug"
- "Add metric support"

Bad PR titles:
- "Update"
- "Fix"
- "Changes"

## First Timer?

Look for `good first issue` labels. Usually simple stuff.

## Questions?

Open an issue. I'll answer when I can.

## Code of Conduct

Don't be a jerk. We're all just trying to build furniture without wasting wood.

---

Built this because I suck at woodworking. Your code doesn't need to be perfect. Just better than measuring wrong.