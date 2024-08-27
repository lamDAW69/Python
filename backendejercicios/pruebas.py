from flask import Blueprint

pruebas_bp = Blueprint('pruebas', __name__)

@pruebas_bp.route('/', methods=['GET'])
def index():
    html_content = """
    <html>
    <head><title>Enlaces de prueba backend ejercicios</title></head>
    <body>
        <h1>Enlaces de prueba backend ejercicios</h1>
        <ul>
            <li><a href="/pokemon?num_pokemons=10">Obtener información de Pokémons (num_pokemons=10)</a></li>
            <li><a href="/pokemon/grafica?num_pokemons=10">Obtener gráfica de tipos de Pokémon (num_pokemons=10)</a></li>
            <li><a href="/tiempo?ciudad=London">Obtener información del tiempo en una ciudad (ciudad=London)</a></li>
            <li><a href="/tiempo/grafica?ciudad=London">Obtener gráfica del tiempo en una ciudad (ciudad=London)</a></li>
            <li><a href="/finanzas/grafica?empresa=GOOGL&periodo=1y">Obtener gráfica financiera de una empresa (empresa=GOOGL, periodo=1y)</a></li>
            <li><a href="/recetas?ingredientes=tomate,queso">Obtener sugerencias de recetas (ingredientes=tomate,queso)</a></li>
            <li><a href="/recetas/ingredientes">Obtener lista de ingredientes para recetas</a></li>
            <li><a href="/mascotas?caracteristicas=pequeño,amigable">Obtener sugerencias de mascotas (caracteristicas=pequeño,amigable)</a></li>
            <li><a href="/mascotas/caracteristicas">Obtener lista de características para mascotas</a></li>
            <li><a href="/spam?texto=Este es un mensaje de prueba">Comprobar probabilidad de spam (texto=Este es un mensaje de prueba)</a></li>
            <li><a href="/comentarios?comentario=Este producto es terrible">Comprobar probabilidad de comentario negativo (comentario=Este producto es terrible)</a></li>
            <li><a href="/emojis?texto=Hola mundo">Traducir texto a emojis (texto=Hola mundo)</a></li>
            <li><a href="/traductor?texto=Hola mundo">Traducir texto a inglés (texto=Hola mundo)</a></li>
            <li><a href="/casas?tamanyo=120.5&habitaciones=3&banyos=2&garajes=1">Predecir precio de casa (tamanyo=120.5, habitaciones=3, banyos=2, garajes=1)</a></li>
            <li><a href="/crowdfunding/prediccion?categoria=tecnología&meta_financiera=10000&dinero_recaudado=5000&duracion=30&numero_patrocinadores=100">Predecir éxito de crowdfunding (categoría=tecnología, meta_financiera=10000, dinero_recaudado=5000, duracion=30, numero_patrocinadores=100)</a></li>
            <li><a href="/crowdfunding/categorias">Obtener todas las categorías para crowdfunding</a></li>
        </ul>
    </body>
    </html>
    """
    return html_content
