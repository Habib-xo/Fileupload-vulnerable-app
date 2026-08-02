import uuid
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

    #===================== vulnerable part ==================================
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) #Saves the file directly without any form of validation
    return render_template('level.html', level=1, success=True, filename=filename)
    #========================================================================


# LEVEL 2
@app.route('/level2')
def level2_index():
    return render_template('level.html', level=2, title="Level 2: MIME Check", protection="Protection: Content-Type (Images Only)", action_url="/level2/upload")

@app.route('/level2/upload', methods=['POST'])
def level2_upload():
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template('level.html', level=2, error="No file selected!"), 400

    #======================== protection by content type only ===============================
    uploaded_file = request.files['file']
    allowed_mimes = ['image/png', 'image/jpeg', 'image/jpg']

    if uploaded_file.content_type not in allowed_mimes: #intercepting the request and spoof the header of content type and set to image/png can simply bypass the protection
        return render_template('level.html', level=2, error=f"Access Denied! Only Images Allowed. Received: {uploaded_file.content_type}"), 403

    filename = uploaded_file.filename
    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
    return render_template('level.html', level=2, success=True, filename=filename)
    #========================================================================================

@app.route('/level3')
def level3_index():
    return render_template('level.html',level=3, 
                           title='Level 3: Blacklist filter',
                           protection="Protection: Extension Blacklist (Blocks .py, .php, .sh)",
                            action_url="/level3/upload")

@app.route('/level3/upload', methods=['POST'])
def level3_upload():
    if 'file' not in request.files or request.files['file'] == '':
        return render_template('level.html', level=3, error="No file selected !"), 400

    uploaded_file = request.files['file']
    filename = uploaded_file.filename

    #======================== Blacklist Protection ============================
    blacklisted_extension = ['.py', '.php', '.sh', '.exe'] 
    file_ext = os.path.splitext(filename)[1]

    if file_ext in blacklisted_extension: # !!! checks if extension in blacklist but fails to normalize input using .lower() '.PY' bypasses '.py'
        return render_template('level.html', level=3, error=f"Access Denied! Extension '{file_ext}' is strictly forbidden."), 400
    #===========================================================================
    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('level.html', level=3, success=True, filename=filename)

@app.route('/level4')
def level4_index():
    return render_template('level.html', level=4, 
                           title="Level 4: Whitelist Filter", 
                           protection="Protection: Strict Whitelist (.png, .jpg only)", 
                           action_url="/level4/upload")

@app.route('/level4/upload', methods=['POST'])
def level4_upload():
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template('level.html', level=4, error="No file selected!"), 400

    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    allowed_extensions = ['png','jpg','jpeg']

    #==================================== Whitelist protection ==============================
    file_parts = filename.split('.')
    ext = file_parts[1].lower() if len(file_parts) > 1 else ''
    #The code only checks for the first extension so it can be bypassed by 'file.png.php'
    if ext not in allowed_extensions:
        return render_template('level.html', level=4, 
                               error=f"Access Denied! Extension '{ext}' is not allowed."), 403
    #=========================================================================================

    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template('level.html', level=4, success=True, filename=filename)

#=============================== Level 5 (The secure implementation) ===========================================
@app.route('/level5')
def level5_index():
    return render_template('level.html', level=5, 
                           title="Level 5: Secure Implementation", 
                           protection="Protection: Whitelist + Lowercase + UUID Renaming", 
                           action_url="/level5/upload")

@app.route('/level5/upload', methods=['POST'])
def level5_upload():
    if 'file' not in request.files or request.files['file'].filename == '':
        return render_template('level.html', level=5, error="No file selected!"), 400

    uploaded_file = request.files['file']
    original_filename = uploaded_file.filename
    allowed_extensions = ['.png','.jpg','.jpeg'] #whitelist by allowed extensions (1)

    file_ext = os.path.splitext(original_filename)[1].lower() #only get the last extension (2)

    if file_ext not in allowed_extensions: # blocking any extension not allowed (3)
        return render_template('level.html', level=5, 
                               error=f"Access Denied! Extension '{file_ext}' is strictly forbidden."), 403

    secure_filename = f"{uuid.uuid4().hex}{file_ext}" #rename the file by a random uuid 

    uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename))
    return render_template('level.html', level=5, success=True, filename=secure_filename)
 
@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)