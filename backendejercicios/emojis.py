import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
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

# Función para limpiar y preprocesar el texto con stemming y eliminación completa de stopwords
def preprocesar_texto(texto):
    # Eliminar caracteres especiales y convertir a minúsculas
    texto = re.sub(r'\W', ' ', texto)
    texto = texto.lower()
    # Tokenizar y aplicar stemming
    tokens = word_tokenize(texto)
    # Eliminar todas las stopwords
    tokens = [stemmer.stem(token) for token in tokens if token not in stopwords.words('spanish')]
    return ' '.join(tokens)  # Formamos una cadena con las palabras separadas por espacios

# Función para entrenar el modelo de emojis utilizando Naive Bayes
def entrenar_modelo(csv_path):
    # Cargar datos de entrenamiento desde el CSV
    df = pd.read_csv(csv_path)

    # Filtrar las filas con emojis duplicados
    df = df.drop_duplicates(subset='emojis')

    # Preprocesar las palabras clave en el conjunto de datos
    df['palabras'] = df['palabras'].apply(preprocesar_texto)

    # Vectorizar las palabras clave usando TF-IDF
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['palabras'])

    # Entrenar el modelo Naive Bayes
    modelo = MultinomialNB().fit(X, df['emojis'])

    # Retornar un diccionario con todos los componentes necesarios
    return {
        'modelo': modelo,
        'vectorizer': vectorizer
    }

# Función para sugerir emojis basados en palabras clave
def traducir_a_emojis(modelo_emojis, texto, num_emojis=5):
    # Preprocesar el texto completo para extraer palabras clave
    texto = preprocesar_texto(texto)

    # Extraer componentes del diccionario
    modelo = modelo_emojis['modelo']
    vectorizer = modelo_emojis['vectorizer']

    # Transformar las palabras clave de entrada en un vector TF-IDF
    X_test = vectorizer.transform([texto])

    # Predecir la probabilidad de cada emoji
    probabilidades = modelo.predict_proba(X_test)[0]

    # Ordenar los emojis por probabilidad descendente
    indices_ordenados = probabilidades.argsort()[::-1][:num_emojis]

    # Construir el array de resultados
    resultado = []
    for idx in indices_ordenados:
        emoji = modelo.classes_[idx]
        similitud = round(probabilidades[idx] * 100, 2)
        resultado.append({"emojis": emoji, "similitud": similitud})

    return resultado

# Entrenamiento del modelo con los datos del archivo csv
modelo_emojis = entrenar_modelo('csv/emojis.csv')
