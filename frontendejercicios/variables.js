// Constante que almacena la URL del servidor Python al que se realizarán las solicitudes
const URL_PYTHON = 'https://bba8915c-d3f7-4799-9944-d908c79b4d0a-00-35qmi0wr5qc5u.kirk.replit.dev:5000'; 

// Constante que almacena la clave de la API de OpenWeather para realizar solicitudes de datos meteorológicos
const API_KEY_OPEN_WEATHER = '36716e91288f48d1fb0d996c17c7ce73';

// URL base para la API de OpenWeather, incluyendo parámetros de idioma, unidades de medida y la clave API
const URL_OPEN_WEATHER = `https://api.openweathermap.org/data/2.5/weather?lang=es&units=metric&appid=${API_KEY_OPEN_WEATHER}`;

// Constante que define el número inicial de Pokémons a mostrar
const NUM_POKEMONS = 10;

// Variable para almacenar el temporizador que controlará el tiempo de espera entre peticiones
let timeout = null; 