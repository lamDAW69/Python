import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
import unicodedata

def entrenar_modelo_recetas(csv_path):
    # Cargar datos de entrenamiento desde el CSV
    df = pd.read_csv(csv_path)

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
        'X': X  # Incluimos X para poder obtener las recetas correspondientes
    }
    
def obtener_ingredientes(modelo_recetas):
    df = modelo_recetas['df']
    # Extraer todos los ingredientes
    ingredientes = df['ingredientes'].apply(lambda x: x.split(',')).explode().unique()
    # Ordenarlos alfabéticamente
    ingredientes_ordenados = sorted(ingredientes, key=lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('ascii'))
    return ingredientes_ordenados

def sugerir_recetas(modelo_recetas, ingredientes, num_recetas=5):
    # Extraer componentes del diccionario
    modelo = modelo_recetas['modelo']
    mlb = modelo_recetas['mlb']
    df = modelo_recetas['df']

    # Transformar los ingredientes de entrada en un vector binario
    ingredientes_vector = mlb.transform([ingredientes])

    # Encontrar las recetas más cercanas
    distancias, indices = modelo.kneighbors(ingredientes_vector, n_neighbors=num_recetas)

    resultado = []
    for idx, distancia in zip(indices[0], distancias[0]):
        receta = df.iloc[idx]['receta']
        similitud = round((1 - distancia) * 100, 2)
        if similitud > 0: resultado.append({"receta": receta, "similitud": similitud})

    return resultado

# Entrenar el modelo con los datos del archivo 'recetas.csv'
modelo_recetas = entrenar_modelo_recetas('csv/recetas.csv')
