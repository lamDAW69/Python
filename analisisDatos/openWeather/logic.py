import datetime
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import requests
from io import BytesIO
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

API_KEY = "1fe9ecd1d45d76ff5ae46294e85557e3"
URL_BASE = f"https://api.openweathermap.org/data/2.5/forecast?lang=es&units=metric&appid={API_KEY}"


app = Flask(__name__)
CORS(app)

def obtener_datos_tiempo(ciudad):
    url = f"{URL_BASE}&q={ciudad}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

@app.route('/tiempo/grafica', methods=['GET'])
def obtener_grafica_tiempo():
    ciudad = request.args.get('ciudad')
    datos = obtener_datos_tiempo(ciudad)
    fechas = []
    temperaturas = []
    for item in datos['list']:
        fecha_obj = datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S') #Esto hace que la fecha sea un objeto de tipo datetime
        fecha_formateada = fecha_obj.strftime('%d %b %H:%M')                #y esto la formatea a un string con el formato que queremos
        fechas.append(fecha_formateada)
        temperaturas.append(item['main']['temp'])
    plt.figure(figsize=(10, 6.5))
    plt.plot(fechas, temperaturas, marker='o', linestyle='-', color='r')
    plt.title(f'Temperaturas para {ciudad}', fontsize=16)
    plt.xlabel("Fecha y Hora", fontsize=14)
    plt.ylabel("Temperaturas (°C)", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return send_file(img, mimetype="image/png")

if __name__ == "__main__":
    app.run(port=5000)
