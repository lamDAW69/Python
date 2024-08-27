import matplotlib
matplotlib.use('Agg')  # Configura matplotlib para usar 'Agg', para generar gráficos sin necesidad de una pantalla
import matplotlib.pyplot as plt  # Importa pyplot de matplotlib para la creación de gráficos
import yfinance as yf  # Importa la librería yfinance para descargar datos financieros
from io import BytesIO  # Importa BytesIO para manejar datos binarios en memoria

# Función para obtener los datos históricos de una empresa específica en un período determinado
def obtener_datos_empresas(empresa, periodo):
    # Descarga los datos históricos de la empresa usando yfinance
    datos = yf.download(empresa, period=periodo)
    return datos  # Retorna el DataFrame con los datos obtenidos

# Función para generar un gráfico de la evolución del precio de cierre de una empresa
def generar_grafico_empresas(empresa, periodo):
    # Obtiene los datos históricos de la empresa para el período especificado
    datos = obtener_datos_empresas(empresa, periodo)

    # Listas para almacenar las fechas y los precios de cierre
    fechas = []
    precios_cierre = []

    # Itera sobre las fechas de los datos obtenidos
    for fecha in datos.index:
        # Convierte la fecha a un objeto datetime
        fecha_obj = fecha.to_pydatetime()
        # Formatea la fecha en el formato que decidamos. En este caso: día, mes (en texto), año
        fecha_formateada = fecha_obj.strftime('%d %b %Y')
        # Agrega la fecha formateada y el precio de cierre a las listas
        fechas.append(fecha_formateada)
        precios_cierre.append(datos['Close'][fecha])

    # Crea una nueva imagen para el gráfico con un tamaño específico
    plt.figure(figsize=(10, 6.5))
    # Genera el gráfico con los precios de cierre a lo largo del tiempo
    plt.plot(fechas, precios_cierre, label='Precios de Cierre', color='b')

    # Añade un título al gráfico
    plt.title(f'Evolución de {empresa}', fontsize=16)
    # Añade una etiqueta al eje X (Fechas)
    plt.xlabel('Fecha', fontsize=14)
    # Obtiene la moneda en la que se expresan los precios y la usa para etiquetar el eje Y
    moneda = yf.Ticker(empresa).info['currency']
    plt.ylabel(f'Precio ({moneda})', fontsize=14)

    # Define el número de etiquetas en el eje X y su espaciado
    num_etiquetas = 10
    step = max(1, len(fechas) // num_etiquetas)
    plt.xticks(fechas[::step], rotation=45, ha='right')

    # Activa la cuadrícula en el gráfico para mejorar la legibilidad
    plt.grid(True)
    # Ajusta automáticamente el diseño para que los elementos no se superpongan
    plt.tight_layout()

    # Guarda el gráfico en un objeto BytesIO para manejarlo como un archivo en memoria
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  # Coloca el cursor al principio del objeto BytesIO para leerlo posteriormente
    plt.close('all')  # Cierra todas las imágenes abiertas para liberar memoria

    # Retorna la imagen generada como un archivo binario
    return img
