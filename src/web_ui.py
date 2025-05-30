#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import subprocess
from typing import Dict, Any, Tuple
import tempfile
from pathlib import Path

app = Flask(__name__)
CORS(app)

OUTPUT_DIR = Path("/app/output")
OUTPUT_DIR.mkdir(exist_ok=True)

FURNITURE_TYPES = {
    "workbench": "Workbench",
    "storage_bench": "Storage Bench", 
    "bed_frame": "Bed Frame",
    "bookshelf": "Bookshelf"
}

@app.route('/')
def index():
    return render_template('index.html', furniture_types=FURNITURE_TYPES)

@app.route('/api/generate', methods=['POST'])
def generate_furniture():
    try:
        data = request.json
        furniture_type = data.get('type', 'workbench')
        dimensions = {
            'length': float(data.get('length', 48)),
            'width': float(data.get('width', 24)),
            'height': float(data.get('height', 36))
        }
        
        # Run the main.py script to generate files
        cmd = [
            'python3', '/app/src/main.py',
            '--type', furniture_type,
            '--length', str(int(dimensions['length'])),
            '--width', str(int(dimensions['width'])),
            '--height', str(int(dimensions['height'])),
            '--output-dir', str(OUTPUT_DIR),
            '--no-visualize'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({'error': f'Generation failed: {result.stderr}'}), 500
        
        # Read generated files
        stl_assembled_path = OUTPUT_DIR / f"{furniture_type}.stl"
        stl_exploded_path = OUTPUT_DIR / f"{furniture_type}_exploded.stl"
        cut_list_path = OUTPUT_DIR / "cut_list.txt"
        shopping_list_path = OUTPUT_DIR / "shopping_list.txt"
        
        response_data = {
            'success': True,
            'furniture_type': furniture_type,
            'dimensions': dimensions,
            'files': {
                'stl_assembled': f"{furniture_type}.stl" if stl_assembled_path.exists() else None,
                'stl_exploded': f"{furniture_type}_exploded.stl" if stl_exploded_path.exists() else None,
                'cut_list': 'cut_list.txt' if cut_list_path.exists() else None,
                'shopping_list': 'shopping_list.txt' if shopping_list_path.exists() else None
            }
        }
        
        # Read cut list and shopping list content
        if cut_list_path.exists():
            with open(cut_list_path, 'r') as f:
                response_data['cut_list_content'] = f.read()
        
        if shopping_list_path.exists():
            with open(shopping_list_path, 'r') as f:
                response_data['shopping_list_content'] = f.read()
        
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download/<filename>')
def download_file(filename):
    try:
        file_path = OUTPUT_DIR / filename
        if file_path.exists() and file_path.is_file():
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)