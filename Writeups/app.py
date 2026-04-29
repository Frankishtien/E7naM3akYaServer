import os
import json
import tempfile
import subprocess
import requests
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB max file size
app.config['UPLOAD_FOLDER'] = 'scans'

# Ensure scans directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'py', 'js', 'php', 'java', 'cpp', 'c', 'go', 'rb', 'rs', 'swift', 'kt', 'ts'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else 'txt'

def run_semgrep_scan(file_path, language=None):
    """Run Semgrep scan on the provided file"""
    try:
        # Build semgrep command
        cmd = ['semgrep', '--config', 'auto', '--json', file_path]
        
        # Run semgrep
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0 and result.returncode != 1:  # Semgrep returns 1 when finding issues
            return {'error': f'Semgrep scan failed: {result.stderr}'}
        
        # Parse JSON output
        scan_results = json.loads(result.stdout)
        return parse_semgrep_results(scan_results)
    
    except subprocess.TimeoutExpired:
        return {'error': 'Scan timeout expired'}
    except json.JSONDecodeError:
        return {'error': 'Failed to parse Semgrep output'}
    except Exception as e:
        return {'error': f'Scan failed: {str(e)}'}

def parse_semgrep_results(results):
    """Parse Semgrep JSON output into a structured format"""
    parsed_results = {
        'total_vulnerabilities': 0,
        'severity_counts': {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0,
            'INFO': 0
        },
        'vulnerabilities': []
    }
    
    severity_mapping = {
        'ERROR': 'HIGH',
        'WARNING': 'MEDIUM',
        'INFO': 'LOW',
        'INVENTORY': 'INFO'
    }
    
    for result in results.get('results', []):
        severity = result.get('extra', {}).get('severity', 'INFO').upper()
        
        # Map severity to our categories
        if severity in ['CRITICAL']:
            mapped_severity = 'CRITICAL'
        elif severity in ['HIGH', 'ERROR']:
            mapped_severity = 'HIGH'
        elif severity in ['MEDIUM', 'WARNING']:
            mapped_severity = 'MEDIUM'
        elif severity in ['LOW']:
            mapped_severity = 'LOW'
        else:
            mapped_severity = 'INFO'
        
        parsed_results['severity_counts'][mapped_severity] += 1
        parsed_results['total_vulnerabilities'] += 1
        
        vulnerability = {
            'id': str(uuid.uuid4()),
            'name': result.get('check_id', 'Unknown'),
            'severity': mapped_severity,
            'file': result.get('path', 'unknown'),
            'line': result.get('start', {}).get('line', 0),
            'description': result.get('extra', {}).get('message', 'No description available'),
            'fix': result.get('extra', {}).get('fix', 'Review code and apply security best practices'),
            'code': result.get('extra', {}).get('lines', ''),
            'cwe': result.get('extra', {}).get('metadata', {}).get('cwe', 'N/A')
        }
        
        parsed_results['vulnerabilities'].append(vulnerability)
    
    return parsed_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan/upload', methods=['POST'])
def scan_upload():
    """Handle file upload scanning"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': f'File type not allowed. Allowed types: {", ".join(ALLOWED_EXTENSIONS)}'}), 400
    
    try:
        # Save file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Run scan
        results = run_semgrep_scan(file_path)
        
        # Clean up
        os.remove(file_path)
        
        if 'error' in results:
            return jsonify(results), 500
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scan/paste', methods=['POST'])
def scan_paste():
    """Handle pasted code scanning"""
    data = request.json
    
    if not data or 'code' not in data:
        return jsonify({'error': 'No code provided'}), 400
    
    code = data['code']
    language = data.get('language', 'py')
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{language}', delete=False, dir=app.config['UPLOAD_FOLDER']) as f:
            f.write(code)
            temp_path = f.name
        
        # Run scan
        results = run_semgrep_scan(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        if 'error' in results:
            return jsonify(results), 500
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/scan/github', methods=['POST'])
def scan_github():
    """Handle GitHub URL scanning"""
    data = request.json
    
    if not data or 'url' not in data:
        return jsonify({'error': 'No URL provided'}), 400
    
    url = data['url']
    
    try:
        # Convert GitHub URL to raw content URL
        if 'github.com' in url and '/blob/' in url:
            raw_url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        else:
            return jsonify({'error': 'Invalid GitHub URL format'}), 400
        
        # Fetch file content
        response = requests.get(raw_url, timeout=10)
        response.raise_for_status()
        
        code = response.text
        
        # Get file extension from URL
        filename = url.split('/')[-1]
        language = get_file_extension(filename)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix=f'.{language}', delete=False, dir=app.config['UPLOAD_FOLDER']) as f:
            f.write(code)
            temp_path = f.name
        
        # Run scan
        results = run_semgrep_scan(temp_path)
        
        # Clean up
        os.remove(temp_path)
        
        if 'error' in results:
            return jsonify(results), 500
        
        return jsonify(results)
    
    except requests.RequestException as e:
        return jsonify({'error': f'Failed to fetch GitHub file: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)     
