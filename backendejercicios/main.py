from flask import Flask, jsonify, request, send_file  # Importa las clases y funciones necesarias de Flask
from flask_cors import CORS  # Importa CORS para permitir solicitudes desde otros dominios
import pandas as pd  # Importa pandas para el manejo de datos

# Importa funciones y modelos de los módulos correspondientes
from pokemons import cargar_datos_pokemons, analizar_datos, generar_grafico_distribucion_tipos, NUM_POKEMONS
from tiempo import obtener_datos_tiempo, generar_grafico_tiempo
from finanzas import generar_grafico_empresas
from spam import probabilidad_spam, modelo_spam
from comentarios import probabilidad_negativo, modelo_comentarios
from recetas import sugerir_recetas, modelo_recetas, obtener_ingredientes
from mascotas import sugerir_mascotas, modelo_mascotas, obtener_caracteristicas
from emojis import modelo_emojis, traducir_a_emojis
from traductor import traducir_a_ingles
from casas import modelo_casas, predecir_precio
from crowdfunding import modelo_crowdfunding, predecir_probabilidad_exito
from pruebas import pruebas_bp  # Importa el blueprint desde pruebas.py

# Inicializa la aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para la aplicación

# Registra el blueprint de pruebas
app.register_blueprint(pruebas_bp)

# Ruta para obtener información de Pokémons
@app.route('/pokemon', methods=['GET'])
def obtener_pokemon_info():
    # Obtiene el número de pokemons a analizar desde los parámetros de la solicitud
    num_pokemons = int(request.args.get('num_pokemons', NUM_POKEMONS))
    df = cargar_datos_pokemons(num_pokemons)  # Carga los datos de Pokémon
    analisis, distribucion_tipos = analizar_datos(df)  # Realiza el análisis de los datos

    return jsonify({"analisis": analisis})  # Retorna el análisis como JSON

# Ruta para obtener un gráfico de la distribución de tipos de Pokémon
@app.route('/pokemon/grafica', methods=['GET'])
def obtener_grafica_tipos():
    num_pokemons = int(request.args.get('num_pokemons', NUM_POKEMONS))
    df = cargar_datos_pokemons(num_pokemons)
    analisis, distribucion_tipos = analizar_datos(df)
    img = generar_grafico_distribucion_tipos(distribucion_tipos)  # Genera el gráfico

    return send_file(img, mimetype='image/png')  # Envía la imagen como respuesta

# Ruta para obtener información del tiempo en una ciudad específica
@app.route('/tiempo', methods=['GET'])
def obtener_tiempo_info():
    ciudad = request.args.get('ciudad')
    if not ciudad:
        return jsonify({"error": "No se ha especificado ninguna ciudad"}), 400 

    datos = obtener_datos_tiempo(ciudad)

    # Extrae las métricas relevantes de los datos
    temperaturas = [item['main']['temp'] for item in datos['list']]
    humedades = [item['main']['humidity'] for item in datos['list']]
    presiones = [item['main']['pressure'] for item in datos['list']]
    velocidades_viento = [item['wind']['speed'] for item in datos['list']]
    descripciones = [item['weather'][0]['description'] for item in datos['list']]

    # Crea DataFrames para calcular estadísticas
    df_temperatura = pd.DataFrame(temperaturas, columns=['Temperatura'])
    df_humedad = pd.DataFrame(humedades, columns=['Humedad'])
    df_presion = pd.DataFrame(presiones, columns=['Presión'])
    df_viento = pd.DataFrame(velocidades_viento, columns=['Viento'])

    # Calcula las estadísticas y las organiza en un diccionario
    estadisticas = {
        "media_temperatura": df_temperatura['Temperatura'].mean(),
        "max_temperatura": df_temperatura['Temperatura'].max(),
        "min_temperatura": df_temperatura['Temperatura'].min(),
        "media_humedad": df_humedad['Humedad'].mean(),
        "media_presion": df_presion['Presión'].mean(),
        "media_viento": df_viento['Viento'].mean(),
        "descripciones": descripciones
    }

    return jsonify(estadisticas)  # Retorna las estadísticas como JSON

# Ruta para obtener un gráfico del tiempo en una ciudad específica
@app.route('/tiempo/grafica', methods=['GET'])
def obtener_grafica_tiempo():
    ciudad = request.args.get('ciudad')
    if not ciudad:
        return jsonify({"error": "No se ha especificado ninguna ciudad"}), 400

    datos = obtener_datos_tiempo(ciudad)
    if datos:
        img = generar_grafico_tiempo(datos, ciudad)  # Genera el gráfico del tiempo
        return send_file(img, mimetype='image/png')  # Envía la imagen como respuesta
    else:
        return jsonify({"error": "Datos de tiempo no disponibles"}), 404  # Error si no hay datos disponibles

# Ruta para obtener un gráfico financiero de una empresa específica
@app.route('/finanzas/grafica', methods=['GET'])
def obtener_grafica_finanzas():
    empresa = request.args.get('empresa')
    if not empresa:
        return jsonify({"error": "No se ha especificado ninguna empresa"}), 400

    periodo = request.args.get('periodo', '1y')  # Período por defecto de 1 año

    img = generar_grafico_empresas(empresa, periodo)  # Genera el gráfico financiero
    return send_file(img, mimetype='image/png')  # Envía la imagen como respuesta

