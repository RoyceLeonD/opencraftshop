# Quick Start

## Get It Running

```bash
git clone https://github.com/RoyceLeonD/opencraftshop.git
cd opencraftshop
make build
```

If that breaks, you probably don't have Docker. Go install it.

## Make Furniture

```bash
make bookshelf
```

Check `output/` folder. Your plans are there.

## Custom Sizes

```bash
# Different dimensions
docker-compose run workbench-designer --type bookshelf --height 48 --width 30

# Other furniture
docker-compose run workbench-designer --type storage_bench --length 60 --width 20
```

## All Furniture Types

```bash
make workbench
make storage-bench
make bed
make bookshelf
```

## Common Problems

**"Docker not found"**
Install Docker. Google it.

**"Output folder is empty"**
Did the command finish? Wait for it.

**"Dimensions seem wrong"**
A 2x4 isn't 2"x4". Tool knows this. You're welcome.

## What You Get

In `output/`:
- `.stl` - 3D model
- `.scad` - Source file
- `bill_of_materials.txt` - Shopping list
- `cut_list.txt` - Follow exactly
- `shopping_list.txt` - Take to store

## Tips

1. Start with defaults
2. Print the lists
3. Buy extra wood
4. Measure your space first

## Still Confused?

File an [issue](https://github.com/RoyceLeonD/opencraftshop/issues). Be specific.

---

Built for people who can't cut straight. That's it.