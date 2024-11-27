import os
from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename
from manual_censor import censor_faces_mediapipe

app = Flask(__name__)

# Configuración
UPLOAD_FOLDER = 'static/uploads'
CENSORED_FOLDER = 'static/censored'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CENSORED_FOLDER'] = CENSORED_FOLDER

# Crear directorios si no existen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CENSORED_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                censored_path = censor_faces_mediapipe(filepath, app.config['CENSORED_FOLDER'], pixelado=True)
                
                if censored_path and os.path.exists(censored_path):
                    # Usar rutas relativas a static/
                    original_path = f"uploads/{filename}"
                    censored_rel_path = f"censored/{os.path.basename(censored_path)}"
                    
                    print(f"Original path: {original_path}")  # Debug
                    print(f"Censored path: {censored_rel_path}")  # Debug
                    
                    return render_template('index.html', 
                                        original=original_path, 
                                        censored=censored_rel_path)
                else:
                    return "Error al procesar la imagen", 500
                    
            except Exception as e:
                print(f"Error: {str(e)}")
                return "Error al procesar la imagen", 500
                
    return render_template('index.html', original=None, censored=None)

if __name__ == '__main__':
    app.run(debug=True)