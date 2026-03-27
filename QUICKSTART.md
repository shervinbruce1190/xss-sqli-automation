# VulnScan - Quick Start Guide

## 📦 Files Included

```
vulnscan/
├── app.py                  # Flask backend (main server)
├── index.html             # Web UI (place in templates/ folder)
├── requirements.txt       # Python dependencies
├── vulnerable_app.py      # Demo vulnerable app for testing
└── README.md             # Full documentation
```

## 🚀 Quick Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Create Folder Structure
```bash
mkdir templates
```

### Step 3: Place Files
```
app.py              → root folder
index.html          → templates/ folder
vulnerable_app.py   → root folder (optional, for testing)
requirements.txt    → root folder
```

### Step 4: Run the Server
```bash
python app.py
```

### Step 5: Open in Browser
```
http://localhost:5000
```

---

## 🧪 Testing the Scanner

### Option A: Scan Your Own Vulnerable App (Recommended)

**Terminal 1** - Run the vulnerable test app:
```bash
python vulnerable_app.py
```
It will run on `http://localhost:5001`

**Terminal 2** - Run the main scanner:
```bash
python app.py
```
Access at `http://localhost:5000`

**In Browser**:
1. Go to http://localhost:5000
2. Enter target URL: `http://localhost:5001`
3. Select scan type: "Both"
4. Click "Start Scan"
5. Watch real-time vulnerability detection!

### Option B: Scan Real Websites (Get Permission First!)
1. Make sure you have written permission
2. Enter the target URL in the scanner
3. Run the scan
4. Review findings

---

## 🎯 How It Works

### Frontend (index.html)
- Modern dark-themed UI
- Real-time progress tracking
- Beautiful vulnerability report display
- Cyberpunk aesthetic design

### Backend (app.py)
- Extracts forms and input parameters
- Tests 14 different XSS payloads
- Tests 17 different SQLi payloads
- Analyzes responses for vulnerabilities
- Returns detailed results

### Vulnerable App (vulnerable_app.py)
- Contains 4 intentionally vulnerable endpoints
- Perfect for testing the scanner
- Shows what vulnerable code looks like
- Educational reference

---

## 📋 Scanner Features

✅ **14 XSS Payloads**
- Script tags
- Event handlers
- Image tags
- SVG exploits
- And more...

✅ **17 SQLi Payloads**
- Boolean-based
- Error-based
- UNION queries
- Time-based
- And more...

✅ **Smart Parameter Detection**
- Auto-discovers form fields
- Tests common parameters
- Handles nested forms
- Tests multiple injection points

✅ **Real-time Results**
- Shows vulnerabilities as found
- Severity indicators
- Payload display
- Parameter identification

---

## 🔍 Example Test Cases

### Test 1: Reflected XSS
```
URL: http://localhost:5001/vulnerable-xss?q=test
Payload: <script>alert('xss')</script>
Expected: XSS Vulnerability Detected ✓
```

### Test 2: SQL Injection
```
URL: http://localhost:5001/vulnerable-sqli?username=admin
Payload: ' OR '1'='1
Expected: SQLi Vulnerability Detected ✓
```

### Test 3: Form Injection
```
URL: http://localhost:5001/vulnerable-form
Method: POST
Payload in name field: <img src=x onerror=alert(1)>
Expected: XSS Vulnerability Detected ✓
```

---

## ⚙️ Configuration

### Add Custom Payloads
Edit `app.py` and modify:
```python
XSS_PAYLOADS = [
    '<script>alert("xss")</script>',
    # Add your custom payloads
]

SQLI_PAYLOADS = [
    "' OR '1'='1",
    # Add your custom payloads
]
```

### Change Port
Edit `app.py` last line:
```python
app.run(debug=True, port=5001)  # Change port number
```

### Adjust Request Timeout
Edit `app.py` in scan function:
```python
timeout=5  # Change timeout in seconds
```

---

## 🐛 Troubleshooting

