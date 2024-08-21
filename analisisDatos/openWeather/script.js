const API_KEY = '1fe9ecd1d45d76ff5ae46294e85557e3';
const URL_OPEN_WEATHER = `https://api.openweathermap.org/data/2.5/weather?lang=es&units=metric&appid=${API_KEY}`;
const PYTHON_URL = 'http://localhost:5000';

async function obtener_tiempo(ciudad) {
    let datos = await fetch(`${URL_OPEN_WEATHER}&q=${ciudad}`);
    datos = await datos.json();
    console.log(datos);
    document.getElementById('tiempo').innerHTML = `
    <img src="https://openweathermap.org/img/wn/${datos.weather[0].icon}@4x.png">
    <p class="text-uppercase">${datos.weather[0].description}</p>
    <p>Temperatura Actual: ${datos.main.temp}°C</p>
    <p>Temperatura Máxima: ${datos.main.temp_max}°C</p>
    <p>Temperatura Mínima: ${datos.main.temp_min}°C</p>
    <p>Humedad: ${datos.main.humidity}%</p>
    <p>Presión: ${datos.main.pressure} hPa</p>
    <p>Viento: ${datos.wind.speed} m/s</p>
  `;
}


function obtener_grafica(ciudad) {
    document.getElementById("tiempo").innerHTML += 
    `<img src="${PYTHON_URL}/tiempo/grafica?ciudad=${ciudad}" class="img-fluid">`;
}
/*
async function obtener_estadisticas(ciudad) {
    let datos = await fetch (`${PYTHON_URL}/estadisticas?=ciudad=${ciudad}`);
    datos = await datos.json();

    document.getElementById("tiempo").innerHTML = `
    <p>Media Temperatura: ${datos.media_temperatura}°C</p>
    <p>Media Temperatura Máxima: ${datos.media_temperatura_max}°C</p>
    <p>Media Temperatura Mínimi: ${datos.media_temperatura_min}°C</p>
    <p>Media Humedad: ${datos.media_humedad}%</p>
    <p>Media Velocidad del viento: ${datos.media_viento} m/s</p>
º   <p>Media Presión: ${datos.media_presion} hPa</p>
`;
}
*/





function inicializar() {
    const formulario = document.getElementById("formulario");
    const ciudad = document.getElementById("ciudad");

    formulario.addEventListener('submit', async function(event) {
        event.preventDefault();
        await obtener_tiempo(ciudad.value);
        obtener_grafica(ciudad.value);
        //obtener_estadisticas(ciudad.value);
    });
    obtener_tiempo(ciudad.value);
}
inicializar();