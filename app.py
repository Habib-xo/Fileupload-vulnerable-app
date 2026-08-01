import os
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

# LEVEL 1
@app.route('/level1')
def level1_index():
    return render_template('level.html', level=1, title="Level 1: Basic Upload", protection="Protection: Disabled", action_url="/level1/upload")

@app.route('/level1/upload', methods=['POST'])
def level1_upload():
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template('level.html', level=1, error="No file selected!"), 400

    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('level.html', level=1, success=True, filename=filename)

# LEVEL 2
@app.route('/level2')
def level2_index():
    return render_template('level.html', level=2, title="Level 2: MIME Check", protection="Protection: Content-Type (Images Only)", action_url="/level2/upload")

@app.route('/level2/upload', methods=['POST'])
def level2_upload():
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template('level.html', level=2, error="No file selected!"), 400

    uploaded_file = request.files['file']
    allowed_mimes = ['image/png', 'image/jpeg', 'image/jpg']

    if uploaded_file.content_type not in allowed_mimes:
        return render_template('level.html', level=2, error=f"Access Denied! Only Images Allowed. Received: {uploaded_file.content_type}"), 403

    filename = uploaded_file.filename
    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('level.html', level=2, success=True, filename=filename)

@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)