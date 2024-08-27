import requests  # Importa la librería requests para realizar solicitudes HTTP
from datetime import datetime  # Importa datetime para manejar y formatear fechas
import matplotlib  # Importa matplotlib para la generación de gráficos
matplotlib.use('Agg')  # Configura matplotlib para usar 'Agg', para generar gráficos sin una interfaz gráfica
import matplotlib.pyplot as plt  # Importa pyplot para la creación de gráficos
from io import BytesIO  # Importa BytesIO para manejar datos binarios en memoria

# Constante que almacena la API Key para acceder a OpenWeather
API_KEY_OPENWEATHER = '36716e91288f48d1fb0d996c17c7ce73'

# Función para obtener los datos meteorológicos de una ciudad específica usando la API de OpenWeather
def obtener_datos_tiempo(ciudad):
    # Construye la URL para realizar la solicitud a la API de OpenWeather
    url = f"http://api.openweathermap.org/data/2.5/forecast?lang=es&units=metric&appid={API_KEY_OPENWEATHER}&q={ciudad}"
    response = requests.get(url)  # Realiza la solicitud GET a la API
    if response.status_code == 200:  # Verifica si la solicitud fue exitosa
        data = response.json()  # Convierte la respuesta en formato JSON a un diccionario de Python
        return data  # Retorna los datos del pronóstico meteorológico
    else:
        return None  # Retorna None si hubo algún error en la solicitud

# Función para generar un gráfico de la evolución de las temperaturas en una ciudad específica
def generar_grafico_tiempo(datos, ciudad):
    fechas = []  # Lista para almacenar las fechas y horas del pronóstico
    temperaturas = []  # Lista para almacenar las temperaturas correspondientes

    # Itera sobre cada entrada en la lista de pronósticos de la API
    for item in datos['list']:
        # Convierte la cadena de texto de la fecha y hora a un objeto datetime
        fecha_obj = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S')
        # Formatea la fecha en un formato más legible
        fecha_formateada = fecha_obj.strftime('%d %b %H:%M')
        fechas.append(fecha_formateada)  # Añade la fecha formateada a la lista
        temperaturas.append(item['main']['temp'])  # Añade la temperatura a la lista

    # Crea una nueva imagen para el gráfico con un tamaño específico
    plt.figure(figsize=(10, 6.5))
    # Grafica las temperaturas a lo largo del tiempo con un estilo de línea y marcadores
    plt.plot(fechas, temperaturas, marker='o', linestyle='-', color='b')
    # Añade un título al gráfico con el nombre de la ciudad
    plt.title(f'Temperaturas previstas para {ciudad}', fontsize=16)
    # Añade etiquetas a los ejes X e Y
    plt.xlabel("Fecha y Hora", fontsize=14)
    plt.ylabel("Temperaturas (°C)", fontsize=14)
    plt.xticks(rotation=45, ha='right')  # Rota las etiquetas del eje X para mejor legibilidad
    plt.grid(True)  # Activa la cuadrícula en el gráfico para mejorar la visualización
    plt.tight_layout()  # Ajusta automáticamente el diseño para evitar superposiciones

    # Guarda el gráfico en un objeto BytesIO en formato PNG
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  # Posiciona el cursor al inicio del objeto BytesIO para su lectura posterior
    plt.close('all')  # Cierra todas las imágenes abiertas para liberar memoria

    # Retorna la imagen generada como un archivo binario
    return img
