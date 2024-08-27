// Función asíncrona que obtiene y muestra el tiempo actual de una ciudad utilizando la API de OpenWeather
async function obtenerTiempo(ciudad) {
  // Realiza una solicitud a la API de OpenWeather para obtener los datos meteorológicos de la ciudad especificada
  const respuesta = await fetch(`${URL_OPEN_WEATHER}&q=${ciudad}`);
  const datos = await respuesta.json(); // Convierte la respuesta en formato JSON

  // Muestra los datos meteorológicos en el elemento con id 'tiempo'
  document.getElementById("tiempo").innerHTML = `
    <img src="https://openweathermap.org/img/wn/${datos.weather[0].icon}@4x.png">
    <p class="text-uppercase">${datos.weather[0].description}</p>
    <p>Temperatura Actual: ${datos.main.temp} °C</p>
    <p>Temperatura Máxima: ${datos.main.temp_max} °C</p>
    <p>Temperatura Mínima: ${datos.main.temp_min} °C</p>
    <p>Humedad: ${datos.main.humidity} %</p>
    <p>Viento: ${datos.wind.speed} m/s</p>
    <p>Presión: ${datos.main.pressure} hPa</p>
  `;
}

// Función que obtiene y muestra una gráfica meteorológica de una ciudad específica desde el servidor Python
function obtenerGrafica(ciudad) {
  // Añade una imagen de la gráfica al elemento con id 'tiempo'
  document.getElementById('tiempo').innerHTML += `
    <img src="${URL_PYTHON}/tiempo/grafica?ciudad=${ciudad}" class="img-fluid mt-4">
  `;
}

// Función asíncrona que obtiene y muestra estadísticas meteorológicas de una ciudad específica desde el servidor Python
async function obtenerEstadisticas(ciudad) {
  // Realiza una solicitud al servidor Python para obtener estadísticas meteorológicas de la ciudad especificada
  let datos = await fetch(`${URL_PYTHON}/tiempo?ciudad=${ciudad}`);
  datos = await datos.json(); // Convierte la respuesta en formato JSON

  // Añade las estadísticas al elemento con id 'tiempo'
  document.getElementById('tiempo').innerHTML += `
    <p>Media de temperatura: ${datos.media_temperatura.toFixed(2)} °C</p>
    <p>Temperatura máxima: ${datos.max_temperatura} °C</p>
    <p>Temperatura mínima: ${datos.min_temperatura} °C</p>
    <p>Media de humedad: ${datos.media_humedad} %</p>
    <p>Media de viento: ${datos.media_viento.toFixed(2)} m/s</p>
    <p>Media de presión: ${datos.media_presion} hPa</p>
    <p>Descripciones del clima:<p>
    <ul>${datos.descripciones.join(`, `)}<ul>
  `;
}

// Función asíncrona que inicializa la aplicación y configura los eventos necesarios
async function inicializa() {
  const formulario = document.getElementById("formulario"); // Referencia al formulario de entrada de la ciudad
  const ciudad = document.getElementById("ciudad"); // Referencia al campo de texto donde se ingresa la ciudad

  // Añade un evento de submit al formulario para obtener y mostrar la información meteorológica cuando se envíe
  formulario.addEventListener("submit", async (e) => {
    e.preventDefault(); // Previene el envío del formulario de forma tradicional

    // Llama a las funciones para obtener y mostrar el tiempo, la gráfica y las estadísticas de la ciudad ingresada
    await obtenerTiempo(ciudad.value);
    obtenerGrafica(ciudad.value);
    obtenerEstadisticas(ciudad.value);
  });

  // Llama a las funciones para mostrar la información meteorológica al cargar la página, usando la ciudad ingresada
  await obtenerTiempo(ciudad.value);
  obtenerGrafica(ciudad.value);
  obtenerEstadisticas(ciudad.value);
}

// Llama a la función de inicialización cuando se carga el script
inicializa();
