#!/bin/bash

echo "🚀 Starting OpenCraftShop web UI for screenshot capture..."
echo ""

# Start web server in background
echo "Starting web server..."
docker-compose up -d web

# Wait for server to start
echo "Waiting for web server to start..."
sleep 10

# Get container IP
WEB_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' opencraftshop-web)
echo "Web server running at: http://$WEB_IP:5000"

# Simple curl test
echo ""
echo "Testing web server..."
curl -s "http://localhost:5000" | grep -q "OpenCraftShop" && echo "✅ Web server is running!" || echo "❌ Web server not responding"

echo ""
echo "📌 Access the web UI at: http://localhost:5000"
echo ""
echo "You can now:"
echo "1. Open your browser to http://localhost:5000"
echo "2. Select different furniture types from the dropdown"
echo "3. Click 'Generate Design' to see the 3D model"
echo "4. Toggle between Assembled/Exploded views"
echo "5. View ASCII cut diagrams in the right pane"
echo ""
echo "Press Ctrl+C to stop the server..."

# Keep running
docker-compose logs -f web