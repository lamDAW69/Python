import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def entrenar_modelo_mascotas(archivo):
    # Cargar datos de entrenamiento desde el CSV
    df = pd.read_csv(f"C:\\Users\\Luis\\Documents\\Curso Python\\Python\\analisisDatos\\MascotasPrediccion\\{archivo}")

    # Codificar las características como vectores binarios
    mlb = MultiLabelBinarizer()
    X = mlb.fit_transform(df['caracteristicas'].apply(lambda x: x.split(',')))

    # Entrenar el modelo k-NN utilizando la métrica de Jaccard
    modelo = NearestNeighbors(n_neighbors=5, metric='jaccard').fit(X)

    # Retornar un diccionario con todos los componentes necesarios
    return {
        'modelo': modelo,
        'mlb': mlb,
        'df': df
    }

def sugerir_mascotas(modelo_mascotas, caracteristicas, num_mascotas=3):
    # Extraer componentes del diccionario
    modelo = modelo_mascotas['modelo']
    mlb = modelo_mascotas['mlb']
    df = modelo_mascotas['df']

    # Transformar las características de entrada en un vector binario
    caracteristicas_vector = mlb.transform([caracteristicas])

    # Encontrar las mascotas más cercanas
    distancias, indices = modelo.kneighbors(caracteristicas_vector, n_neighbors=10)

    resultado = []
    mascotas_añadidas = set()

    for idx, distancia in zip(indices[0], distancias[0]):
        mascota = df.iloc[idx]['mascota']

        # Solo añadir si la mascota no está ya en el resultado
        if mascota not in mascotas_añadidas:
            resultado.append({"mascota": mascota, "similitud": round((1 - distancia) * 100, 2)})
            mascotas_añadidas.add(mascota)

    return resultado

# Entrenar el modelo con los datos del archivo 'mascotas.csv'
modelo_mascotas = entrenar_modelo_mascotas('mascotas.csv')
@app.route('/mascotas', methods=['GET'])
def obtener_mascotas():
    caracteristicas = request.args.get('caracteristicas')
    if not caracteristicas:
        return jsonify({"error": "No se han proporcionado características"}), 400
    caracteristicas = [caracteristica.strip() for caracteristica in caracteristicas.split(',')]
    mascotas_sugeridas = sugerir_mascotas(modelo_mascotas, caracteristicas, num_mascotas=3)
    return jsonify(mascotas_sugeridas)

if __name__ == '__main__':
    app.run(port=5000)