import yfinance as yf

from io import BytesIO
from flask import Flask, send_file, request

import matplotlib 

matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)

empresas = {
    'apple': 'AAPL',
    'google': 'GOOGL',
    'amazon': 'AMZN',
    'tesla': 'TSLA',
    'microsoft' : 'MSFT',
    'facebook' : 'META',
    'netflix': 'NFLX',
    'spotify': 'SPOT',
    'uber': 'UBER',
    'adobe': 'ADBE',
    'salesforce': 'CRM',
    'intel' : 'INTC'
}
def obtener_datos_empresa(empresa, periodo):
    if empresa is None:
        return None
    empresa = empresas.get(empresa)
    datos = yf.download(empresa, period=periodo)
    print(datos)
    return datos

def generar_grafico_empresa(empresa, periodo): 
    datos = obtener_datos_empresa(empresa, periodo)

    fechas = []
    precios_cierre = []

    for fecha in datos.index:
        fecha_obj = fecha.to_pydatetime()
        fecha_formateada = fecha_obj.strftime('%d %b')
        fechas.append(fecha_formateada)
        precios_cierre.append(datos['Close'][fecha])

    plt.figure(figsize=(10, 6.5))
    plt.plot(fechas, precios_cierre, marker='o', linestyle='-', color='r')

    plt.title(f'Precio de cierre para {empresa}', fontsize=16)
    plt.xlabel("Fecha", fontsize=14)
    plt.ylabel("Precio de cierre", fontsize=14)

    num_etiquetas = 10
    step = len(fechas) // num_etiquetas
    plt.xticks(fechas[::step], rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img

@app.route('/finanzas/grafica', methods=['GET'])
def obtener_grafica_finanzas():
    empresa = request.args.get('empresa')
    periodo = request.args.get('periodo', '1y') # Por defecto, se muestra el historial de un año
    img = generar_grafico_empresa(empresa, periodo)
    return send_file(img, mimetype='image/png')
   

if __name__ == '__main__':
    app.run(port=5000, debug=True)
