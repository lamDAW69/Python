// Función que crea el elemento <select> para seleccionar la cantidad de Pokémons a mostrar
function crearSelect() {
  const select = document.getElementById('cantidadPokemons'); // Referencia al elemento <select> en el DOM

  // Añade opciones al <select> en incrementos de 10, desde 10 hasta 150
  for (let i = 10; i <= 150; i += 10) {
    select.innerHTML += `<option value="${i}">${i}</option>`;
  }

  // Añade un evento para detectar cambios en la selección del <select>
  select.addEventListener('change', function() {
    mostrarTodosPokemons(+this.value); // Muestra los Pokémons en función del número seleccionado
  });
}

// Función asíncrona que muestra el análisis de datos de los Pokémons seleccionados y una gráfica correspondiente
async function mostrarAnalisisDatos(cantidad = NUM_POKEMONS) {
  // Inserta la imagen de la gráfica en el HTML utilizando el número de Pokémons especificado
  let html = `<img src="${URL_PYTHON}/pokemon/grafica?num_pokemons=${cantidad}" class="img-fluid">`;

  // Realiza una solicitud al servidor para obtener el análisis de los datos de los Pokémons
  const respuesta = await fetch(`${URL_PYTHON}/pokemon?num_pokemons=${cantidad}`);
  const datos = await respuesta.json(); // Convierte la respuesta en formato JSON

  // Añade el peso y la altura promedio de los Pokémons al HTML
  html += `
    <h2>Peso y altura promedio</h2>
    <ul class="h5 mb-5">
      <li>Peso promedio: ${(datos.analisis.peso_promedio / 10).toFixed(2)} Kg.</li>
      <li>Altura promedio: ${(datos.analisis.altura_promedio / 10).toFixed(2)} m.</li>
    </ul>
  `;

  // Inserta el HTML generado en el contenedor con id "pokemons"
  document.getElementById("pokemons").innerHTML = html;
}

// Función asíncrona que muestra todos los Pokémons, sus datos y una gráfica en función de la cantidad seleccionada
async function mostrarTodosPokemons(cantidad = NUM_POKEMONS) {
  // Mostrar un spinner de carga mientras se obtienen los datos
  document.getElementById('loadingSpinner').style.display = 'block'; 

  // Muestra el análisis de datos de los Pokémons
  await mostrarAnalisisDatos(cantidad);

  // Itera sobre el número de Pokémons seleccionados y los muestra uno por uno
  for (let i = 1; i <= cantidad; i++) {
    const datos = await fetch(`https://pokeapi.co/api/v2/pokemon/${i}`); // Solicita datos de cada Pokémon desde la API
    const pokemon = await datos.json(); // Convierte la respuesta en formato JSON
    mostrarPokemon(i, pokemon); // Llama a la función para mostrar los datos del Pokémon
  }

  // Ocultar el spinner de carga una vez que los datos han sido cargados
  document.getElementById('loadingSpinner').style.display = 'none';
}

// Función que muestra los detalles de un Pokémon específico
function mostrarPokemon(i, pokemon) {
  let html = `<h2 class="text-capitalize mt-3">${i}. ${pokemon.name}</h2>`; // Muestra el nombre del Pokémon

  // Definición de colores para los diferentes tipos de Pokémon
  const colores = {
    normal: '#A8A77A',
    fire: '#EE8130',
    water: '#6390F0',
    electric: '#F7D02C',
    grass: '#7AC74C',
    ice: '#96D9D6',
    fighting: '#C22E28',
    poison: '#A33EA1',
    ground: '#E2BF65',
    flying: '#A98FF3',
    psychic: '#F95587',
    bug: '#A6B91A',
    rock: '#B6A136',
    ghost: '#735797',
    dragon: '#6F35FC',
    dark: '#705746',
    steel: '#B7B7CE',
    fairy: '#D685AD'
  };

  // Añade etiquetas con los tipos de Pokémon, coloreadas según el tipo
  html += '<h4>';
  pokemon.types.forEach(type => {
    const tipo = type.type.name;
    html += `<span class="badge me-1" style="background-color: ${colores[tipo]}">${tipo}</span>`;
  });
  html += '</h4>';

  // Añade el peso, la altura y el sonido del Pokémon al HTML
  html += `
    <p>${(pokemon.weight / 10).toFixed(2)} Kg. - ${(pokemon.height / 10).toFixed(2)} m.</p>
    <audio src="${pokemon.cries.latest}" controls></audio><br>
  `;

  // Lista de imágenes del Pokémon en diferentes poses o formas
  const imagenes = [
    'front_default',
    'front_shiny',
    'back_default',
    'back_shiny',
    'front_female',
    'front_shiny_female',
    'back_female',
    'back_shiny_female',
  ];

  // Añade las imágenes disponibles del Pokémon al HTML
  imagenes.forEach(sprite => {
    if (pokemon.sprites[sprite]) {
      html += `<img src="${pokemon.sprites[sprite]}">`;
    }
  });

  // Inserta el HTML generado en el contenedor con id "pokemons"
  document.getElementById("pokemons").innerHTML += html;
}

// Función que inicializa la aplicación cargando el select y mostrando los primeros Pokémons
function inicializar() {
  crearSelect(); // Llama a la función para crear el select de cantidad de Pokémons
  mostrarTodosPokemons(); // Muestra los primeros 10 Pokémons al cargar la página
}

// Llama a la función de inicialización cuando se carga el script
inicializar();
