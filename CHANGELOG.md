# Changelog: A History of My Mistakes and Occasional Victories 📜

All notable changes to OpenCraftShop will be documented in this file. And by "notable," I mean "things I remembered to write down."

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/), but with more personality and self-deprecation.

## [Unreleased] - The Stuff I'm Breaking Right Now

### 🚧 Working On
- Dining table template (currently falls over)
- Metric support (math is hard)
- Better error messages (current ones are useless)
- My woodworking skills (no ETA on this)

## [0.1.5] - 2024-01-15 - "The One Where Nothing Caught Fire"

### ✨ Added
- Terminal visualization! Now you can see your furniture in glorious ASCII art
- `--no-visualize` flag for when the ASCII art makes you sad
- Color output because plain text was too boring
- More self-deprecating comments in the code

### 🐛 Fixed
- Fixed bug where 0-inch shelves were allowed (physics says no)
- Terminal UI no longer crashes on Windows (usually)
- Actually saves files to output directory now (revolutionary!)

### 📝 Changed
- Made error messages slightly less cryptic
- Default kerf width now actually matches common saw blades

## [0.1.4] - 2024-01-01 - "New Year, Same Bad Woodworking"

### ✨ Added
- Bed frame template! (Sleeps one, doesn't squeak much)
- `--debug` flag to see what's actually happening
- Validation for impossible dimensions (no more negative height!)

### 🐛 Fixed
- Fixed the "90-foot bookshelf" bug (input validation is important, kids)
- Optimizer no longer suggests buying 47 boards for a small shelf
- Math.random() is no longer used for structural calculations

### 🔥 Removed
- Removed the "wing it" optimization mode (it never worked anyway)

## [0.1.3] - 2023-12-15 - "The Christmas Miracle Update"

### ✨ Added
- Storage bench template (perfect for hiding your failures)
- Support for custom kerf widths (because saw blades vary)
- Shopping list now includes estimated prices (prepare your wallet)

### 🐛 Fixed
- Fixed issue where all furniture was 1 inch tall
- Cut list now actually accounts for saw blade width
- No longer recommends negative quantities of wood

### 📝 Changed
- Improved optimization algorithm (wastes 20% less wood!)
- Made default dimensions actually reasonable

## [0.1.2] - 2023-11-30 - "The Thanksgiving Disaster Recovery"

### ✨ Added
- Workbench template (for making more mistakes on)
- Docker support (consistency across platforms!)
- Basic test suite (they sometimes pass!)

### 🐛 Fixed
- Fixed critical bug where all cuts were 1 inch too short
- Material calculations now use actual lumber dimensions (2x4 ≠ 2"x4")
- Files actually save with the correct extension now

### 💔 Known Issues
- Still can't help with actual cutting skills
- No refunds on wasted wood

## [0.1.1] - 2023-11-15 - "The One Where It Actually Works"

### ✨ Added
- Bill of materials generation
- Cut list optimization (First-Fit Decreasing algorithm!)
- Makefile for easy building

### 🐛 Fixed
- OpenSCAD actually runs now (missing semicolon, of course)
- Output directory is created if it doesn't exist
- Basic math errors in dimension calculations

### 📝 Changed
- Rewrote README to be less terrible
- Added more comments (future me will thank present me)

## [0.1.0] - 2023-11-01 - "The Beginning of the End (of Bad Furniture)"

### 🎉 Initial Release!
- Basic bookshelf template (my white whale)
- OpenSCAD integration
- Command-line interface
- Generates STL files
- Works on my machine™

### 💔 Known Issues
- Everything is held together by hope and Python
- Only makes bookshelves
- Measurements might be suggestions
- No tests whatsoever
- Documentation is just the README

---

## The Pre-History (Before I Learned Git)

### 2023-10-15: "The Incident"
- Tried to build a bookshelf manually
- It fell over immediately
- Wife suggested I "use my computer skills"
- OpenCraftShop was born

### 2023-10-01: "Rock Bottom"
- Spent $300 on wood
- Made $50 worth of scrap
- Cried a little
- Decided to learn OpenSCAD

### 2023-09-15: "The Leaning Tower of Pine"
- Built my third crooked bookshelf
- Googled "how to make furniture straight"
- Found out about "measuring"
- Mind = blown

---

## Version Numbering Philosophy

I use semantic versioning, sort of:
- **Major**: When I add furniture that doesn't immediately collapse
- **Minor**: New features that probably work
- **Patch**: Bug fixes and apologies

## How to Read This Changelog

- 🎉 = Something actually works!
- 🐛 = Fixed a bug I created
- 💔 = Still broken, sorry
- 🔥 = Removed because it was terrible
- ✨ = New feature to break
- 📝 = Changed my mind about something

## Contributing to This Changelog

Found a bug? Built some furniture? Got a story? Add it here! This changelog is as much about the journey as it is about the code.

Remember: Every failure is just a future changelog entry!

---

*"Those who cannot remember the past are condemned to repeat it. Also, those who can't use a saw properly are condemned to buy more wood."* - Me, probably