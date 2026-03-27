# VulnScan Architecture & Technical Guide

## 🏗️ System Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      USER BROWSER                             │
│  ┌────────────────────────────────────────────────────────┐  │
│  │           HTML/CSS/JavaScript Frontend                 │  │
│  │         (Modern Cyberpunk Dark Theme UI)               │  │
│  │  - URL Input                                            │  │
│  │  - Scan Type Selection                                 │  │
│  │  - Real-time Progress                                  │  │
│  │  - Results Display                                     │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                          ↓↑ HTTP/JSON
┌──────────────────────────────────────────────────────────────┐
│                    FLASK BACKEND                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              app.py (Main Application)                 │  │
│  │                                                         │  │
│  │  Endpoints:                                            │  │
│  │  - POST /api/scan (Main Vulnerability Scan)           │  │
│  │  - POST /api/quick-scan (Header Check)                │  │
│  │  - GET / (Serve HTML Interface)                        │  │
│  │                                                         │  │
│  │  Modules:                                              │  │
│  │  ├─ Request Handler                                   │  │
│  │  ├─ Parameter Extractor (BeautifulSoup)              │  │
│  │  ├─ XSS Tester (14 Payloads)                         │  │
│  │  ├─ SQLi Tester (17 Payloads)                        │  │
│  │  └─ Response Analyzer                                 │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                          ↓↑ HTTP Requests
┌──────────────────────────────────────────────────────────────┐
│                   TARGET WEBSITE                              │
│              (Website being scanned)                          │
│                                                               │
│  Scanner sends crafted payloads to:                         │
│  - Form fields                                              │
│  - Query parameters                                         │
│  - Hidden inputs                                            │
│  - Search boxes                                             │
│  - Comment fields                                           │
└──────────────────────────────────────────────────────────────┘
```

## 📁 File Structure

```
vulnscan/
│
├── app.py                          # Main Flask Application (580 lines)
│   ├── Flask initialization
│   ├── XSS Payload definitions (14 payloads)
│   ├── SQLi Payload definitions (17 payloads)
│   ├── SQL Error pattern matching (8 patterns)
│   ├── Form & parameter extraction
│   ├── XSS testing logic
│   ├── SQLi testing logic
│   ├── API endpoints (/api/scan, /api/quick-scan)
│   └── Error handling & response formatting
│
├── templates/
│   └── index.html                  # Web Interface (720 lines)
│       ├── HTML structure
│       ├── Cyberpunk dark theme CSS
│       ├── Animation & transitions
│       ├── Form inputs & controls
│       ├── Progress indicators
│       ├── Results display
│       └── JavaScript logic (Fetch API, DOM manipulation)
│
├── vulnerable_app.py               # Test Application (220 lines)
│   ├── Vulnerable XSS endpoint
│   ├── Vulnerable SQLi endpoint
│   ├── Form injection endpoint
│   ├── Combined vulnerability endpoint
│   ├── Safe example endpoint
│   └── Test UI with examples
│
├── requirements.txt                # Python Dependencies
│   ├── Flask 2.3.2
│   ├── Flask-CORS 4.0.0
│   ├── requests 2.31.0
│   └── beautifulsoup4 4.12.2
│
├── README.md                       # Complete Documentation
│   ├── Features
│   ├── Installation guide
│   ├── Usage instructions
│   ├── How it works
│   ├── API documentation
│   ├── Customization
│   ├── Troubleshooting
│   └── Legal disclaimer
│
├── QUICKSTART.md                   # Quick Setup Guide
│   ├── 5-minute setup
│   ├── Testing instructions
│   ├── Example test cases
│   ├── Troubleshooting
│   └── Learning resources
│
└── This file (ARCHITECTURE.md)     # Technical Deep Dive
```

## 🔄 Request Flow Diagram

```
User Input (URL + Scan Type)
        ↓
Browser JavaScript
  - Validates input
  - Sends POST to /api/scan
        ↓
Flask Backend receives request
        ↓
Parameter Extraction
  - GET main page HTML
  - Parse with BeautifulSoup
  - Find all <form> elements
  - Find all <input>, <textarea>, <select>
  - Extract parameter names
        ↓
Split Testing
  ├─ XSS Testing Loop
  │   ├─ For each parameter
  │   ├─ For each XSS payload (14 total)
  │   ├─ Send HTTP request
  │   ├─ Check if payload reflected
  │   ├─ Check for pattern matches
  │   └─ Record if vulnerable
  │
  └─ SQLi Testing Loop
      ├─ For each parameter
      ├─ For each SQLi payload (17 total)
      ├─ Send HTTP request
      ├─ Check for SQL error messages
      ├─ Pattern match database errors
      └─ Record if vulnerable
        ↓
