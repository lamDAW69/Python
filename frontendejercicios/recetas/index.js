// Función que inicializa los eventos y la carga de ingredientes
function inicializar() {
  // Añade un evento para cuando el contenido del documento ha sido completamente cargado
  document.addEventListener('DOMContentLoaded', function() {
    cargarIngredientes(); // Llama a la función para cargar los ingredientes desde el servidor
  });

  // Añade un evento de 'input' al campo de texto de ingredientes
  document.getElementById('ingredientes').addEventListener('input', function() {
    clearTimeout(timeout); // Limpia el temporizador previo si está activo

    // Establece un nuevo temporizador que sincroniza los checkboxes y obtiene las recetas después de 1 segundo
    timeout = setTimeout(() => {
      sincronizarCheckboxes(this.value); // Sincroniza el estado de los checkboxes con el texto ingresado
      obtenerRecetas(this.value); // Obtiene las recetas que coinciden con los ingredientes ingresados
    }, 1000);
  });

  // Añade un evento de 'reset' al formulario para limpiar el resultado cuando se reinicia el formulario
  document.getElementById('formulario').addEventListener('reset', function() {
    document.getElementById('resultado').innerHTML = ""; // Limpia el contenido del elemento de resultados
  });
}

// Función asíncrona que carga los ingredientes desde el servidor y los muestra como checkboxes
async function cargarIngredientes() {
  try {
    // Realiza una solicitud fetch al servidor para obtener la lista de ingredientes
    let respuesta = await fetch(`${URL_PYTHON}/recetas/ingredientes`);
    let ingredientes = await respuesta.json(); // Convierte la respuesta en formato JSON
    const container = document.getElementById('checkboxes-container'); // Referencia al contenedor de los checkboxes

    // Crea y añade los checkboxes al contenedor basado en los ingredientes obtenidos
    container.innerHTML = ingredientes.map(ingrediente => `
      <div class="form-check form-check-inline small">
        <input class="form-check-input" type="checkbox" id="ingrediente-${ingrediente}" value="${ingrediente}">
        <label class="form-check-label me-2" for="ingrediente-${ingrediente}">${ingrediente}</label>
      </div>
    `).join('');

    // Añade un evento 'change' a cada checkbox para actualizar el textarea y obtener las recetas
    document.querySelectorAll('#checkboxes-container input[type="checkbox"]').forEach(checkbox => {
      checkbox.addEventListener('change', function() {
        actualizarTextarea(); // Actualiza el campo de texto de ingredientes basado en los checkboxes seleccionados
        obtenerRecetas(document.getElementById('ingredientes').value); // Obtiene las recetas que coinciden con los ingredientes seleccionados
      });
    });
  } catch (error) {
    // Muestra un mensaje de error si la solicitud falla
    console.error("Error al cargar los ingredientes:", error);
  }
}

// Función que actualiza el campo de texto de ingredientes basado en los checkboxes seleccionados
function actualizarTextarea() {
  const seleccionadas = Array.from(document.querySelectorAll('#checkboxes-container input[type="checkbox"]:checked'))
                              .map(checkbox => checkbox.value); // Obtiene los valores de los checkboxes seleccionados

  // Une los valores seleccionados en una cadena de texto separada por comas y la asigna al campo de texto
  document.getElementById('ingredientes').value = seleccionadas.join(', ');
}

// Función que sincroniza el estado de los checkboxes con el texto ingresado en el campo de ingredientes
function sincronizarCheckboxes(texto) {
  const ingredientes = texto.split(',').map(c => c.trim().toLowerCase()); // Divide el texto en una lista de ingredientes

  // Itera sobre todos los checkboxes y los marca o desmarca según los ingredientes en el texto
  document.querySelectorAll('#checkboxes-container input[type="checkbox"]').forEach(checkbox => {
    checkbox.checked = ingredientes.includes(checkbox.value.toLowerCase()); // Sincroniza el estado del checkbox
  });
}

// Función asíncrona que obtiene las recetas que coinciden con los ingredientes seleccionados o ingresados
async function obtenerRecetas(ingredientes) {
  const resultado = document.getElementById('resultado'); // Referencia al elemento donde se mostrarán los resultados

  // Si no hay ingredientes ingresados, limpia el resultado y detiene la ejecución de la función
  if (ingredientes.trim() === "") {
    resultado.innerHTML = "";
    return;
  }

  try {
    // Realiza una solicitud fetch al servidor para obtener las recetas que coinciden con los ingredientes
    let respuesta = await fetch(`${URL_PYTHON}/recetas?ingredientes=${encodeURIComponent(ingredientes)}`);
    respuesta = await respuesta.json(); // Convierte la respuesta en formato JSON

    // Si se encontraron recetas, las muestra en el resultado; de lo contrario, muestra un mensaje de advertencia
    if (respuesta && respuesta.length > 0) {
      resultado.innerHTML = respuesta.map(receta => `
        <p>${receta.receta} (${receta.similitud.toFixed(2)}%)</p>
      `).join('');
    } else {
      resultado.innerHTML = "<span class='text-warning'>No se encontraron recetas con esos ingredientes.</span>";
    }
  } catch (error) {
    // Muestra un mensaje de error si la solicitud falla
    console.error("Error al obtener recetas:", error);
    resultado.innerHTML = "<span class='text-warning'>Error al obtener las recetas</span>";
  }
}

// Inicializar los eventos y funcionalidades
inicializar();
