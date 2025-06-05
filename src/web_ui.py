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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate_model', methods=['POST'])
def generate_model():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        prompt = data.get('prompt')
        
        if not prompt:
            return jsonify({"error": "Missing prompt"}), 400

        # Placeholder for model generation logic.
        # This will be replaced with actual Shap-E integration later.
        # For now, simulate creating a dummy file.
        
        # Create a unique ID for the request to manage outputs if needed
        request_id = tempfile.NamedTemporaryFile().name.split('/')[-1] # Generate a unique name
        model_filename = f"model_{request_id}.obj" # Example output filename
        model_path = OUTPUT_DIR / model_filename

        # Simulate file creation
        with open(model_path, 'w') as f:
            f.write(f"# Dummy OBJ file for prompt: {prompt}\nv 1.0 1.0 1.0\nv -1.0 -1.0 1.0\nv -1.0 1.0 -1.0\nf 1 2 3")

        response_data = {
            'success': True,
            'message': 'Model generation initiated (placeholder).',
            'prompt': prompt,
            'files': {
                'model_file': model_filename  # Or 'stl_assembled' if the frontend expects that key
            }
        }
        
        return jsonify(response_data)
        
    except Exception as e:
        app.logger.error(f"Error in generate_model: {str(e)}") # Add logging
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