Response Analysis & Collection
  ├─ Compile XSS vulnerabilities
  ├─ Compile SQLi vulnerabilities
  ├─ Calculate statistics
  └─ Format JSON response
        ↓
Send Results to Browser
        ↓
JavaScript receives JSON
  ├─ Display vulnerability count
  ├─ Show severity indicators
  ├─ List all vulnerabilities
  ├─ Display payloads & parameters
  └─ Highlight critical issues
        ↓
User Reviews Findings
```

## 🧩 Core Components

### 1. Frontend (index.html)

**Technology Stack:**
- HTML5 semantic structure
- CSS3 with CSS variables & animations
- Vanilla JavaScript (ES6+)
- Fetch API for async requests

**Key Features:**
```javascript
// Main scanning function
async function startScan() {
    - Get target URL from input
    - Get scan type (XSS/SQLi/Both)
    - Validate input
    - Send POST request to /api/scan
    - Handle response
    - Display results
}

// Result display
function displayResults(results) {
    - Update vulnerability counts
    - Create vulnerability cards
    - Show severity indicators
    - Format payloads
}
```

### 2. Backend (app.py)

**Payload Testing Logic:**
```python
# XSS Testing
def test_xss(url, payload, param_name, method='GET'):
    - Send payload as parameter value
    - Check if reflected in response
    - Check for unencoded tags
    - Return: vulnerable status + details

# SQLi Testing
def test_sqli(url, payload, param_name, method='GET'):
    - Send SQL syntax payload
    - Look for error messages
    - Pattern match known DB errors
    - Return: vulnerable status + error type
```

**Parameter Extraction:**
```python
def extract_forms(url, html_content):
    - Parse HTML with BeautifulSoup
    - Find all <form> elements
    - Extract form action URLs
    - Get form method (GET/POST)
    - Find all input fields
    - Return: list of forms with fields

def extract_inputs(url, html_content):
    - Find all <input> elements
    - Find all <textarea> elements
    - Find all <select> elements
    - Extract name attributes
    - Return: list of parameters
```

### 3. Vulnerable App (vulnerable_app.py)

**Intentional Vulnerabilities:**
```python
# Endpoint 1: Reflected XSS
/vulnerable-xss?q=<payload>
├─ Gets 'q' parameter
├─ Inserts directly into HTML
├─ No escaping/encoding
└─ Shows unfiltered user input

# Endpoint 2: SQL Injection
/vulnerable-sqli?username=<payload>
├─ Gets 'username' parameter
├─ Uses string concatenation
├─ Builds SQL query: f"SELECT * FROM users WHERE username = '{username}'"
├─ No parameterized queries
└─ Shows SQL errors in response

# Endpoint 3: Form Injection
/vulnerable-form (POST)
├─ Gets form data
├─ Inserts into HTML response
├─ No sanitization
└─ Vulnerable to XSS via form submission

# Endpoint 4: Combined
/search-users?q=<payload>
├─ Both XSS and SQLi vulnerabilities
├─ Demonstrates chained attacks
└─ Real-world attack scenario
```

## 🎯 XSS Detection Logic

```
For each parameter:
    For each of 14 payloads:
        1. Send payload: ?param=<script>alert("xss")</script>
        
        2. Receive response HTML
        
        3. Check if payload appears unencoded:
           ├─ Look for exact match
           ├─ Look for decoded versions
           └─ Look for partial matches
        
        4. Patterns checked:
           ├─ <script> tags
           ├─ Event handlers (onerror, onclick, etc.)
           ├─ JavaScript protocol
           └─ HTML entities
        
        5. Result:
           ├─ If found → VULNERABLE
           ├─ Record parameter name
           ├─ Record payload used
           ├─ Record vulnerability type
           └─ Set severity to HIGH
```

## 🎯 SQLi Detection Logic

```
For each parameter:
    For each of 17 payloads:
        1. Send payload: ?param=' OR '1'='1
        
        2. Receive response HTML
        
        3. Check for SQL error messages:
           ├─ Pattern: "SQL syntax"
           ├─ Pattern: "Unclosed quotation"
           ├─ Pattern: "MySQL"
           ├─ Pattern: "PostgreSQL"
           ├─ Pattern: "MSSQL"
           ├─ Pattern: "ORA-" (Oracle)
           └─ Other DB-specific errors
        
        4. Special checks:
           ├─ UNION-based detection
           ├─ Boolean-based detection
           ├─ Time-based detection (SLEEP/WAITFOR)
           └─ Error-based detection
        
        5. Result:
           ├─ If error found → VULNERABLE
           ├─ Record parameter name
           ├─ Record payload used
           ├─ Classify vulnerability type
           └─ Set severity to CRITICAL
