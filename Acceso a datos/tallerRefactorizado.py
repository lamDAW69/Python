import uuid
from  flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)


@app.route('/') #Endpoint
def hello():
    return 'Hello, World!'

#Almacenamiento en memoria

usuarios = []
servicios = []
intervenciones = []
facturas = []


class Usuario: 
    def __init__(self, id, nombre, email): 
        self.id = id
        self.nombre = nombre
        self.email = email


class Servicio: 
    def __init__(self, id, nombre, precio): 
        self.id = id
        self.nombre = nombre
        self.precio = precio

class Intervencion: 
    def __init__(self, id, id_usuario, id_servicio, fecha): 
        self.id = id
        self.id_usuario = id_usuario
        self.id_servicio = id_servicio
        self.fecha = fecha

class Factura:
    def __init__(self, id, id_intervencion, importe): 
        self.id = id
        self.id_intervencion = id_intervencion
        self.importe = importe

def generador_id():
    return str(uuid.uuid4())

##Rutas para los cruds

@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify({"usuarios": usuarios})

@app.route('/usuarios', methods= ['POST'])
def crearUsuario(): 
     data = request.json
     id = generador_id()
     nuevo_usuario = Usuario(id = id, nombre = data['nombre'], email= data['email'])
     usuarios.append(nuevo_usuario)
     return jsonify({'Mensaje': 'Usuario creado correctamente'}), 201

@app.route('/usuarios/<string:id>', methods= ['PUT'])
def actualizarUsuario(id): 
    data = request.json
    usuario = next((usuario for usuario in usuarios if usuario.id == id), None)
    if usuario: 
        usuario.nombre = data['nombre']
        usuario.email = data['email']
        return jsonify({'Mensaje': 'Usuario actualizado correctamente'})
    return jsonify({'Error': 'Usuario no encontrado'}), 404

@app.route('/usuarios/<string:id>', methods= ['DELETE'])
def eliminarUsuario(id): 
    usuario = next((usuario for usuario in usuarios if usuario.id == id), None)
    if usuario: 
        usuarios.remove(usuario)
        return jsonify({'Mensaje': 'Usuario eliminado correctamente'})
    return jsonify({'Error': 'Usuario no encontrado'}), 404

if __name__ == '__main__':  #Esto lanza la app
    app.run(debug=True)

     
