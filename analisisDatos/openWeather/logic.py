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

@app.route('/tiempo', methods=['GET'])
def obtener_tiempo_info(): 
    ciudad = request.args.get('ciudad')
    datos = obtener_datos_tiempo(ciudad)

    temperaturas = [x['main']['temp'] for x in datos['list']] #La informacion viene de la solicitud a la api con la info de temperatura almacenada en 'main'
    humedades = [x['main']['humidity'] for x in datos['list']] #La informacion viene de la solicitud a la api con la info de humedad almacenada en 'main'
    presiones = [x['main']['pressure'] for x in datos['list']]
    velocidad_viento = [x['wind']['speed'] for x in datos['list']]
    descripciones = [x['weather'][0]['description'] for x in datos['list']]

    df_temperaturas = pd.DataFrame(temperaturas, columns=['Temperatura'])
    df_humedades = pd.DataFrame(humedades, columns=['Humedad'])
    df_presiones = pd.DataFrame(presiones, columns=['Presion'])
    df_velocidad_viento = pd.DataFrame(velocidad_viento, columns=['Velocidad del Viento'])

    #Aqui se calculan las estadisticas con un diccionario
    estadistica = {
        "media_temperatura": df_temperaturas['Temperatura'].mean(),
        "maxima_temperatura": df_temperaturas['Temperatura'].max(),
        "minima_temperatura": df_temperaturas['Temperatura'].min(),
        "media_humedad": df_humedades['Humedad'].mean(),
        "media_presion": df_presiones['Presion'].mean(),
        "media_viento": df_velocidad_viento['Velocidad del Viento'].mean(),
        "descripciones": descripciones
    }
    return jsonify(estadistica)
if __name__ == "__main__":
    app.run(port=5000)