# Ruta para obtener sugerencias de recetas basadas en ingredientes
@app.route('/recetas', methods=['GET'])
def obtener_recetas():
    ingredientes = request.args.get('ingredientes')
    if not ingredientes:
        return jsonify({"error": "No se han proporcionado ingredientes"}), 400

    # Limpia y separa los ingredientes proporcionados
    ingredientes = [ingrediente.strip() for ingrediente in ingredientes.split(',')]
    recetas = sugerir_recetas(modelo_recetas, ingredientes)  # Sugiere recetas basadas en los ingredientes
    return jsonify(recetas)  # Retorna las recetas sugeridas como JSON

# Ruta para obtener una lista de ingredientes disponibles para recetas
@app.route('/recetas/ingredientes', methods=['GET'])
def obtener_ingredientes_recetas():
    ingredientes = obtener_ingredientes(modelo_recetas)  # Obtiene la lista de ingredientes
    return jsonify(ingredientes)  # Retorna la lista de ingredientes como JSON

# Ruta para obtener sugerencias de mascotas basadas en características
@app.route('/mascotas', methods=['GET'])
def obtener_mascotas():
    caracteristicas = request.args.get('caracteristicas')
    if not caracteristicas:
        return jsonify({"error": "No se han proporcionado caracteristicas"}), 400

    # Limpia y separa las características proporcionadas
    caracteristicas = [caracteristica.strip() for caracteristica in caracteristicas.split(',')]
    recetas = sugerir_mascotas(modelo_mascotas, caracteristicas)  # Sugiere mascotas basadas en las características
    return jsonify(recetas)  # Retorna las mascotas sugeridas como JSON

# Ruta para obtener una lista de características disponibles para mascotas
@app.route('/mascotas/caracteristicas', methods=['GET'])
def obtener_caracteristicas_mascotas():
    caracteristicas = obtener_caracteristicas(modelo_mascotas)  # Obtiene la lista de características
    return jsonify(caracteristicas)  # Retorna la lista de características como JSON

# Ruta para comprobar la probabilidad de que un texto sea spam
@app.route('/spam', methods=['GET'])
def comprobar_spam():
    texto = request.args.get('texto')
    if not texto:
        return jsonify({"error": "No se han proporcionado ningún texto"}), 400

    probabilidad = probabilidad_spam(modelo_spam, texto)  # Calcula la probabilidad de spam
    return jsonify({"probabilidad_spam": probabilidad})  # Retorna la probabilidad como JSON

# Ruta para comprobar la probabilidad de que un comentario sea negativo
@app.route('/comentarios', methods=['GET'])
def comprobar_comentario():
    comentario = request.args.get('comentario')
    if not comentario:
        return jsonify({"error": "No se han proporcionado ningún comentario"}), 400

    probabilidad = probabilidad_negativo(modelo_comentarios, comentario)  # Calcula la probabilidad de negatividad
    return jsonify({"probabilidad_negativo": probabilidad})  # Retorna la probabilidad como JSON

# Ruta para traducir un texto a emojis
@app.route('/emojis', methods=['GET'])
def traducir_texto_a_emojis():
    texto = request.args.get('texto')
    if not texto:
        return jsonify({"error": "No se ha proporcionado ningún texto"}), 400

    emojis = traducir_a_emojis(modelo_emojis, texto)  # Traduce el texto a emojis
    return jsonify(emojis)  # Retorna la traducción como JSON

# Ruta para traducir un texto al inglés
@app.route('/traductor', methods=['GET'])
def traducir_texto_a_ingles():
    texto = request.args.get('texto')
    if not texto:
        return jsonify({"error": "No se ha proporcionado ningún texto"}), 400

    traduccion = traducir_a_ingles(texto)  # Traduce el texto al inglés
    return jsonify(traduccion)  # Retorna la traducción como JSON

# Ruta para predecir el precio de una casa basada en sus características
@app.route('/casas', methods=['GET'])
def obtener_precio_casa():
    try:
        # Obtiene los parámetros de la solicitud y los convierte al tipo adecuado
        tamanyo = float(request.args.get('tamanyo'))
        habitaciones = int(request.args.get('habitaciones'))
        banyos = int(request.args.get('banyos'))
        garajes = int(request.args.get('garajes'))
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetros incorrectos."}), 400 

    precio = predecir_precio(modelo_casas, tamanyo, habitaciones, banyos, garajes)  # Predice el precio de la casa
    return jsonify({"precio": precio})  # Retorna el precio como JSON

# Ruta para predecir la viabilidad de un nuevo proyecto
@app.route('/crowdfunding/prediccion', methods=['GET'])
def obtener_probabilidad_exito():
    try:
        # Obtiene los parámetros de la solicitud y los convierte al tipo adecuado
        categoria = request.args.get('categoria')
        meta_financiera = float(request.args.get('meta_financiera'))
        dinero_recaudado = float(request.args.get('dinero_recaudado'))
        duracion = int(request.args.get('duracion'))
        numero_patrocinadores = int(request.args.get('numero_patrocinadores'))
    except (TypeError, ValueError):
        return jsonify({"error": "Parámetros incorrectos."}), 400

    # Predice la probabilidad de éxito del proyecto
    probabilidad_exito = predecir_probabilidad_exito(
        modelo_crowdfunding,
        categoria,
        meta_financiera,
        dinero_recaudado,
        duracion,
        numero_patrocinadores
    )

    return jsonify({
        "probabilidad_exito": f"{probabilidad_exito:.2f}%"  # Formatear la probabilidad como un porcentaje
    })

# Ruta para obtener todas las categorías disponibles para predecir crowdfunding
@app.route('/crowdfunding/categorias', methods=['GET'])
def obtener_categorias_endpoint():
    categorias = modelo_crowdfunding['categorias']
    return jsonify({"categorias": categorias})

# Inicia la aplicación Flask en el puerto 5000
if __name__ == "__main__":
    app.run(port=5000)
