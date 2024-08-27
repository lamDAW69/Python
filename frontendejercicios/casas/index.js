// Función que inicializa el evento para capturar la entrada del usuario en los campos del formulario
function inicializar() {
  // Selecciona todos los inputs dentro del formulario
  const inputs = document.querySelectorAll('#formulario input');
  inputs.forEach(input => {
    // Añade un evento que se dispara cada vez que hay un cambio en alguno de los inputs
    input.addEventListener('input', function() {
      // Limpia el temporizador previo si se está ejecutando
      clearTimeout(timeout);

      // Establece un nuevo temporizador que ejecuta la función calcularPrecio después de 500 ms
      timeout = setTimeout(() => {
        calcularPrecio();
      }, 500); // Espera 500 ms tras la última pulsación de tecla
    });
  });
}

// Función asíncrona que calcula el precio estimado de la casa
async function calcularPrecio() {
  // Obtiene los valores de los inputs del formulario
  const tamanyo = document.getElementById('tamanyo').value;
  const habitaciones = document.getElementById('habitaciones').value;
  const banyos = document.getElementById('banyos').value;
  const garajes = document.getElementById('garajes').value;

  // Si alguno de los campos está vacío, limpia el resultado y detiene la ejecución de la función
  if (!tamanyo || !habitaciones || !banyos || !garajes) {
    document.getElementById('resultado').innerHTML = "";
    return;
  }

  try {
    // Realiza una solicitud fetch al servidor Python con los parámetros correspondientes
    let respuesta = await fetch(`${URL_PYTHON}/casas?tamanyo=${tamanyo}&habitaciones=${habitaciones}&banyos=${banyos}&garajes=${garajes}`);
    respuesta = await respuesta.json(); // Convierte la respuesta en formato JSON

    // Formatear el precio en formato español con dos decimales
    const precioFormateado = respuesta.precio.toLocaleString('es-ES', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });

    // Muestra el precio estimado en el elemento con id 'resultado'
    document.getElementById('resultado').innerHTML = `<p>Precio estimado: ${precioFormateado} €</p>`;
  } catch (error) {
    // Muestra un mensaje de error si la solicitud falla
    console.error("Error al calcular el precio de la casa:", error);
    document.getElementById('resultado').innerHTML = "<span class='text-warning'>Error al calcular el precio</span>";
  }
}

// Llama a la función inicializar para configurar los eventos del formulario
inicializar();
