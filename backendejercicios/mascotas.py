import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MultiLabelBinarizer
import unicodedata

def entrenar_modelo_mascotas(csv_path):
    # Cargar datos de entrenamiento desde el CSV
    df = pd.read_csv(csv_path)

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

def obtener_caracteristicas(modelo_mascotas):
    df = modelo_mascotas['df']
    # Extraer todas las características
    caracteristicas = df['caracteristicas'].apply(lambda x: x.split(',')).explode().unique()
    # Normalizar y ordenar alfabéticamente
    caracteristicas_ordenadas = sorted(caracteristicas, key=lambda x: unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode('ascii'))
    return caracteristicas_ordenadas

def sugerir_mascotas(modelo_mascotas, caracteristicas, num_mascotas=5):
    # Extraer componentes del diccionario
    modelo = modelo_mascotas['modelo']
    mlb = modelo_mascotas['mlb']
    df = modelo_mascotas['df']

    # Transformar las características de entrada en un vector binario
    caracteristicas = mlb.transform([caracteristicas])

    # Encontrar las mascotas más cercanas
    distancias, indices = modelo.kneighbors(caracteristicas, n_neighbors=num_mascotas)

    resultado = []
    for idx, distancia in zip(indices[0], distancias[0]):
        mascota = df.iloc[idx]['mascota']
        similitud = round((1 - distancia) * 100, 2)
        if similitud > 0: resultado.append({"mascota": mascota, "similitud": similitud})

    return resultado

# Entrenar el modelo con los datos del archivo 'mascotas.csv'
modelo_mascotas = entrenar_modelo_mascotas('csv/mascotas.csv')
