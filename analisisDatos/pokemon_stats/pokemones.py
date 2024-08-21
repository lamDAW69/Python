from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import requests
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

def obtener_datos_pokemon(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def cargar_datos_pokemons(num_pokemons):
    pokemon_data = []
    for i in range(1, num_pokemons + 1):
        data = obtener_datos_pokemon(i)
        if data:
            pokemon_info = {
                "Nombre": data["name"],
                "Altura": data["height"],
                "Peso": data["weight"],
                "Tipos": [t["type"]["name"] for t in data["types"]]
            }
            pokemon_data.append(pokemon_info)
    return pd.DataFrame(pokemon_data)

def analizar_datos(df):
    peso_promedio = (df["Peso"]).mean()
    altura_promedio = df["Altura"].mean()
    todos_los_tipos = df["Tipos"].explode()
    distribucion_tipos = todos_los_tipos.value_counts()
    distribucion_tipos_lista = list(distribucion_tipos.items())
    analisis = {
        "peso_promedio": peso_promedio,
        "altura_promedio": altura_promedio,
        "distribucion_tipos": distribucion_tipos_lista
    }
    return analisis, distribucion_tipos

def generar_grafico_distribucion_tipos(distribucion_tipos):
    plt.figure(figsize=(10, 6))
    ax = distribucion_tipos.plot(kind="bar", color="red")
    plt.title("Distribución de tipos de pokemones")
    plt.xlabel("Tipo")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)

    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    plt.close()

    return img
@app.route('/pokemon/grafica', methods=["GET"])
def obtener_grafico():
    df = cargar_datos_pokemons(25)
    analisis, distribucion_tipos = analizar_datos(df)
    img = generar_grafico_distribucion_tipos(distribucion_tipos)

    return send_file(img, mimetype="image/png")

if __name__ == "__main__": 
    app.run(port=5000)