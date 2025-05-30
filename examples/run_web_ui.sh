#!/bin/bash
# Start the OpenCraftShop Web UI

echo "🔨 Starting OpenCraftShop Web UI..."
echo "=================================="
echo ""

# Start the web service
docker-compose up -d web

echo ""
echo "✅ Web UI is starting up!"
echo ""
echo "🌐 Open your browser and go to: http://localhost:5000"
echo ""
echo "📝 Features:"
echo "  • Select furniture type from dropdown"
echo "  • Adjust dimensions with sliders" 
echo "  • View 3D model in real-time"
echo "  • Download STL, cut list, and shopping list"
echo ""
echo "🛑 To stop the server, run: docker-compose down"
echo ""