import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

# Función para cargar y preparar los datos
def cargar_datos(ruta_csv):
    data = pd.read_csv(ruta_csv)
    return data

# Función para escalar los datos numéricos
def escalar_datos(X):
    escalador = StandardScaler()
    X_scaled = escalador.fit_transform(X)
    return X_scaled, escalador

# Función para entrenar el modelo de predicción de precios de casas
def entrenar_modelo(csv_path):
    # Cargar y preparar los datos
    data = cargar_datos(csv_path)
    X = data.drop('Precio', axis=1)
    y = data['Precio']
    columnas = X.columns  # Guardar los nombres de las columnas

    # Escalar los datos
    X_scaled, escalador = escalar_datos(X)

    # Entrenar el modelo
    modelo = LinearRegression().fit(X_scaled, y)

    # Retornar un diccionario con todos los componentes necesarios
    return {
        'modelo': modelo,
        'escalador': escalador,
        'columnas': columnas
    }

# Función para predecir el precio de una nueva casa
def predecir_precio(modelo_casas, tamanyo, habitaciones, banyos, garajes):
    nueva_casa = [tamanyo, habitaciones, banyos, garajes]
    columnas = modelo_casas['columnas']

    # Crear un DataFrame para la nueva casa con los nombres de las características
    nueva_casa_df = pd.DataFrame([nueva_casa], columns=columnas)

    # Escalar la nueva casa usando el escalador
    nueva_casa_escalada = modelo_casas['escalador'].transform(nueva_casa_df)

    # Predecir el precio usando el modelo entrenado
    precio_predicho = modelo_casas['modelo'].predict(nueva_casa_escalada)[0]

    return precio_predicho

# Entrenamiento del modelo con los datos del archivo CSV
modelo_casas = entrenar_modelo('csv/casas.csv')
