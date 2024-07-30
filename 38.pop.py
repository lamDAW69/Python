# #Crea la clase Persona con nombre y edad

# Implementa los siguiente métodos
# - Representar como str: Pepito - 25
# - Comparar con < (por edad)
# - Comparar con == (por nombre y edad)

# Crea una lista de personas y ordénala.
# Después muestra la lista 
# Finalmente compara si 2 personas con los mismos atributos son iguales

# Definición de la clase Persona

class Persona:
    def __init__(self, nombre, edad):       # Constructor	
        self.nombre = nombre
        self.edad = edad
    
    def __str__(self):                          # Representar como str: Pepito - 25
        return f"{self.nombre} - {self.edad}"
    
    def __lt__(self, other):                        # Comparar con < (por edad)
        return self.edad < other.edad
    
    def __eq__(self, other):                            # Comparar con == (por nombre y edad)	
        return self.nombre == other.nombre and self.edad == other.edad

personas = [Persona("Pepito", 25), Persona("Juanito", 20), Persona("Maria", 30)]

personas_ordenadas = sorted(personas)  # Ordenar la lista de personas

for persona in personas_ordenadas:      # Mostrar la lista de personas
    print(persona)

persona1 = personas[2]
persona2 = personas[0]
print(persona1 == persona2)
