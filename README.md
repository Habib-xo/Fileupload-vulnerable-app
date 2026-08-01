# File Upload Security Lab - Level 1

A dockerized vulnerable web application built with Python (Flask) demonstrating an **Unrestricted File Upload** vulnerability.

---

## Vulnerability Description
In **Level 1**, the application accepts file uploads without enforcing checks on:
- File extensions (e.g., `.py`, `.sh`, `.php`).
- Content-Type / MIME headers.
- File integrity or content.

This allows an attacker to upload arbitrary files to the server and potentially achieve **Remote Code Execution (RCE)**.

---

## How to Run with Docker

1. **Clone the repository:**
   
   git clone [https://github.com/Habib-xo/Fileupload-vulnerable-app.git](https://github.com/Habib-xo/Fileupload-vulnerable-app.git)
   cd Fileupload-vulnerable-app

2. **Build and run the container:**

- docker build -t file-upload-lab .
- docker run -p 5000:5000 file-upload-lab

3. **Access the application:**
   Open your browser and navigate to: http://localhost:5000

## Mitigation / Secure Code fix

To fix this vulnerability in a production environment:

- Enforce strict file extension whitelisting (e.g., allowing only .jpg, .png).

- Rename uploaded files using random identifiers (e.g., UUIDs).

- Store uploaded files outside the public web-root folder.