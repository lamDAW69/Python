import requests  # Importa la librería requests para realizar solicitudes HTTP
import pandas as pd  # Importa pandas para manipulación y análisis de datos
import matplotlib  # Importa matplotlib para la generación de gráficos
matplotlib.use('Agg')  # Configura matplotlib para usar 'Agg', para generar gráficos sin una interfaz gráfica
import matplotlib.pyplot as plt  # Importa pyplot para la creación de gráficos
from io import BytesIO  # Importa BytesIO para manejar datos binarios en memoria

# Constante global que define el número por defecto de Pokémon a procesar
NUM_POKEMONS = 10

# Función para obtener datos de un Pokémon específico usando la API de PokeAPI
def obtener_datos_pokemon(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"  # URL de la API con el ID del Pokémon
    response = requests.get(url)  # Realiza la solicitud GET a la API
    if response.status_code == 200:  # Verifica si la solicitud fue exitosa
        data = response.json()  # Convierte la respuesta en formato JSON a un diccionario de Python
        return data  # Retorna los datos del Pokémon
    else:
        return None  # Retorna None si la solicitud no fue exitosa

# Función para cargar datos de varios Pokémon y organizarlos en un DataFrame
def cargar_datos_pokemons(num_pokemons):
    pokemon_data = []  # Lista para almacenar la información de cada Pokémon
    for i in range(1, num_pokemons + 1):  # Itera desde 1 hasta el número especificado de Pokémon
        data = obtener_datos_pokemon(i)  # Obtiene los datos de cada Pokémon
        if data:  # Si los datos fueron obtenidos correctamente
            # Extrae y organiza la información relevante del Pokémon
            pokemon_info = {
                "Nombre": data["name"],
                "Altura": data["height"],
                "Peso": data["weight"],
                "Tipos": [t["type"]["name"] for t in data["types"]]
            }
            pokemon_data.append(pokemon_info)  # Añade la información del Pokémon a la lista
    return pd.DataFrame(pokemon_data)  # Convierte la lista de datos en un DataFrame de pandas y lo retorna

# Función para analizar los datos de los Pokémon en el DataFrame
def analizar_datos(df):
    # Calcula el peso promedio y la altura promedio de los Pokémon
    peso_promedio = df["Peso"].mean()
    altura_promedio = df["Altura"].mean()

    # Expande la columna de tipos (que es una lista) y cuenta la frecuencia de cada tipo
    todos_los_tipos = df.explode("Tipos")["Tipos"]
    distribucion_tipos = todos_los_tipos.value_counts()  # Cuenta cuántos Pokémons hay de cada tipo

    distribucion_tipos_lista = list(distribucion_tipos.items())  # Convierte la distribución de tipos a una lista de tuplas

    # Organiza los resultados del análisis en un diccionario
    analisis = {
        "peso_promedio": peso_promedio,
        "altura_promedio": altura_promedio,
        "distribucion_tipos": distribucion_tipos_lista
    }

    # Retorna el análisis y la distribución de tipos
    return analisis, distribucion_tipos

# Función para generar un gráfico de la distribución de tipos de Pokémon
def generar_grafico_distribucion_tipos(distribucion_tipos):
    # Diccionario que asocia cada tipo de Pokémon con un color específico
    colores = {
        'normal': '#A8A77A',
        'fire': '#EE8130',
        'water': '#6390F0',
        'electric': '#F7D02C',
        'grass': '#7AC74C',
        'ice': '#96D9D6',
        'fighting': '#C22E28',
        'poison': '#A33EA1',
        'ground': '#E2BF65',
        'flying': '#A98FF3',
        'psychic': '#F95587',
        'bug': '#A6B91A',
        'rock': '#B6A136',
        'ghost': '#735797',
        'dragon': '#6F35FC',
        'dark': '#705746',
        'steel': '#B7B7CE',
        'fairy': '#D685AD'
    }
    # Genera una lista de colores correspondientes a los tipos en la distribución
    colores = [colores.get(tipo) for tipo in distribucion_tipos.index]

    # Crea una nueva imagen para el gráfico con un tamaño específico
    plt.figure(figsize=(10, 6.5))
    # Genera un gráfico de barras con la distribución de tipos y los colores especificados
    distribucion_tipos.plot(kind="bar", color=colores)
    # Añade un título y etiquetas a los ejes del gráfico
    plt.title("Distribución de tipos de Pokémon")
    plt.xlabel("Tipo")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)  # Rota las etiquetas del eje X para mejor legibilidad
    plt.tight_layout()  # Ajusta el diseño para que todos los elementos se visualicen correctamente

    # Guarda el gráfico en un objeto BytesIO en formato PNG
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  # Posiciona el cursor al inicio del objeto BytesIO para su lectura posterior
    plt.close('all')  # Cierra todas las imágenes abiertas para liberar memoria

    # Retorna la imagen generada como un archivo binario
    return img
