// Función que inicializa los eventos y la carga de características
function inicializar() {
  // Añade un evento para cuando el contenido del documento ha sido completamente cargado
  document.addEventListener('DOMContentLoaded', function() {
    cargarCaracteristicas(); // Llama a la función para cargar las características desde el servidor
  });

  // Añade un evento de 'input' al campo de texto de características
  document.getElementById('caracteristicas').addEventListener('input', function() {
    clearTimeout(timeout); // Limpia el temporizador previo si está activo

    // Establece un nuevo temporizador que sincroniza los checkboxes y obtiene las mascotas después de 1 segundo
    timeout = setTimeout(() => {
      sincronizarCheckboxes(this.value); // Sincroniza el estado de los checkboxes con el texto introducido
      obtenerMascotas(this.value); // Obtiene las mascotas que coinciden con las características introducidas
    }, 1000);
  });

  // Añade un evento de 'reset' al formulario para limpiar el resultado cuando se reinicia el formulario
  document.getElementById('formulario').addEventListener('reset', function() {
    document.getElementById('resultado').innerHTML = ""; // Limpia el contenido del elemento de resultados
  });
}

// Función asíncrona que carga las características desde el servidor y las muestra como checkboxes
async function cargarCaracteristicas() {
  try {
    // Realiza una solicitud fetch al servidor para obtener las características de las mascotas
    let respuesta = await fetch(`${URL_PYTHON}/mascotas/caracteristicas`);
    let caracteristicas = await respuesta.json(); // Convierte la respuesta en formato JSON
    const container = document.getElementById('checkboxes-container'); // Referencia al contenedor de los checkboxes

    // Crea y añade los checkboxes al contenedor basado en las características obtenidas
    container.innerHTML = caracteristicas.map(caracteristica => `
      <div class="form-check form-check-inline small">
        <input class="form-check-input" type="checkbox" id="caracteristica-${caracteristica}" value="${caracteristica}">
        <label class="form-check-label me-2" for="caracteristica-${caracteristica}">${caracteristica}</label>
      </div>
    `).join('');

    // Añade un evento 'change' a cada checkbox para actualizar el textarea y obtener las mascotas
    document.querySelectorAll('#checkboxes-container input[type="checkbox"]').forEach(checkbox => {
      checkbox.addEventListener('change', function() {
        actualizarTextarea(); // Actualiza el campo de texto de características basado en los checkboxes seleccionados
        obtenerMascotas(document.getElementById('caracteristicas').value); // Obtiene las mascotas que coinciden con las características seleccionadas
      });
    });
  } catch (error) {
    // Muestra un mensaje de error si la solicitud falla
    console.error("Error al cargar las características:", error);
  }
}

// Función que actualiza el campo de texto de características basado en los checkboxes seleccionados
function actualizarTextarea() {
  const seleccionadas = Array.from(document.querySelectorAll('#checkboxes-container input[type="checkbox"]:checked'))
                              .map(checkbox => checkbox.value); // Obtiene los valores de los checkboxes seleccionados

  // Une los valores seleccionados en una cadena de texto separada por comas y la asigna al campo de texto
  document.getElementById('caracteristicas').value = seleccionadas.join(', ');
}

// Función que sincroniza el estado de los checkboxes con el texto ingresado en el campo de características
function sincronizarCheckboxes(texto) {
  const caracteristicas = texto.split(',').map(c => c.trim().toLowerCase()); // Divide el texto en una lista de características

  // Itera sobre todos los checkboxes y los marca o desmarca según las características en el texto
  document.querySelectorAll('#checkboxes-container input[type="checkbox"]').forEach(checkbox => {
    checkbox.checked = caracteristicas.includes(checkbox.value.toLowerCase()); // Sincroniza el estado del checkbox
  });
}

// Función asíncrona que obtiene las mascotas que coinciden con las características seleccionadas o ingresadas
async function obtenerMascotas(caracteristicas) {
  const resultado = document.getElementById('resultado'); // Referencia al elemento donde se mostrarán los resultados

  // Si no hay características ingresadas, limpia el resultado y detiene la ejecución de la función
  if (caracteristicas.trim() === "") {
    resultado.innerHTML = "";
    return;
  }

  try {
    // Realiza una solicitud fetch al servidor para obtener las mascotas que coinciden con las características
    let respuesta = await fetch(`${URL_PYTHON}/mascotas?caracteristicas=${encodeURIComponent(caracteristicas)}`);
    respuesta = await respuesta.json(); // Convierte la respuesta en formato JSON

    // Si se encontraron mascotas, las muestra en el resultado; de lo contrario, muestra un mensaje de advertencia
    if (respuesta && respuesta.length > 0) {
      resultado.innerHTML = respuesta.map(mascota => `
        <p>${mascota.mascota} (${mascota.similitud.toFixed(2)}%)</p>
      `).join('');
    } else {
      resultado.innerHTML = "<span class='text-warning'>No se encontraron mascotas con esas características.</span>";
    }
  } catch (error) {
    // Muestra un mensaje de error si la solicitud falla
    console.error("Error al obtener mascotas:", error);
    resultado.innerHTML = "<span class='text-warning'>Error al obtener las mascotas</span>";
  }
}

// Inicializa los eventos y funcionalidades cuando se carga el script
inicializar();