### "Port 5000 already in use"
```bash
# Use a different port
# Edit app.py last line: app.run(debug=True, port=5002)
python app.py
```

### "Connection refused"
- Check Flask is running: `python app.py`
- Check URL is correct: `http://localhost:5000`
- Check firewall settings

### "No vulnerabilities found" (on vulnerable_app)
- Make sure vulnerable_app.py is running on port 5001
- Try manual test: `http://localhost:5001/vulnerable-xss?q=<script>alert(1)</script>`
- Check browser console for errors (F12)

### "SSL Certificate Error"
- Use `http://` not `https://` for testing
- Scanner handles both protocols

---

## 📊 Understanding Results

### Vulnerability Card
```
┌─────────────────────────────┐
│ 🔴 XSS Vulnerabilities     │
├─────────────────────────────┤
│ Parameter: q                │
│ Type: Reflected XSS         │
│ Severity: High              │
│ Payload: <script>alert...</script> │
└─────────────────────────────┘
```

### Severity Levels
- **🔴 Critical**: Immediate exploitation risk (SQLi)
- **🟠 High**: Can cause significant damage (XSS)
- **🟡 Medium**: Security header missing

---

## 🛡️ Security & Ethics

### ⚠️ Legal Warning
- Only test websites you own
- Get explicit written permission
- Unauthorized testing is illegal
- Follow responsible disclosure

### Best Practices
1. Test in isolated environments first
2. Keep detailed logs of scans
3. Report vulnerabilities responsibly
4. Document all findings
5. Get client sign-off

---

## 🚀 Performance Tips

- **Faster Scanning**: Reduce payload count in app.py
- **Better Accuracy**: Keep all payloads for production scans
- **Rate Limiting**: Adjust delay: `time.sleep(0.1)` in app.py
- **Parallel Testing**: Use --threads flag (requires modification)

---

## 📚 Learning Resources

### Understanding XSS
- **OWASP**: https://owasp.org/www-community/attacks/xss/
- **PortSwigger**: https://portswigger.net/web-security/cross-site-scripting

### Understanding SQLi
- **OWASP**: https://owasp.org/www-community/attacks/SQL_Injection
- **PortSwigger**: https://portswigger.net/web-security/sql-injection

### Web Security Testing
- **OWASP Testing Guide**: https://owasp.org/www-project-web-security-testing-guide/
- **PortSwigger Academy**: https://portswigger.net/web-security

---

## 🎓 What You'll Learn

By using this scanner, you'll understand:

1. ✅ How security scanners detect vulnerabilities
2. ✅ What makes code vulnerable to XSS
3. ✅ What makes code vulnerable to SQLi
4. ✅ How web applications are tested
5. ✅ Real security assessment workflows
6. ✅ Payload construction and testing
7. ✅ Response analysis for vulnerabilities
8. ✅ Professional security tooling

---

## 📖 Next Steps

### For Learning:
1. Scan the vulnerable_app.py
2. Review detected vulnerabilities
3. Look at the vulnerable code
4. Understand why it's vulnerable
5. Learn how to fix it

### For Professional Use:
1. Get written permission
2. Customize payloads for target
3. Document findings carefully
4. Create professional reports
5. Follow responsible disclosure

---

## 🤝 Need Help?

1. Check README.md for full documentation
2. Review app.py source code
3. Check browser console (F12) for errors
4. Look at vulnerable_app.py for examples
5. Study the HTML/CSS/JS in index.html

---

## 💡 Pro Tips

✨ **Tip 1**: Always test locally first before scanning live sites
✨ **Tip 2**: Review payloads in app.py to understand detection
✨ **Tip 3**: Use browser DevTools to see actual requests being sent
✨ **Tip 4**: Compare vulnerable vs safe code in vulnerable_app.py
✨ **Tip 5**: Add custom payloads based on target technology

---

## 🎉 You're Ready!

Now you have a professional-grade vulnerability scanner!

**Next:** Run the app and start scanning! 🚀