```

## 📊 Data Structures

### Vulnerability Object
```json
{
  "parameter": "search",
  "payload": "<script>alert('xss')</script>",
  "type": "Reflected XSS",
  "severity": "High"
}
```

### Scan Results Object
```json
{
  "url": "http://example.com",
  "status": "completed",
  "xss_vulnerabilities": [...],
  "sqli_vulnerabilities": [...],
  "total_tests": 465,
  "vulnerable_found": 3
}
```

## ⚡ Performance Characteristics

### Scan Complexity
```
Parameters: N
XSS Payloads: 14
SQLi Payloads: 17
Scan Type Multiplier: 1-2x

Total Tests = N × (14 + 17) × Multiplier
         = N × 31 × Multiplier

For 5 parameters (typical):
Total Tests ≈ 155 requests
Time ≈ 15-30 seconds
```

### Request Timeline
```
Time (seconds) | Action
0-1           | GET main page, extract parameters
1-15          | XSS testing (100ms per request)
15-30         | SQLi testing (100ms per request)
30-31         | Response compilation
31+           | Display results
```

## 🔒 Security Considerations

### What's Safe
- ✅ Payloads are non-destructive
- ✅ No data modification
- ✅ No persistent changes
- ✅ Detection-only testing
- ✅ No credential harvesting
- ✅ No system commands

### What's Detected
- ✅ Reflected XSS vulnerabilities
- ✅ SQL injection vulnerabilities
- ✅ Basic security headers
- ✅ Parameter injection points
- ✅ Form submission issues

### What's NOT Detected
- ❌ Stored/Persistent XSS (requires callback)
- ❌ DOM-based XSS (JavaScript execution)
- ❌ Blind SQL Injection (requires timing/out-of-band)
- ❌ Authenticated vulnerabilities (no auth support)
- ❌ CSRF attacks
- ❌ Command injection
- ❌ XXE attacks

## 🔧 Customization Points

### Add Custom Payload
1. Edit `app.py`
2. Find `XSS_PAYLOADS` or `SQLI_PAYLOADS`
3. Add new payload string
4. Restart Flask

### Change Detection Patterns
1. Edit `SQL_ERROR_PATTERNS` in `app.py`
2. Add new regex pattern
3. Restart Flask

### Modify UI Theme
1. Edit CSS variables in `index.html`
2. Change colors, fonts, animations
3. Refresh browser (no restart needed)

### Add New Vulnerability Type
1. Create new testing function in `app.py`
2. Add new endpoint in Flask app
3. Update JavaScript in `index.html`
4. Call new endpoint from JavaScript

## 📈 Scalability & Optimization

### Current Limitations
- Single-threaded scanning
- Sequential request sending
- No parallel testing
- Memory limits on response size

### Optimization Opportunities
1. **Multi-threading**: Test multiple parameters in parallel
2. **Connection pooling**: Reuse HTTP connections
3. **Async I/O**: Use asyncio for non-blocking requests
4. **Payload grouping**: Combine similar payloads
5. **Caching**: Cache parameter extraction results

### Recommended Improvements
```python
# From:
for param in params:
    for payload in payloads:
        test(param, payload)  # Sequential

# To:
from concurrent.futures import ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(test, p, py) 
               for p in params for py in payloads]
    results = [f.result() for f in futures]
```

## 🧪 Testing the Scanner

### Unit Testing Approach
```python
# Test XSS detection
test_payload = "<script>alert('xss')</script>"
response = test_xss(vulnerable_url, test_payload, "q")
assert response['vulnerable'] == True

# Test SQLi detection
test_payload = "' OR '1'='1"
response = test_sqli(vulnerable_url, test_payload, "id")
assert response['vulnerable'] == True
```

## 📚 Code Quality

### Total Lines of Code
- `app.py`: ~580 lines
- `index.html`: ~720 lines
- `vulnerable_app.py`: ~220 lines
- **Total**: ~1,500 lines

### Key Metrics
- Complexity: Low-Medium
- Readability: High (well-commented)
- Maintainability: High (modular design)
- Test Coverage: 0% (no unit tests)
- Documentation: Comprehensive

## 🚀 Deployment Notes

### Development Mode
```bash
python app.py
# Debug: ON
# Auto-reload: ON
# Full error messages: YES
```

### Production Mode
```python
# In app.py:
app.run(debug=False, port=80)
# Use production WSGI server (Gunicorn, uWSGI)
```

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

**This architecture enables a complete, functional vulnerability scanning system suitable for educational and authorized professional use.**
