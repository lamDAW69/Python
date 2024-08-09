from abc import ABC, abstractmethod
from datetime import date

# Clases de Vehículo
class Vehiculo(ABC):
    def __init__(self, marca, modelo, matricula):
        self.marca = marca
        self.modelo = modelo
        self.matricula = matricula

    @abstractmethod
    def get_tipo(self):
        pass

class Coche(Vehiculo):
    def get_tipo(self):
        return "Coche"

class Moto(Vehiculo):
    def get_tipo(self):
        return "Moto"

class Furgoneta(Vehiculo):
    def get_tipo(self):
        return "Furgoneta"

class Autobus(Vehiculo):
    def get_tipo(self):
        return "Autobus"

# Factory para Vehículos
class VehiculoFactory:
    @staticmethod
    def crear_vehiculo(tipo, marca, modelo, matricula):
        tipos = {
            "coche": Coche,
            "moto": Moto,
            "furgoneta": Furgoneta,
            "autobus": Autobus
        }
        return tipos.get(tipo.lower())(marca, modelo, matricula)

# Clase Cliente
class Cliente:
    def __init__(self, nombre, apellido, dni):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.vehiculos = []

    def añadir_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

# Implementación del patrón Decorator para Servicios
class ServicioComponent(ABC):
    @abstractmethod
    def get_coste(self):
        pass

    @abstractmethod
    def get_descripcion(self):
        pass

class ServicioBase(ServicioComponent):
    def __init__(self, nombre, descripcion, precio_hora, horas):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_hora = precio_hora
        self.horas = horas

    def get_coste(self):
        return self.precio_hora * self.horas

    def get_descripcion(self):
        return f"{self.nombre}: {self.descripcion}"

class ServicioDecorator(ServicioComponent):
    def __init__(self, servicio):
        self._servicio = servicio

    def get_coste(self):
        return self._servicio.get_coste()

    def get_descripcion(self):
        return self._servicio.get_descripcion()

class ComponenteAdicional(ServicioDecorator):
    def __init__(self, servicio, nombre, coste):
        super().__init__(servicio)
        self.nombre = nombre
        self.coste = coste

    def get_coste(self):
        return super().get_coste() + self.coste

    def get_descripcion(self):
        return f"{super().get_descripcion()} + {self.nombre}"

# Clase Intervención
class Intervencion:
    def __init__(self, cliente, fecha):
        self.cliente = cliente
        self.fecha = fecha
        self.vehiculos = []
        self.servicios = []

    def añadir_vehiculo(self, vehiculo):
        self.vehiculos.append(vehiculo)

    def añadir_servicio(self, servicio):
        self.servicios.append(servicio)

# Clase Factura
class Factura:
    def __init__(self, intervencion):
        self.intervencion = intervencion

    def calcular_total(self):
        return sum(servicio.get_coste() for servicio in self.intervencion.servicios)

    def imprimir(self):
        print(f"Factura para {self.intervencion.cliente.nombre} {self.intervencion.cliente.apellido}")
        print(f"Fecha: {self.intervencion.fecha}")
        print("Vehículos:")
        for vehiculo in self.intervencion.vehiculos:
            print(f"- {vehiculo.get_tipo()}: {vehiculo.marca} {vehiculo.modelo} ({vehiculo.matricula})")
        print("Servicios:")
        for servicio in self.intervencion.servicios:
            print(f"- {servicio.get_descripcion()}: {servicio.get_coste()}€")
        print(f"Total: {self.calcular_total()}€")