#!/bin/bash
# Example: Building a bookshelf because I have books (somehow)

echo "🔨 OpenCraftShop Custom Bookshelf Builder"
echo "========================================="
echo ""
echo "Project: 'I-swear-I'll-read-these-someday' shelf"
echo "Requirements: 5 feet tall (because I'm optimistic about book collecting)"
echo "              2 feet wide (reality check on space)"
echo "              10 inches deep (for normal books, not coffee table monsters)"
echo ""
echo "Firing up the saw blade calculator... 🪚"
echo ""

# Run OpenCraftShop with custom dimensions
docker-compose run opencraftshop \
    --type bookshelf \
    --height 60 \
    --length 24 \
    --width 10

echo ""
echo "✅ Design complete! Your files await in output/"
echo ""
echo "📁 What you got:"
echo "  📐 bookshelf.stl - For dreaming in 3D"
echo "  ✂️  cut_list.txt - Your roadmap to sawdust"
echo "  💸 shopping_list.txt - Your credit card's worst nightmare"
echo ""
echo "⚠️  Remember: The books are optional, but the level floor isn't!"
echo ""
echo "Good luck, and may your shelves be less saggy than mine! 📚"