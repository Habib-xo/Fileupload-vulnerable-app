# File Upload Security Labs (Dockerized)

A hands-on, dockerized vulnerable web application built with **Python (Flask)** demonstrating common **File Upload Security Vulnerabilities** and their bypass techniques.

Designed for security researchers, penetration testers, and developers to practice exploit logic and secure coding.

---

## Project Architecture

The project follows a clean, modular Flask structure:

```text
file-upload-lab/
├── app.py              # Main application logic & routes
├── Dockerfile          # Container environment configuration
├── static/
│   └── style.css       # Clean UI styling
└── templates/
    ├── index.html      # Main Lab Hub
    └── level.html      # Dynamic template for all lab levels
```
---
## 🎯 Lab Levels Overview

### Level 1: Unrestricted File Upload (No Validation)
* **Protection:** None.
* **Vulnerability:** The application accepts and saves files without inspecting their extensions or content.
* **Exploitation:** Direct upload of executable scripts leading to **Remote Code Execution (RCE)**.

### Level 2: Content-Type / MIME Check Bypass
* **Protection:** Validates incoming HTTP `Content-Type` headers against allowed image types (`image/png`, `image/jpeg`).
* **Vulnerability:** Relies on client-supplied headers without inspecting actual file bytes.
* **Exploitation:** Intercept the upload request using **Burp Suite** and modify the `Content-Type` header to `image/png`.

### Level 3: Extension Blacklist Bypass (Case Sensitivity)
* **Protection:** Enforces a blacklist blocking sensitive file extensions (`.py`, `.php`, `.sh`, `.exe`).
* **Vulnerability:** Case-sensitive string comparison — fails to normalize extensions using `.lower()`.
* **Exploitation:** Rename the payload extension to uppercase or mixed-case (e.g., `shell.PY` or `script.PhP`) to bypass the filter.

### Level 4: Extension Whitelist Bypass (Double Extension)
* **Protection:** Enforces an extension whitelist (`.png`, `.jpg`).
* **Vulnerability:** Weak string parsing — the server checks the first extension after the split rather than the final file extension.
* **Exploitation:** Upload a payload named using double extensions (e.g., `exploit.png.py`). The server validates `.png` and accepts the upload, while the OS/interpreter executes `.py`.

### Level 5: Secure Implementation (Patched)
* **Protection:** 
  1. Strict extension Whitelisting (`.png`, `.jpg`, `.jpeg`).
  2. Input normalization using `.lower()`.
  3. Randomized UUID filename generation (prevents execution of original scripts & path traversal).
* **Result:** **Fully Secured** against bypass attempts.

## How to run with Docker

Prerequests
- Docker installed on your system.

Steps
1. Clone the repostiry: 

```bash
git clone https://github.com/Habib-xo/Fileupload-vulnerable-app.git
cd Fileupload-vulnerable-app
```

2. Build the Docker image:

```bash
docker build -t file-upload-lab .
```

3. Run the container 
```bash
docker run -p 5000:5000 file-upload-lab
```
4. Access the application at http://localhost:5000

## Mitigation & Secure Implementation

To completely secure file upload functions in production:

1. Strict Whitelisting: Enforce server-side file extension whitelisting (e.g., allow strictly .jpg, .png).

2. Re-validation: Validate file contents/magic bytes using image processing libraries (e.g., Pillow), not just headers.

3. Randomized File Names: Rename uploaded files using UUIDs to prevent direct path guessing or execution.

4. Isolate Storage: Store uploaded files outside the web root or on an isolated media server with execution permissions disabled.