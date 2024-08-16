from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from logica_negocio import db, Cliente, Reparacion, Factura
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/clientes', methods=['GET', 'POST'])
def clientes():
    if request.method == 'GET':
        clientes = Cliente.query.all()
        return jsonify([{
            'id': cliente.id,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'reparaciones': [{
                'id': reparacion.id,
                'descripcion': reparacion.descripcion,
                'fecha': str(reparacion.fecha),
                'coste': reparacion.coste
            } for reparacion in cliente.reparaciones]
        } for cliente in clientes])
    elif request.method == 'POST':
        data = request.json
        cliente = Cliente(nombre=data['nombre'], apellido=data['apellido'])
        db.session.add(cliente)
        db.session.commit()
        return jsonify({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'reparaciones': []
        }), 201

@app.route('/clientes/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def cliente(id):
    cliente = Cliente.query.get(id)
    if not cliente:
        return jsonify({'error': 'No encontrado'}), 404

    if request.method == 'GET':
        return jsonify({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'reparaciones': [{
                'id': reparacion.id,
                'descripcion': reparacion.descripcion,
                'fecha': str(reparacion.fecha),
                'coste': reparacion.coste
            } for reparacion in cliente.reparaciones]
        })
    elif request.method == 'PUT':
        data = request.json
        cliente.nombre = data['nombre']
        cliente.apellido = data['apellido']
        db.session.commit()
        return jsonify({
            'id': cliente.id,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'reparaciones': [{
                'id': reparacion.id,
                'descripcion': reparacion.descripcion,
                'fecha': str(reparacion.fecha),
                'coste': reparacion.coste
            } for reparacion in cliente.reparaciones]
        })
    elif request.method == 'DELETE':
        db.session.delete(cliente)
        db.session.commit()
        return '', 204

@app.route('/reparaciones', methods=['GET', 'POST'])
def reparaciones():
    if request.method == 'GET':
        reparaciones = Reparacion.query.all()
        return jsonify([{
            'id': reparacion.id,
            'descripcion': reparacion.descripcion,
            'fecha': str(reparacion.fecha),
            'coste': reparacion.coste,
            'cliente': {
                'id': reparacion.cliente.id,
                'nombre': reparacion.cliente.nombre,
                'apellido': reparacion.cliente.apellido
            },
            'factura': {
                'id': reparacion.factura.id,
                'fecha': str(reparacion.factura.fecha),
                'total': reparacion.factura.total
            } if reparacion.factura else None
        } for reparacion in reparaciones])
    elif request.method == 'POST':
        data = request.json
        cliente = Cliente.query.get(data['cliente_id'])
        if not cliente:
            return jsonify({'error': 'Cliente no encontrado'}), 404
        reparacion = Reparacion(
            descripcion=data['descripcion'],
            fecha=date.fromisoformat(data['fecha']),
            coste=data['coste'],
            cliente=cliente
        )
        db.session.add(reparacion)
        db.session.commit()
        return jsonify({
            'id': reparacion.id,
            'descripcion': reparacion.descripcion,
            'fecha': str(reparacion.fecha),
            'coste': reparacion.coste,
            'cliente': {
                'id': reparacion.cliente.id,
                'nombre': reparacion.cliente.nombre,
                'apellido': reparacion.cliente.apellido
            },
            'factura': None
        }), 201

@app.route('/facturas', methods=['GET', 'POST'])
def facturas():
    if request.method == 'GET':
        facturas = Factura.query.all()
        return jsonify([{
            'id': factura.id,
            'fecha': str(factura.fecha),
            'total': factura.total,
            'reparaciones': [{
                'id': reparacion.id,
                'descripcion': reparacion.descripcion,
                'fecha': str(reparacion.fecha),
                'coste': reparacion.coste
            } for reparacion in factura.reparaciones]
        } for factura in facturas])
    elif request.method == 'POST':
        data = request.json
        reparaciones = Reparacion.query.filter(Reparacion.id.in_(data['reparacion_ids'])).all()
        if not reparaciones:
            return jsonify({'error': 'Reparaciones no encontradas'}), 404
        factura = Factura(
            fecha=date.fromisoformat(data['fecha']),
            total=sum(r.coste for r in reparaciones),
            reparaciones=reparaciones
        )
        db.session.add(factura)
        db.session.commit()
        return jsonify({
            'id': factura.id,
            'fecha': str(factura.fecha),
            'total': factura.total,
            'reparaciones': [{
                'id': reparacion.id,
                'descripcion': reparacion.descripcion,
                'fecha': str(reparacion.fecha),
                'coste': reparacion.coste
            } for reparacion in factura.reparaciones]
        }), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host = '0.0.0.0' ,debug=True)

    #Importante poner '0.0.0.0' para que sea visible desde el exterior y pueda atender peticiones desde cualquier servidor