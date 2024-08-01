from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# Lista para almacenar usuarios
usuarios = []

# Función auxiliar para buscar usuarios por ID
def buscar_usuario(id):
    return next((usuario for usuario in usuarios if usuario['id'] == id), None)

# Ruta raíz
@app.route('/')
def inicio():
    return jsonify({"mensaje": "API de gestión de usuarios"})

# Obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({"usuarios": usuarios})

# Obtener un usuario específico
@app.route('/usuarios/<string:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = buscar_usuario(id)
    if usuario:
        return jsonify(usuario)
    return jsonify({"error": "Usuario no encontrado"}), 404

# Crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    nuevo_usuario = request.json
    if not nuevo_usuario or 'nombre' not in nuevo_usuario or 'email' not in nuevo_usuario:
        return jsonify({"error": "Datos incompletos"}), 400
    
    nuevo_usuario['id'] = str(uuid.uuid4())
    usuarios.append(nuevo_usuario)
    return jsonify(nuevo_usuario), 201

# Actualizar un usuario existente
@app.route('/usuarios/<string:id>', methods=['PUT'])
def actualizar_usuario(id):
    usuario = buscar_usuario(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    datos = request.json
    if 'nombre' in datos:
        usuario['nombre'] = datos['nombre']
    if 'email' in datos:
        usuario['email'] = datos['email']
    
    return jsonify(usuario)

# Eliminar un usuario
@app.route('/usuarios/<string:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = buscar_usuario(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    usuarios.remove(usuario)
    return jsonify({"mensaje": "Usuario eliminado"})

# Búsqueda de usuarios por nombre
@app.route('/usuarios/buscar', methods=['GET'])
def buscar_usuarios():
    nombre = request.args.get('nombre', '')
    if not nombre:
        return jsonify({"error": "Parámetro de búsqueda 'nombre' requerido"}), 400
    
    resultados = [usuario for usuario in usuarios if nombre.lower() in usuario['nombre'].lower()]
    return jsonify({"resultados": resultados})

# Añadir amigo a un usuario
@app.route('/usuarios/<string:id>/amigos', methods=['POST'])
def añadir_amigo(id):
    usuario = buscar_usuario(id)
    if not usuario:
        return jsonify({"error": "Usuario no encontrado"}), 404
    
    amigo_id = request.json.get('amigo_id')
    if not amigo_id:
        return jsonify({"error": "ID de amigo no proporcionado"}), 400
    
    amigo = buscar_usuario(amigo_id)
    if not amigo:
        return jsonify({"error": "Amigo no encontrado"}), 404
    
    if 'amigos' not in usuario:
        usuario['amigos'] = []
    
    if amigo_id not in usuario['amigos']:
        usuario['amigos'].append(amigo_id)
        return jsonify({"mensaje": "Amigo añadido", "usuario": usuario})
    else:
        return jsonify({"mensaje": "El amigo ya está en la lista"})

if __name__ == '__main__':
    # Añadir algunos usuarios de ejemplo
    usuarios.extend([
        {"id": str(uuid.uuid4()), "nombre": "Ana García", "email": "ana@example.com"},
        {"id": str(uuid.uuid4()), "nombre": "Carlos López", "email": "carlos@example.com"},
        {"id": str(uuid.uuid4()), "nombre": "María Rodríguez", "email": "maria@example.com"}
    ])
    app.run(debug=True)