"""
WorldSummarize Web Application
Serves the PDF document through a web interface with automatic updates
"""

from flask import Flask, render_template, send_file, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from pathlib import Path
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
PDF_PATH = 'world_summary.pdf'
ARCHIVE_PATH = 'archive/'

@app.route('/')
def index():
    """Serve the main web page"""
    return render_template('index.html')

@app.route('/api/pdf')
def serve_pdf():
    """Serve the current PDF document"""
    try:
        if os.path.exists(PDF_PATH):
            return send_file(PDF_PATH, mimetype='application/pdf')
        else:
            return jsonify({'error': 'PDF not found'}), 404
    except Exception as e:
        logger.error(f"Error serving PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def get_status():
    """Get the current status of the document"""
    try:
        status = {
            'pdf_exists': os.path.exists(PDF_PATH),
            'last_updated': None,
            'file_size': None,
            'archive_count': 0
        }
        
        if status['pdf_exists']:
            stat = os.stat(PDF_PATH)
            status['last_updated'] = datetime.fromtimestamp(stat.st_mtime).isoformat()
            status['file_size'] = stat.st_size
        
        # Count archive files
        if os.path.exists(ARCHIVE_PATH):
            status['archive_count'] = len([f for f in os.listdir(ARCHIVE_PATH) if f.endswith('.pdf')])
        
        return jsonify(status)
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/archives')
def list_archives():
    """List all archived PDFs"""
    try:
        archives = []
        if os.path.exists(ARCHIVE_PATH):
            for filename in sorted(os.listdir(ARCHIVE_PATH), reverse=True):
                if filename.endswith('.pdf'):
                    filepath = os.path.join(ARCHIVE_PATH, filename)
                    stat = os.stat(filepath)
                    archives.append({
                        'filename': filename,
                        'timestamp': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                        'size': stat.st_size
                    })
        return jsonify({'archives': archives[:20]})  # Return last 20 archives
    except Exception as e:
        logger.error(f"Error listing archives: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/archive/<filename>')
def serve_archive(filename):
    """Serve an archived PDF"""
    try:
        filepath = os.path.join(ARCHIVE_PATH, filename)
        if os.path.exists(filepath) and filename.endswith('.pdf'):
            return send_file(filepath, mimetype='application/pdf')
        else:
            return jsonify({'error': 'Archive not found'}), 404
    except Exception as e:
        logger.error(f"Error serving archive: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    logger.info("Starting WorldSummarize Web Application")
    app.run(debug=True, host='0.0.0.0', port=5000)
