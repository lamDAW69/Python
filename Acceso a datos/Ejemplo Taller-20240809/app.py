from flask import Flask, request, jsonify
from abc import ABC, abstractmethod
from logica_negocio import Cliente, VehiculoFactory, ServicioBase, ComponenteAdicional, Intervencion, Factura

app = Flask(__name__)

# Clase base para los controladores REST
class BaseController(ABC):
    def __init__(self):
        self.items = []
        self.next_id = 1

    def _search_by_id(self,id):
            return next((item for item in self.items if item.id == id), None)

    def get_all(self):
        return jsonify([self.to_dict(item) for item in self.items])

    def get_one(self, id):
        item = self._search_by_id(id)
        if item is None:
            return jsonify({"error": "No encontrado"}), 404
        return jsonify(self.to_dict(item))

    def create(self):
        data = request.json
        item = self.create_item(data)
        item.id = self.next_id
        self.next_id += 1
        self.items.append(item)
        return jsonify(self.to_dict(item)), 201
    
    

    def update(self, id):
        item = self._search_by_id(id)
        if item is None:
            return jsonify({"error": "No encontrado"}), 404
        data = request.json
        self.update_item(item, data)
        return jsonify(self.to_dict(item))

    def delete(self, id):
        item = self._search_by_id(id)
        if item is None:
            return jsonify({"error": "No encontrado"}), 404
        self.items.remove(item)
        return '', 204

    @abstractmethod
    def to_dict(self, item):
        pass

    @abstractmethod
    def create_item(self, data):
        pass

    @abstractmethod
    def update_item(self, item, data):
        pass

# Controladores específicos
class ClienteController(BaseController):
    def to_dict(self, item):
        return {
            'id': item.id,
            'nombre': item.nombre,
            'apellido': item.apellido,
            'dni': item.dni,
            'vehiculos': [{'tipo': v.get_tipo(), 'marca': v.marca, 'modelo': v.modelo, 'matricula': v.matricula} for v in item.vehiculos]
        }

    def create_item(self, data):
        cliente = Cliente(data['nombre'], data['apellido'], data['dni'])
        if 'vehiculos' in data:
            for v in data['vehiculos']:
                vehiculo = VehiculoFactory.crear_vehiculo(v['tipo'], v['marca'], v['modelo'], v['matricula'])
                cliente.añadir_vehiculo(vehiculo)
        return cliente

    def update_item(self, item, data):
        item.nombre = data.get('nombre', item.nombre)
        item.apellido = data.get('apellido', item.apellido)
        item.dni = data.get('dni', item.dni)
        if 'vehiculos' in data:
            item.vehiculos = []
            for v in data['vehiculos']:
                vehiculo = VehiculoFactory.crear_vehiculo(v['tipo'], v['marca'], v['modelo'], v['matricula'])
                item.añadir_vehiculo(vehiculo)

class ServicioController(BaseController):
    def to_dict(self, item):
        return {
            'id': item.id,
            'nombre': item.nombre,
            'descripcion': item.descripcion,
            'precio_hora': item.precio_hora,
            'horas': item.horas
        }

    def create_item(self, data):
        servicio = ServicioBase(data['nombre'], data['descripcion'], data['precio_hora'], data['horas'])
        if 'componentes_adicionales' in data:
            for comp in data['componentes_adicionales']:
                servicio = ComponenteAdicional(servicio, comp['nombre'], comp['coste'])
        return servicio

    def update_item(self, item, data):
        item.nombre = data.get('nombre', item.nombre)
        item.descripcion = data.get('descripcion', item.descripcion)
        item.precio_hora = data.get('precio_hora', item.precio_hora)
        item.horas = data.get('horas', item.horas)

class IntervencionController(BaseController):
    def to_dict(self, item):
        return {
            'id': item.id,
            'cliente': cliente_controller.to_dict(item.cliente),
            'fecha': str(item.fecha),
            'vehiculos': [{'tipo': v.get_tipo(), 'marca': v.marca, 'modelo': v.modelo, 'matricula': v.matricula} for v in item.vehiculos],
            'servicios': [servicio_controller.to_dict(s) for s in item.servicios]
        }

    def create_item(self, data):
        cliente = next((c for c in cliente_controller.items if c.id == data['cliente_id']), None)
        if cliente is None:
            raise ValueError("Cliente no encontrado")
        intervencion = Intervencion(cliente, date.fromisoformat(data['fecha']))
        for v_id in data.get('vehiculos_ids', []):
            vehiculo = next((v for v in cliente.vehiculos if v.id == v_id), None)
            if vehiculo:
                intervencion.añadir_vehiculo(vehiculo)
        for s_id in data.get('servicios_ids', []):
            servicio = next((s for s in servicio_controller.items if s.id == s_id), None)
            if servicio:
                intervencion.añadir_servicio(servicio)
        return intervencion

    def update_item(self, item, data):
        if 'cliente_id' in data:
            cliente = next((c for c in cliente_controller.items if c.id == data['cliente_id']), None)
            if cliente:
                item.cliente = cliente
        if 'fecha' in data:
            item.fecha = date.fromisoformat(data['fecha'])
        if 'vehiculos_ids' in data:
            item.vehiculos = []
            for v_id in data['vehiculos_ids']:
                vehiculo = next((v for v in item.cliente.vehiculos if v.id == v_id), None)
                if vehiculo:
                    item.añadir_vehiculo(vehiculo)
        if 'servicios_ids' in data:
            item.servicios = []
            for s_id in data['servicios_ids']:
                servicio = next((s for s in servicio_controller.items if s.id == s_id), None)
                if servicio:
                    item.añadir_servicio(servicio)

class FacturaController(BaseController):
    def to_dict(self, item):
        return {
            'id': item.id,
            'intervencion': intervencion_controller.to_dict(item.intervencion),
            'total': item.calcular_total()
        }

    def create_item(self, data):
        intervencion = next((i for i in intervencion_controller.items if i.id == data['intervencion_id']), None)
        if intervencion is None:
            raise ValueError("Intervención no encontrada")
        return Factura(intervencion)

    def update_item(self, item, data):
        if 'intervencion_id' in data:
            intervencion = next((i for i in intervencion_controller.items if i.id == data['intervencion_id']), None)
            if intervencion:
                item.intervencion = intervencion

# Instancias de los controladores
cliente_controller = ClienteController()
servicio_controller = ServicioController()
intervencion_controller = IntervencionController()
factura_controller = FacturaController()

# Función para registrar rutas dinámicamente
def register_routes(app, controller, base_route):
    app.add_url_rule(f'/{base_route}', f'get_all_{base_route}', controller.get_all, methods=['GET'])
    app.add_url_rule(f'/{base_route}/<int:id>', f'get_one_{base_route}', controller.get_one, methods=['GET'])
    app.add_url_rule(f'/{base_route}', f'create_{base_route}', controller.create, methods=['POST'])
    app.add_url_rule(f'/{base_route}/<int:id>', f'update_{base_route}', controller.update, methods=['PUT'])
    app.add_url_rule(f'/{base_route}/<int:id>', f'delete_{base_route}', controller.delete, methods=['DELETE'])

# Registrar rutas para cada entidad
register_routes(app, cliente_controller, 'clientes')
register_routes(app, servicio_controller, 'servicios')
register_routes(app, intervencion_controller, 'intervenciones')
register_routes(app, factura_controller, 'facturas')

if __name__ == '__main__':
    app.run(debug=True)