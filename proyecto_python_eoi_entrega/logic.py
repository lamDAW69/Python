from flask import Flask, send_file, request
from io import BytesIO
import requests
import matplotlib.pyplot as plt
import matplotlib 
matplotlib.use('Agg')
import flask_cors as CORS


url_api = 'https://ergast.com/api/f1'

app = Flask(__name__)
CORS.CORS(app)

def get_driver_data(year, driver):
    url = f"{url_api}/{year}/drivers/{driver}/results.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

@app.route('/grafica', methods=['GET'])
def get_driver_graph():

    year = request.args.get('year')
    driver = request.args.get('driver')
    data = get_driver_data(year, driver)
    race_date = []
    circuit = []
    points = []
    position = []

    if data is not None:
        for x in data['MRData']['RaceTable']['Races']: 
            circuit.append(x['Circuit']['circuitName'])
            race_date.append(x['date'])
            points.append(float(x['Results'][0]['points']))  # Convertir a flotante
            position.append(x['Results'][0]['position'])

        # Aplicar estilo de Matplotlib
        #plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle')
        plt.style.use('dark_background')
        plt.figure(figsize=(12, 7))
        plt.plot(circuit, points, marker='o', linestyle='-', color='#FFFFFF', linewidth=2, markersize=8)
        
        # Añadir etiquetas y título con fuente personalizada
        plt.title(f'Puntos obtenidos por {driver} en {year}', fontsize=18, fontweight='bold', color='#FFFFFF')
        plt.xlabel("Circuito", fontsize=14, fontweight='bold', color='#FFFFFF')
        plt.ylabel("Puntos", fontsize=14, fontweight='bold', color='#FFFFFF')

        # Rotar las etiquetas del eje X
        plt.xticks(rotation=45, ha='right', fontsize=12, color='#FFFFFF')
        plt.yticks(fontsize=12, color='#FFFFFF')

    # Ajustar los límites del eje Y
        plt.ylim(0, max(points) + 1)

        # Personalizar la cuadrícula
        plt.grid(True, linestyle='--', linewidth=0.6, color='#e8947f')
        #plt.gca().invert_yaxis()   Invertir el eje Y// esto es lo que causaba que se invirtiera el eje Y en la gráfica se viera raro
        plt.tight_layout()


        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close()
        return send_file(img, mimetype="image/png")
    else: 
        return "No se encontraron datos para el año y piloto seleccionados"

# Example URL: http://localhost:5000/grafica?year=2021&driver=hamilton

if __name__ == "__main__":
    app.run(port=5000)
