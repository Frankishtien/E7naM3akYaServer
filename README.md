

# 🔒 Security Code Scanner - SAST Tool

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)

![Semgrep](https://img.shields.io/badge/Semgrep-1.45+-red.svg)

![License](https://img.shields.io/badge/License-MIT-yellow.svg)

**Static Application Security Testing (SAST) Tool powered by Semgrep**

Scan your code for security vulnerabilities instantly

[Features](#-features) - [Installation](#-installation) - [Usage](#-usage) - [API Documentation](#-api-documentation)

</div>

---

## 📋 Table of Contents

- [What is this?](#what-is-this)

- [Features](#-features)

- [Tech Stack](#-tech-stack)

- [Installation](#-installation)

- [Usage](#-usage)

- [API Documentation](#-api-documentation)

- [Supported Languages](#-supported-languages)

- [Examples](#-examples)

- [Project Structure](#-project-structure)

- [Screenshots](#-screenshots)

- [Contributing](#-contributing)

- [License](#-license)

---

## 🎯 What is this?

**Security Code Scanner** is a web-based static code analysis tool that automatically detects security vulnerabilities in your source code. It uses **Semgrep** - a powerful static analysis engine - to identify:

- 🚨 Critical Security Vulnerabilities

- 🔐 Hardcoded Secrets & Credentials

- 💉 Injection Flaws (SQL, Command, Code)

- 🛡️ OWASP Top 10 Issues

- 📦 Unsafe Deserialization

- ⚠️ Security Anti-patterns

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📁 **File Upload** | Upload and scan local files |
| 📝 **Paste Code** | Directly paste code snippets |
| 🐙 **GitHub Integration** | Scan files directly from GitHub URLs |
| 🎨 **Web Interface** | Beautiful, user-friendly dashboard |
| 📊 **Detailed Reports** | Severity levels, CWE IDs, line numbers |
| 💡 **Fix Suggestions** | Get recommendations for fixing vulnerabilities |
| 🚀 **Fast Scanning** | Scans complete in seconds |
| 🔒 **Privacy First** | Files are deleted immediately after scanning |

## 🛠️ Tech Stack

- **Backend**: Python 3.8+ with Flask

- **Security Engine**: Semgrep

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5

- **API**: RESTful JSON API

## 📦 Installation

### Prerequisites

```bash

python3 --version

# Install pip if not present

sudo apt install python3

```

### Step 1: Clone the Repository

```bash

git clone https://github.com/yourusername/security-code-scanner.git

cd security-code-scanner

```

### Step 2: Install requirements


```bash
pip3 install flask werkzeug requests
# Or use requirements.txt
pip3 install -r requirements.txt
```



### Step 5: Run the Application

```bash

# Start the Flask server
python3 app.py
# Server will run at: http://localhost:5000

```

## 🚀 Usage

### Method 1: Web Interface (Easiest)

1\. Open browser and navigate to `http://localhost:5000`

2\. Choose one of three input methods:

   - **Upload File**: Click and select a file

   - **Paste Code**: Paste your code in the textarea

   - **GitHub URL**: Enter a raw GitHub file URL

3\. Click **Scan** button

4\. View detailed vulnerability report

### Method 2: API Access (For Developers)

#### 📁 Scan uploaded file

```bash

curl -X POST http://localhost:5000/api/scan/upload
  -F "file=@/path/to/your/file.py"

```

#### 📝 Scan pasted code

```bash

curl -X POST http://localhost:5000/api/scan/paste
  -H "Content-Type: application/json"
  -d '{"code":"import os; os.system(\"ls\")", "language":"py"}'

```

#### 🐙 Scan GitHub file

```bash
curl -X POST http://localhost:5000/api/scan/github
  -H "Content-Type: application/json"
  -d '{"url":"https://github.com/user/repo/blob/main/file.py"}'
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Web interface |
| POST | `/api/scan/upload` | Scan uploaded file |
| POST | `/api/scan/paste` | Scan pasted code |
| POST | `/api/scan/github` | Scan GitHub file |

### Response Format

```json

{
  "total_vulnerabilities": 5,
  "severity_counts": {
    "CRITICAL": 1,
    "HIGH": 2,
    "MEDIUM": 1,
    "LOW": 1,
    "INFO": 0
  },
  "vulnerabilities": [
    {
      "id": "uuid-1234",
      "name": "Command Injection",
      "severity": "CRITICAL",
      "file": "app.py",
      "line": 42,
      "description": "Using os.system() with user input",
      "fix": "Use subprocess with shell=False",
      "code": "os.system(user_input)",
      "cwe": "CWE-78"
    }
  ]
}

```

### Error Response

```json

{
  "error": "Description of the error"
}

```

## 💻 Supported Languages

| Language | Extension | Status |
|----------|-----------|--------|
| Python | `.py` | ✅ Full Support |
| JavaScript | `.js` | ✅ Full Support |
| TypeScript | `.ts` | ✅ Full Support |
| Java | `.java` | ✅ Full Support |
| PHP | `.php` | ✅ Full Support |
| C++ | `.cpp`, `.cc` | ✅ Full Support |
| C | `.c` | ✅ Full Support |
| Go | `.go` | ✅ Full Support |
| Ruby | `.rb` | ✅ Full Support |
| Rust | `.rs` | ✅ Full Support |
| Swift | `.swift` | ✅ Full Support |
| Kotlin | `.kt` | ✅ Full Support |

## 🔍 Examples

### Example 1: Scanning Vulnerable Python Code

**Input:**

```python

import os
def process(user_input):
    eval(user_input)  # Dangerous!
    os.system("rm -rf " + user_input)  # Command injection
    password = "admin123"  # Hardcoded secret

```

**Output:**

- ✅ 3 vulnerabilities detected

- 🔴 2 CRITICAL, 🟡 1 HIGH

- CWE-95 (Code Injection)

- CWE-78 (Command Injection)

- CWE-798 (Hardcoded Credentials)

### Example 2: API Response

```bash

$ curl -X POST http://localhost:5000/api/scan/paste
  -H "Content-Type: application/json"
  -d '{"code":"print(eval(input()))", "language":"py"}'
{
  "total_vulnerabilities": 1,
  "severity_counts": {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 0, "LOW": 0, "INFO": 0},
  "vulnerabilities": [{
    "name": "eval-detection",
    "severity": "HIGH",
    "description": "Use of eval() with user input",
    "line": 1
  }]
}

```

## 📁 Project Structure

```
security-code-scanner/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
│
├── templates/            # HTML templates
│   └── index.html       # Main web interface
│
├── static/              # Static assets (CSS, JS)
│   ├── style.css
│   └── script.js
│
├── scans/               # Temporary storage (auto-created)
|
└── scan_stats.json      # Scan statistics (optional)

```

## 📝 Configuration

### Change Port

```python

# In app.py, modify the last line:

app.run(debug=True, host='0.0.0.0', port=8080)  # Changed to port 8080

```

### Change Max File Size

```python

# In app.py, modify:

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB (default is 5MB)

```

### Add Custom Semgrep Rules

```python

# In app.py, modify the semgrep command:
cmd = ['semgrep', '--config', 'my-custom-rules/', '--json', file_path]

```

## 🎨 Screenshots

<details>

<summary>Click to view screenshots</summary>

### Home Page

<img width="1917" height="687" alt="image" src="https://github.com/user-attachments/assets/9918309d-f8b9-4a09-8a39-5b21b861f65c" />


### Scan Results

<img width="1161" height="679" alt="image" src="https://github.com/user-attachments/assets/8fb92da2-1746-4b15-9541-7bbebc757963" />


</details>

## 🐛 Troubleshooting

### Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `semgrep: command not found` | Run `pip3 install semgrep` |
| `Permission denied` | Use `sudo` or install with `--user` flag |
| `Port 5000 already in use` | Change port in app.py or kill process: `sudo lsof -i:5000` |
| `File too large` | Increase `MAX_CONTENT_LENGTH` in app.py |
| `No such file or directory` | Create required folders: `mkdir -p scans templates static` |





<div align="center">

**⭐ Star this repository if you find it useful! ⭐**

Made with ❤️ for the security community

</div>



## 📄 ملف requirements.txt إضافي

```txt
Flask==2.3.3
Werkzeug==2.3.7
requests==2.31.0
semgrep==1.45.0
```

