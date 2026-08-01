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
## Lab Levels Overview

### Level 1: Unrestricted file upload (No Validation)

- Vulnerability: The server accepts and stores any uploaded file without validation.

- Impact: Arbitrary file upload leading to Remote Code Execution (RCE).

- Exploitation: Upload any executable file/script directly and trigger it via /uploads/<filename>.

### Level 2: Content-Type / MIME Check Bypass

- Protection: The server validates the Content-Type header sent in the HTTP request (allows only image/png, image/jpeg).

- Vulnerability: Weak server-side logic relying purely on client-supplied headers.

- Exploitation: Upload a script (e.g., .py / .php), intercept the request in Burp Suite, and modify the Content-Type header to image/png.

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