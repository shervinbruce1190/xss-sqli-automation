# VulnScan - Web Vulnerability Scanner

A real-time web-based XSS and SQL Injection vulnerability scanner with modern UI. Built with Flask backend and HTML5/CSS3/JavaScript frontend.

## Features

✅ **Real-time XSS Detection**
- Tests 14+ XSS payload variations
- Detects reflected XSS vulnerabilities
- Tests across GET/POST parameters

✅ **Real-time SQLi Detection**
- Tests 17+ SQL injection payloads
- Error-based SQLi detection
- UNION-based SQLi detection
- Time-based blind SQLi detection

✅ **Modern Web Interface**
- Real-time scanning progress
- Beautiful dark theme with cyberpunk aesthetic
- Detailed vulnerability reports
- Severity indicators

✅ **Automated Parameter Discovery**
- Automatically extracts form fields
- Discovers input parameters
- Tests multiple injection points

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

### 1. Clone or Extract Files

```bash
cd /home/claude
```

### 2. Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

### Start the Flask Server

```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Access the Web Interface

Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### 1. **Enter Target URL**
- Type the website URL you want to scan (e.g., `http://example.com`)
- The scanner will handle both http:// and https:// URLs

### 2. **Select Scan Type**
- **Both**: Test for both XSS and SQLi (recommended)
- **XSS Only**: Only test for Cross-Site Scripting vulnerabilities
- **SQLi Only**: Only test for SQL Injection vulnerabilities

### 3. **Start Scan**
- Click "Start Scan" button
- The scanner will:
  - Discover all input parameters
  - Send various payloads
  - Analyze responses for vulnerabilities
  - Display results in real-time

### 4. **Review Results**
- See total vulnerabilities found
- Click on each vulnerability to see:
  - Vulnerable parameter
  - Payload that triggered it
  - Vulnerability type
  - Severity level

## How It Works

### XSS Detection Process

1. **Parameter Discovery**: Extracts all form fields and input parameters
2. **Payload Injection**: Sends XSS payloads like:
   - `<script>alert("xss")</script>`
   - `"><script>alert(1)</script>`
   - `<img src=x onerror="alert('xss')">`
   - And 11+ more variations
3. **Response Analysis**: Checks if payloads appear unencoded in responses
4. **Result**: Reports reflected XSS vulnerabilities with high accuracy

### SQLi Detection Process

1. **Parameter Discovery**: Identifies all injectable parameters
2. **Error-Based Testing**: Sends SQL syntax payloads:
   - `' OR '1'='1`
   - `' OR 1=1--`
   - `admin' --`
   - And more...
3. **Error Pattern Matching**: Looks for SQL error messages:
   - MySQL errors
   - PostgreSQL errors
   - MSSQL errors
   - SQLite errors
4. **Result**: Reports SQL injection vulnerabilities with type classification

## Payload Examples

### XSS Payloads Tested
```
<script>alert("xss")</script>
"><script>alert(1)</script>
<img src=x onerror="alert('xss')">
<svg onload="alert('xss')">
javascript:alert("xss")
<iframe src="javascript:alert('xss')"></iframe>
<body onload="alert('xss')">
<input onfocus="alert('xss')" autofocus>
...and more
```

### SQLi Payloads Tested
```
' OR '1'='1
' OR 1=1--
' OR 1=1#
admin' --
' AND SLEEP(5)--
' UNION SELECT NULL--
...and more
```

## API Endpoints

### POST /api/scan
Performs a full vulnerability scan

**Request:**
```json
{
  "url": "http://example.com",
  "type": "both"  // "xss", "sqli", or "both"
}
```

**Response:**
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

### POST /api/quick-scan
Quick security header check

**Request:**
```json
{
  "url": "http://example.com"
}
```

## Security Considerations

### ⚠️ Important Notes

1. **Authorization Required**: Only scan websites you own or have explicit written permission to test
2. **Legal Compliance**: Unauthorized security testing is illegal in most jurisdictions
3. **Rate Limiting**: Built-in delays between requests (100ms) to avoid overwhelming targets
4. **User-Agent Spoofing**: Uses realistic User-Agent headers for legitimate testing
5. **No Malicious Payloads**: All payloads are non-destructive and for detection only

### Best Practices

- Test on your own applications first
- Get written permission before testing third-party sites
- Document all findings
- Report vulnerabilities responsibly
- Follow responsible disclosure practices

## Detected Vulnerability Types

### XSS
- **Reflected XSS**: Payload echoed in response without encoding
- **Severity**: High
- **Impact**: Session hijacking, credential theft, malware distribution

### SQLi
- **Error-based SQLi**: Database errors revealed
- **UNION-based SQLi**: Data extraction through UNION queries
- **Time-based SQLi**: Detection through response delays
- **Severity**: Critical
- **Impact**: Data breach, authentication bypass, system compromise

## Customization

### Adding Custom Payloads

Edit `app.py` and modify these lists:

```python
XSS_PAYLOADS = [
    '<script>alert("xss")</script>',
    # Add your custom payloads here
]

SQLI_PAYLOADS = [
    "' OR '1'='1",
    # Add your custom payloads here
]
```

### Adjusting Detection Patterns

Modify SQL error patterns:

```python
SQL_ERROR_PATTERNS = [
    r"SQL syntax",
    r"SQL error",
    # Add custom regex patterns
]
```

## Troubleshooting

### Port Already in Use
```bash
# Use a different port
python app.py --port 5001
```

### Connection Refused
- Make sure the Flask server is running
- Check firewall settings
- Verify the URL is correct

### Scan Takes Too Long
- The scanner tests many payloads for accuracy
- Average scan: 30-60 seconds depending on target
- Reduce payloads for faster scanning

### False Positives
- Some legitimate sites may echo input
- Manual verification of results is recommended
- Check the actual payload in the response

## Dependencies

- **Flask 2.3.2**: Web framework
- **Flask-CORS 4.0.0**: Cross-Origin Resource Sharing
- **requests 2.31.0**: HTTP library for sending payloads
- **beautifulsoup4 4.12.2**: HTML parsing for form discovery

## System Requirements

- **RAM**: 256MB minimum
- **Storage**: 50MB free space
- **Network**: Active internet connection
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

## Performance

- **Scan Time**: 30-90 seconds per target
- **Requests per Scan**: ~465 (14 XSS + 17 SQLi per parameter)
- **Concurrent Scans**: Supports 1 scan at a time
- **Rate Limiting**: 100ms delay between requests

## Limitations

- No blind XSS detection with callback verification
- Limited to HTTP/HTTPS requests
- Cannot test authenticated endpoints (without modification)
- No cookie/session handling by default
- Single-threaded scanning

## Future Enhancements

- [ ] Multi-threaded scanning
- [ ] Authentication support
- [ ] Custom header injection
- [ ] Blind XSS with callback server
- [ ] CSRF detection
- [ ] Command injection testing
- [ ] Report generation (PDF/HTML)
- [ ] Scan scheduling
- [ ] API key management

## License

Educational and authorized security testing use only.

## Legal Disclaimer

This tool is designed for authorized security testing and educational purposes only. Users are responsible for complying with all applicable laws and regulations. Unauthorized access to computer systems is illegal. Always obtain written permission before testing any website you do not own.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Flask documentation
3. Check browser console for errors (F12)

## Author Notes

This vulnerability scanner is a demonstration of how security professionals test for common web vulnerabilities. It uses the same techniques and payloads as professional security tools like Burp Suite and OWASP ZAP.

The scanner is intentionally educational and includes all source code for learning purposes.

---

**Happy Secure Testing! 🔒**
