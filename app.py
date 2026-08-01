import os
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template_string, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER ###

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>File Upload Lab - Level 1</title>
    <style>
        body { font-family: sans-serif; margin: 40px; }
        .container { max-width: 500px; padding: 20px; border: 1px solid #ccc; border-radius: 8px; }
        input[type=file] { margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>File Upload Security Lab</h2>
        <p><b>Level 1:</b> Unrestricted File Upload</p>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required><br>
            <input type="submit" value="Upload File">
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in request", 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return "No selected file",400

    if uploaded_file:
        filename = uploaded_file.filename
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        uploaded_file.save(save_path)

    return f'''
    <h3>File uploaded successfully!</h3>
    <p>File location: <code>/uploads/{filename}</code></p>
    <a href="/uploads/{filename}">View/Execute Uploaded File</a>
    <br><br>
    <a href="/">Back to upload</a>
    '''

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)