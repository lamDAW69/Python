// Función que inicializa el evento de entrada de texto para verificar si el texto es SPAM
function inicializar() {
  // Añade un evento de 'input' al campo de texto con id 'texto'
  document.getElementById('texto').addEventListener('input', function() {
    clearTimeout(timeout); // Limpia el temporizador previo si está activo

    // Establece un nuevo temporizador que verifica si el texto es SPAM después de 1 segundo
    timeout = setTimeout(() => {
      verificarSpam(this.value); // Llama a la función para verificar si el texto ingresado es SPAM
    }, 1000); // Espera 1 segundo tras la última pulsación de tecla
  });
}

// Función asíncrona que verifica si el texto ingresado tiene características de SPAM
async function verificarSpam(texto) {
  const resultado = document.getElementById('resultado'); // Referencia al elemento donde se mostrarán los resultados

  // Si el texto está vacío, limpia el resultado y detiene la ejecución de la función
  if (texto.trim() === "") {
    resultado.innerHTML = "";
    return;
  }

  try {
    // Realiza una solicitud fetch al servidor para verificar la probabilidad de que el texto sea SPAM
    let respuesta = await fetch(`${URL_PYTHON}/spam?texto=${encodeURIComponent(texto)}`);
    respuesta = await respuesta.json(); // Convierte la respuesta en formato JSON

    // Muestra la probabilidad de que el texto sea SPAM en un párrafo
    resultado.innerHTML = `<p>Probabilidad de SPAM: ${respuesta.probabilidad_spam.toFixed(2)} %</p>`;

    // Muestra un mensaje adicional basado en si la probabilidad de SPAM es mayor al 50%
    resultado.innerHTML += respuesta.probabilidad_spam > 50
      ? "<span class='text-danger'>Si envías esto, probablemente irá a la carpeta de SPAM ;)</span>"
      : "<span class='text-success'>Este texto NO parece SPAM, probablemente llegará a la bandeja de entrada :)</span>";
  } catch (error) {
    // Muestra un mensaje de error si la solicitud falla
    console.error("Error al verificar el spam:", error);
    resultado.innerHTML = "<span class='text-warning'>Error al verificar el texto</span>";
  }
}

// Inicializa los eventos y funcionalidades cuando se carga el script
inicializar();
