const PYTHON_URL= 'http://localhost:5000/grafica';

const drivers = [
    'Albon',
    'Alonso',
    'Bottas',
    'Gasly',
    'Giovinazzi',
    'Hamilton',
    'Hulkenberg',
    'Latifi',
    'Leclerc',
    'Magnussen',
    'Mazepin',
    'Norris',
    'Ocon',
    'Pérez',
    'Piastri',
    'Raikkonen',
    'Ricciardo',
    'Russell',
    'Schumacher',
    'Sainz',
    'Stroll',
    'Tsunoda',
    'max_verstappen',
    'Zhou'
];

const seasons = [
    '2023', 
    '2022',
    '2021',
];


function createSelectSeason() {
    const select = document.getElementById('season');
    select.innerHTML = '';

    seasons.forEach(season => {
        const option = document.createElement('option');
        option.value = season;
        option.textContent = season;
        select.appendChild(option);
    });
}

function createSelectDriver() {
    const select = document.getElementById('driver');
    select.innerHTML = ''; // Limpiar opciones anteriores

    drivers.forEach(driver => {
        const option = document.createElement('option');
        option.value = driver;
        option.textContent = driver;
        select.appendChild(option);
    });
}

function getGraph(driver, season) {
    const graph = document.getElementById('graph');
    graph.src = `${PYTHON_URL}?year=${season}&driver=${driver}`;
    // Mostrar la imagen con una transición suave
    graph.onload = function() {
        graph.classList.add('show');
    };
    // Si hay un error cargando la imagen, ocultar la imagen
    graph.onerror = function() {
        graph.classList.remove('show');
        alert('Error al cargar estadisticas, el piloto seleccionado no tiene datos para la temporada seleccionada');
    };
}

 document.addEventListener('DOMContentLoaded', function() {
    createSelectSeason();
    createSelectDriver();

    const form = document.getElementById('form');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const driver = document.getElementById('driver').value;
        const season = document.getElementById('season').value;
        getGraph(driver, season);
    });
}
);



