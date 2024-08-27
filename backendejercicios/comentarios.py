import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize

# Descargar recursos necesarios para NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Inicializar el SnowballStemmer para español
stemmer = SnowballStemmer('spanish')

# Preprocesamiento del texto con stemmer
def preprocesar_texto(texto):
    texto = re.sub(r'\W', ' ', texto)  # Eliminar caracteres especiales
    texto = texto.lower()  # Convertir a minúsculas
    tokens = word_tokenize(texto)  # Tokenización
    # Paso 1: Eliminar stopwords
    tokens_filtrados = [token for token in tokens if token not in stopwords.words('spanish')]
    # Paso 2: Aplicar stemming, pero mantener las negaciones sin cambios
    tokens_procesados = [stemmer.stem(token) if token not in ["no", "ni"] else token for token in tokens_filtrados]

    return ' '.join(tokens)

# Entrenamiento del modelo usando SVM
def entrenar_modelo(ruta_csv):
    # Cargar los datos de entrenamiento
    data = pd.read_csv(ruta_csv)  # Este archivo debe contener los comentarios y una columna 'negativa' con 1 para negativa y 0 para positiva

    # Crear el pipeline con TfidfVectorizer y SVC
    modelo = make_pipeline(TfidfVectorizer(preprocessor=preprocesar_texto, ngram_range=(1, 2)), SVC(probability=True))

    # Entrenar el modelo con todos los datos
    modelo.fit(data['comentario'], data['negativo'])

    return modelo

# Predecir la probabilidad de que un comentario sea negativo
def probabilidad_negativo(modelo, texto):
    texto = preprocesar_texto(texto)  # Preprocesar el texto antes de predecir
    probabilidad = modelo.predict_proba([texto])[0][1] * 100  # Obtener la probabilidad de que sea negativo
    return probabilidad

# Crear una instancia del modelo entrenado utilizando todos los datos
modelo_comentarios = entrenar_modelo('csv/comentarios.csv')

