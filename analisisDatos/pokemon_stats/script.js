const NUM_POKEMONS = 10;
const BASE_URL = "http://127.0.0.1:5000/"; //Es necesario cambiar la URL por donde sea levantado el python

function crearSelect() {
  const select = document.getElementById('cantidadPokemons');

  for (let i = 10; i <= 150; i += 10) {
    select.innerHTML += `<option value="${i}">${i}</option>`;
  }

  select.addEventListener('change', function() {
    mostrarTodosPokemons(+this.value);
  })
}

async function mostrarAnalisisDatos(cantidad = NUM_POKEMONS) {
  let html = `<img src="${BASE_URL}/pokemon/grafica?num_pokemons=${cantidad}" class="img-fluid">`;

  const respuesta = await fetch(`${BASE_URL}/pokemon?num_pokemons=${cantidad}`);
  const datos = await respuesta.json();

  html += `<h2>Peso y Altura promedio</h2>
           <ul>
            <li>Peso promedio: ${datos.analisis.peso_promedio} hectogramos.</li>
            <li>Altura promedio: ${datos.analisis.altura_promedio} decÃ­metros.</li>
          </ul>`;

  document.getElementById("pokemons").innerHTML = html;
}

async function mostrarTodosPokemons(cantidad = NUM_POKEMONS) { 
  await mostrarAnalisisDatos(cantidad);

  for(let i=1; i<=cantidad; i++) {
    const datos = await fetch(`https://pokeapi.co/api/v2/pokemon/${i}`);
    const pokemon = await datos.json();
    mostrarPokemon(i, pokemon);
  }
}

function mostrarPokemon(i, pokemon) {
  console.log(pokemon);

  let html = `<h2 class="text-capitalize">${i}. ${pokemon.name}</h2>`;

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
  }

  html += '<h4>';
  pokemon.types.forEach(type => {
    const tipo = type.type.name;
    html += `<span class="badge me-1" style="background-color: ${colores[tipo]}">${tipo}</span>`;
  })
  html += '</h4>';

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

  imagenes.forEach(sprite => {
    if (pokemon.sprites[sprite]) {
      html += `<img src="${pokemon.sprites[sprite]}">`;
    }
  })

  /*Object.values(pokemon.sprites).forEach(url => {
    if (typeof url === 'string') {
      html += `<img src="${url}">`;
    }
  });*/

  document.getElementById("pokemons").innerHTML += html;
}

function inicializar() {
  crearSelect();
  mostrarTodosPokemons();
}

inicializar();