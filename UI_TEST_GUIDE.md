# OpenCraftShop Web UI Testing Guide

## Overview
The web UI has been successfully implemented with the following features:

### 1. Three-Pane Layout
- **Left Pane**: Input controls and file downloads
- **Middle Pane**: 3D STL viewer with assembled/exploded toggle
- **Right Pane**: ASCII cut visualization

### 2. Key Features Implemented

#### Furniture Type Dropdown
- Automatically updates dimensions when changed
- Available types:
  - Workbench (72" x 24" x 34")
  - Storage Bench (48" x 18" x 18")
  - Bed Frame (80" x 60" x 14")
  - Bookshelf (36" x 12" x 72")

#### 3D Model Viewer
- Uses Three.js for WebGL rendering
- Toggle between assembled and exploded views
- Mouse controls: rotate, zoom, pan
- Both STL files are generated: assembled and exploded

#### ASCII Cut Visualization
- Displays cut diagrams in terminal-style format
- Shows stock utilization with visual representation
- Includes waste calculations and efficiency metrics

### 3. Files Created/Modified

1. **src/web_ui.py** - Flask web server with API endpoints
2. **src/templates/index.html** - Web UI with Three.js integration
3. **src/main.py** - Modified to generate both assembled/exploded STLs
4. **src/templates/workbench.scad** - Added view_mode parameter
5. **docker-compose.yml** - Added web service configuration

## Testing the UI

### Quick Start
```bash
# Start the web UI
./simple_ui_test.sh

# Access in browser
http://localhost:5000
```

### Manual Testing Steps

1. **Start the web server**:
   ```bash
   docker-compose up web
   ```

2. **Open browser** to http://localhost:5000

3. **Test furniture type selection**:
   - Select each furniture type
   - Verify dimensions update automatically

4. **Generate a design**:
   - Click "Generate Design"
   - Wait for generation (10-15 seconds)
   - Verify 3D model appears

5. **Test view toggle**:
   - Toggle between Assembled/Exploded views
   - Verify model updates

6. **Check cut visualization**:
   - Look at right pane for ASCII diagrams
   - Verify cut layouts are displayed

7. **Test downloads**:
   - Click download links for STL, Cut List, Shopping List
   - Verify files download correctly

## Known Issues Resolved

1. ✅ ASCII terminal visualization hang - Replaced with web UI
2. ✅ Parameter naming (--output vs --output-dir) - Fixed
3. ✅ Float to integer conversion - Fixed
4. ✅ Automatic dimension updates - Implemented
5. ✅ Dual STL generation - Implemented
6. ✅ ASCII cut visualization in web - Implemented

## Pending Improvements

1. **Assembled View Cohesion**: The assembled view still shows pieces with small gaps. This could be improved by adjusting the OpenSCAD templates to ensure pieces touch properly.

2. **Real-time Updates**: Currently requires full regeneration for dimension changes. Could implement real-time parameter updates.

3. **Progress Indicator**: Add a progress bar during generation instead of just "Generating..."

## Docker Commands

```bash
# Start web UI
docker-compose up web

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Rebuild after changes
docker-compose build web
```

## API Endpoints

- `GET /` - Main web interface
- `POST /api/generate` - Generate furniture design
- `GET /api/download/<filename>` - Download generated files

## Screenshot Opportunities

When testing manually, good moments to capture screenshots:

1. Initial page load with furniture dropdown
2. After selecting different furniture types (showing dimension changes)
3. After generation with 3D model visible
4. With exploded view toggle activated
5. Right pane showing ASCII cut diagrams
6. Full window showing all three panes together