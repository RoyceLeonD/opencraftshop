# Troubleshooting Guide: When Things Go Wrong (And They Will) 🔥

Welcome to the troubleshooting guide, AKA my personal diary of failures. If you're here, something broke. Don't worry, I've probably broken it the same way before.

## 🚨 The "Oh $#!%" Quick Fixes

### Nothing happens when I run commands
```bash
# Did you build it first? (I forget this constantly)
make build

# Still nothing? Check Docker is running
docker --version
docker-compose --version
```

### The output folder is empty
This is my favorite one. Usually means:
1. The command didn't actually finish (check for errors)
2. You're looking in the wrong place (it's in `./output`)
3. I broke something in the latest update (sorry)

### Everything is in metric but I need imperial (or vice versa)
Currently it's all imperial because I'm American and stubborn. Metric support is on the TODO list right after "learn to use a saw properly."

## 🐛 Common Issues (My Greatest Hits)

### 1. Docker Issues

#### "Cannot connect to Docker daemon"
```bash
# Is Docker running? (It's always this)
# Mac/Windows: Open Docker Desktop
# Linux: 
sudo systemctl start docker

# Still broken? You might not be in the docker group
sudo usermod -aG docker $USER
# Log out and back in (annoying, I know)
```

#### "Port already in use"
Someone's using our ports. Find them and... ask nicely:
```bash
# See who's using the port
lsof -i :8080  # Mac/Linux
netstat -ano | findstr :8080  # Windows

# Kill it (with prejudice)
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows
```

### 2. OpenSCAD Problems

#### "OpenSCAD: command not found"
The 3D modeler isn't installed. Here's how to fix it:

```bash
# Mac (easiest)
brew install openscad

# Linux (also easy)
sudo apt-get install openscad  # Debian/Ubuntu
sudo dnf install openscad       # Fedora

# Windows (prayer required)
# Download from https://openscad.org/downloads.html
# Install it
# Add to PATH (good luck)
```

#### "OpenSCAD fails with no error"
This one's fun. Usually means:
1. Syntax error in the .scad file (missing semicolon, always)
2. Invalid dimensions (negative height, etc.)
3. OpenSCAD is having an existential crisis

Debug it:
```bash
# Run OpenSCAD directly
openscad -o test.stl src/templates/bookshelf.scad

# Check the generated .scad file
cat output/bookshelf_custom.scad
```

### 3. Dimension Disasters

#### "Error: Invalid dimensions"
You tried to make something impossible. I've tried these:
- Negative dimensions (physics says no)
- Zero height (that's just a drawing)
- 900-inch bookshelf (typo, but OpenSCAD tried anyway)

#### "The furniture is HUGE/tiny"
Remember: dimensions are in INCHES, not centimeters or feet.
- 72 = 6 feet (reasonable)
- 720 = 60 feet (not reasonable)
- 7.2 = 7.2 inches (tiny table)

### 4. Material & Cut List Issues

#### "Not enough boards calculated"
The optimizer assumes you can cut perfectly. You can't. Neither can I. Buy extra.

#### "Cut list doesn't make sense"
Check your kerf width. Default is 0.125" (1/8"). If your saw blade is different:
```bash
docker-compose run workbench-designer --type bookshelf --kerf 0.1875
```

#### "Material efficiency is terrible"
Sometimes the dimensions just don't pack well. Try:
- Adjusting dimensions slightly (±1-2 inches)
- Using different board lengths
- Accepting that wood is expensive

## 🔧 Advanced Debugging

### Enable Debug Mode
```bash
# See what's really happening
docker-compose run workbench-designer --type bookshelf --debug

# Save intermediate files
docker-compose run workbench-designer --type bookshelf --save-debug-files
```

### Check the Logs
```bash
# See container logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f
```

### Manual Testing
```bash
# Jump into the container
make shell

# Run commands manually
python src/main.py --help
python src/optimize_cuts.py --test
```

## 💥 When Everything is Broken

