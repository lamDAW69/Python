import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
from flask import Flask, jsonify, request
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

def entrenar_modelo_recetas(archivo):
    # Cargar datos de entrenamiento desde el CSV
    df = pd.read_csv(f"C:\\Users\\Luis\\Documents\\Curso Python\\Python\\analisisDatos\\PrediccionRecetas\\{archivo}")

    # Codificar los ingredientes como vectores binarios
    mlb = MultiLabelBinarizer()
    X = mlb.fit_transform(df['ingredientes'].apply(lambda x: x.split(',')))

    # Entrenar el modelo k-NN
    modelo = NearestNeighbors(n_neighbors=5, metric='jaccard').fit(X)

    # Retornar un diccionario con todos los componentes necesarios
    return {
        'modelo': modelo,
        'mlb': mlb,
        'df': df,
        'X': X # Incluimos X para poder obtener las recetas correspondientes
    }


def sugerir_recetas(modelo_recetas, ingredientes, num_recetas=3):
    # Extraer componentes del diccionario
    modelo = modelo_recetas['modelo']
    mlb = modelo_recetas['mlb']
    df = modelo_recetas['df']
    #X = modelo_recetas['X']

    # Transformar los ingredientes de entrada en un vector binario
    ingredientes_vector = mlb.transform([ingredientes])

    # Encontrar las recetas más cercanas
    distancias, indices = modelo.kneighbors(ingredientes_vector, n_neighbors=num_recetas)

    resultado = []
    for idx, distancia in zip(indices[0], distancias[0]):
        receta = df.iloc[idx]['receta']
        resultado.append({"receta": receta, "similitud": round((1 - distancia) * 100, 2)})

    return resultado

modelo_recetas = entrenar_modelo_recetas('recetas.csv')

@app.route('/recetas', methods=['GET'])
def obtener_receta():
    # Obtener los ingredientes desde la URL como un string separado por comas
    ingredientes = request.args.get('ingredientes')
    if not ingredientes:
        return jsonify({"error": "No se proporcionaron ingredientes"}), 400

    # Convertir el string de ingredientes en una lista
    ingredientes = [ingrediente.strip() for ingrediente in ingredientes.split(',')]
    recetas = sugerir_recetas(modelo_recetas, ingredientes, num_recetas=3)
    return jsonify({"recetas": recetas}) # Devolver un JSON con las recetas sugeridas de la forma {"recetas": [{"receta": "...", "similitud": 0.0}, ...]}

if __name__ == '__main__':
    app.run(port=5000)