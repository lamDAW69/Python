// Función que inicializa el evento de entrada de texto para traducirlo
function inicializar() {
  // Añade un evento de 'input' al campo de texto con id 'texto'
  document.getElementById('texto').addEventListener('input', function() {
    clearTimeout(timeout); // Limpia el temporizador previo si está activo

    // Establece un nuevo temporizador que realiza la traducción después de 1 segundo
    timeout = setTimeout(() => {
      traducirTexto(this.value); // Llama a la función para traducir el texto ingresado
    }, 1000); // Espera 1 segundo tras la última pulsación de tecla
  });
}

// Función asíncrona que envía el texto al servidor para traducirlo y muestra el resultado
async function traducirTexto(texto) {
  const resultado = document.getElementById('resultado'); // Referencia al elemento donde se mostrará la traducción

  // Si el campo de texto está vacío, limpia el resultado y detiene la ejecución de la función
  if (texto.trim() === "") {
    resultado.innerHTML = "";
    return;
  }

  // Muestra un spinner mientras se espera la traducción
  resultado.innerHTML = `
    <div class="spinner-border text-primary" role="status"></div>
  `;

  try {
    // Realiza una solicitud fetch al servidor Python para obtener la traducción del texto
    let respuesta = await fetch(`${URL_PYTHON}/traductor?texto=${encodeURIComponent(texto)}`);
    respuesta = await respuesta.json(); // Convierte la respuesta en formato JSON

    // Muestra la traducción en el div resultado
    resultado.innerHTML = `<p>${respuesta}</p>`;
  } catch (error) {
    // Muestra un mensaje de error si la solicitud falla
    console.error("Error al traducir el texto:", error);
    resultado.innerHTML = "<span class='text-warning'>Error al traducir el texto</span>";
  }
}

// Inicializar los eventos y funcionalidades cuando se carga el script
inicializar();
