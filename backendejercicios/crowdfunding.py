import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Función para cargar y preparar los datos
def cargar_datos_crowdfunding(ruta_csv):
    df = pd.read_csv(ruta_csv)
    return df

# Función para preparar los datos
def preparar_datos(df, columnas_categoricas):
    df = df.drop(columns=['Nombre del Proyecto'])  # Eliminar columnas no relevantes
    df = pd.get_dummies(df, columns=columnas_categoricas)  # Convertir categorías a variables dummy
    X = df.drop('Éxito', axis=1)  # Características
    y = df['Éxito']  # Variable objetivo
    return X, y

# Función para entrenar el modelo de viabilidad de crowdfunding
def entrenar_modelo_crowdfunding(csv_path):
    # Cargar y preparar los datos
    df = cargar_datos_crowdfunding(csv_path)
    columnas_categoricas = ['Categoría']
    X, y = preparar_datos(df, columnas_categoricas)

    # Obtener categorías únicas
    categorias = df['Categoría'].unique().tolist()

    # Entrenar el modelo
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X, y)

    # Retornar un diccionario con todos los componentes necesarios
    return {
        'modelo': modelo,
        'columnas_modelo': X.columns,
        'columnas_categoricas': columnas_categoricas,
        'categorias': categorias
    }

# Función para predecir la probabilidad de éxito de un nuevo proyecto
def predecir_probabilidad_exito(modelo_crowdfunding, categoria, meta_financiera, dinero_recaudado, duracion, numero_patrocinadores):
    nuevo_proyecto = {
        'Categoría': categoria,
        'Meta Financiera': meta_financiera,
        'Dinero Recaudado': dinero_recaudado,
        'Duración (días)': duracion,
        'Número de Patrocinadores': numero_patrocinadores
    }

    # Crear un DataFrame para el nuevo proyecto
    X_nuevo = pd.DataFrame([nuevo_proyecto])

    # Convertir la columna categórica a variables dummy
    X_nuevo = pd.get_dummies(X_nuevo, columns=modelo_crowdfunding['columnas_categoricas'])

    # Asegurarse de que X_nuevo tenga todas las columnas necesarias
    X_nuevo = X_nuevo.reindex(columns=modelo_crowdfunding['columnas_modelo'], fill_value=0)

    # Predecir la probabilidad de éxito
    probabilidad_exito = modelo_crowdfunding['modelo'].predict_proba(X_nuevo)[0][1]  # [1] es la clase de éxito

    return probabilidad_exito * 100  # Convertir a porcentaje

# Entrenamiento del modelo con los datos del archivo CSV
modelo_crowdfunding = entrenar_modelo_crowdfunding('csv/crowdfunding.csv')