### The Nuclear Option
```bash
# Remove everything and start over
docker-compose down
docker system prune -a  # WARNING: Deletes ALL Docker stuff
make clean
make build
```

### The "It Worked Yesterday" Fix
```bash
# Go back to a known good version
git log --oneline  # Find a good commit
git checkout <commit-hash>
make build
```

### The "I Give Up" Solution
1. Open an issue on GitHub
2. Include the error message
3. Tell me what you were trying to do
4. I'll probably say "oh yeah, that happens to me too"

## 🤦 My Personal Failures (Learn From Them)

### The 90-Foot Bookshelf Incident
**Problem**: Made a bookshelf 900 inches tall
**Cause**: Typed 900 instead of 90
**Solution**: Added dimension validation
**Lesson**: Always double-check numbers

### The Negative Space Episode  
**Problem**: Bookshelf with -12 inch depth
**Cause**: Subtraction gone wrong in calculations
**Solution**: Physics doesn't work that way
**Lesson**: Validate all the things

### The Missing Kerf Disaster
**Problem**: All cuts were too short
**Cause**: Forgot saw blades have width
**Solution**: Added kerf parameter
**Lesson**: $200 worth of ruined wood

### The Unicode Meltdown
**Problem**: Terminal UI looked like hieroglyphics
**Cause**: Windows terminal vs Unicode
**Solution**: Added --no-visualize option
**Lesson**: ASCII art is hard

## 🩹 Quick Fixes for Common Errors

```bash
# Permission denied
sudo chown -R $USER:$USER .

# Module not found
pip install -r requirements.txt

# Can't find output files
ls -la output/

# Docker compose version issues
docker-compose version
# If v1, some commands might be different

# Python version issues
python --version  # Need 3.10+
```

## 📊 Error Message Decoder Ring

| Error | What It Really Means | Fix |
|-------|---------------------|-----|
| `FileNotFoundError` | I'm looking in the wrong place | Check paths |
| `ValueError: invalid literal` | You typed letters where numbers go | Check inputs |
| `OpenSCAD error` | Missing semicolon, probably | Check .scad syntax |
| `Insufficient boards` | Math is hard | Buy extra wood |
| `Docker daemon not running` | Docker is asleep | Wake it up |
| `Permission denied` | Computer says no | Use sudo (carefully) |

## 🚑 Still Stuck?

### Before You Give Up:

1. **Read the error message** - It's trying to help
2. **Check your inputs** - Garbage in, garbage out
3. **Try the defaults first** - They definitely work
4. **Google the error** - Someone else hit it first
5. **Take a break** - Fresh eyes help

### Getting Help:

- **GitHub Issues**: Best for bugs
- **Discussions**: Best for "how do I..."
- **Email**: When you need to vent
- **Twitter**: If you want to publicly shame my code

### What to Include:

```markdown
**What I was trying to do:**
Make a bookshelf 36" wide

**What I typed:**
docker-compose run workbench-designer --type bookshelf --width 36

**What happened:**
[Error message here]

**What I expected:**
Beautiful bookshelf plans

**My environment:**
- OS: Windows 10 / Mac / Linux
- Docker version: X.X
- How much coffee I've had: 3 cups
```

## 🎓 Lessons Learned

After breaking this thing hundreds of times, here's what I know:

1. **It's usually something simple** - Check the obvious first
2. **Docker fixes 90% of issues** - Consistency is key
3. **Validate your inputs** - Computers do exactly what you tell them
4. **Keep calm** - It's just code, not actual ruined wood
5. **Document your fixes** - Future you will thank you

## 🏁 Final Words

Remember: I built this whole thing because I'm bad at woodworking. The fact that it works at all is kind of miraculous. If you're having issues, you're in good company.

Every error message is a learning opportunity. Or at least that's what I tell myself after the fifth failed attempt.

Happy debugging! May your errors be few and your stack traces be helpful! 🐛🔨

---

*P.S. - If you find a new and creative way to break this, please let me know. I collect them like Pokemon cards.*