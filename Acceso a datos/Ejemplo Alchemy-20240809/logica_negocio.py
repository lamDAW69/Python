from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    reparaciones = db.relationship('Reparacion', backref='cliente', lazy='dynamic')

    def __repr__(self):
        return f'<Cliente {self.nombre} {self.apellido}>'

class Reparacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    coste = db.Column(db.Float, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    factura_id = db.Column(db.Integer, db.ForeignKey('factura.id'), nullable=True)

    def __repr__(self):
        return f'<Reparacion {self.descripcion}>'

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    total = db.Column(db.Float, nullable=False)
    reparaciones = db.relationship('Reparacion', backref='factura', lazy='dynamic')

    def __repr__(self):
        return f'<Factura {self.id}>'