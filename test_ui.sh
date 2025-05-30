#!/bin/bash

echo "🚀 Starting OpenCraftShop UI tests with Puppeteer..."
echo ""

# Create screenshots directory
mkdir -p test/screenshots

# Clean up any existing containers
docker-compose -f docker-compose.test.yml down 2>/dev/null

# Build and run the test
echo "📦 Building test containers..."
docker-compose -f docker-compose.test.yml build

echo ""
echo "🧪 Running UI tests..."
docker-compose -f docker-compose.test.yml up --abort-on-container-exit

# Copy screenshots out of container if needed
echo ""
echo "📸 Screenshots saved to test/screenshots/"
ls -la test/screenshots/ 2>/dev/null || echo "No screenshots found"

# Clean up
echo ""
echo "🧹 Cleaning up..."
docker-compose -f docker-compose.test.yml down

echo "✅ Test complete!"