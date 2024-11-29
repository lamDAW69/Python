from flask import Flask, render_template, request, send_from_directory, redirect
import os
from werkzeug.utils import secure_filename
from censor import censor_faces_mediapipe  # Importamos la función sin ejecutarla automáticamente

app = Flask(__name__)

# Definir carpetas donde se guardan las imágenes
UPLOAD_FOLDER = 'static/uploads/'
CENSORED_FOLDER = 'static/censored/'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

# Configuración de las rutas
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CENSORED_FOLDER'] = CENSORED_FOLDER

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Verifica si el archivo está en la solicitud
        if 'file' not in request.files:
            return redirect(request.url)  # Redirigir si no hay archivo en la solicitud
        file = request.files['file']

        # Si el usuario no selecciona un archivo
        if file.filename == '':
            return redirect(request.url)  # Redirigir si no hay archivo seleccionado

        # Si el archivo es válido, guárdalo
        if file and allowed_file(file.filename):
            # Guardar archivo subido
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Verificar que el archivo se guardó correctamente
            if not os.path.exists(filepath):
                return f"Error: el archivo no se guardó correctamente en la ruta {filepath}"

            # Llamar a la función de censura de rostros (ahora dentro de la ruta)
            censored_image_path = censor_faces_mediapipe(filepath, app.config['CENSORED_FOLDER'], pixelado=True)

            # Verificar que la imagen censurada fue generada
            if not os.path.exists(censored_image_path):
                return f"Error: la imagen censurada no se generó correctamente."

            # Devuelve el archivo censurado al usuario para descarga
            return send_from_directory(app.config['CENSORED_FOLDER'], censored_image_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
