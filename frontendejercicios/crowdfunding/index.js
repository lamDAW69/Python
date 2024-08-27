// Función para cargar las categorías desde el servidor
async function cargarCategorias() {
  try {
    let respuesta = await fetch(`${URL_PYTHON}/crowdfunding/categorias`);
    respuesta = await respuesta.json();

    const selectCategoria = document.getElementById('categoria');
    respuesta.categorias.forEach(categoria => {
      const opcion = document.createElement('option');
      opcion.value = categoria;
      opcion.textContent = categoria;
      selectCategoria.appendChild(opcion);
    });
  } catch (error) {
    console.error("Error al cargar las categorías:", error);
  }
}

// Función que inicializa el evento para capturar la entrada del usuario en los campos del formulario
function inicializar() {
  // Selecciona todos los inputs dentro del formulario
  const inputs = document.querySelectorAll('#formulario input, #formulario select');
  inputs.forEach(input => {
    // Añade un evento que se dispara cada vez que hay un cambio en alguno de los inputs
    input.addEventListener('input', function() {
      // Limpia el temporizador previo si se está ejecutando
      clearTimeout(timeout);

      // Establece un nuevo temporizador que ejecuta la función calcularViabilidad después de 500 ms
      timeout = setTimeout(() => {
        calcularViabilidad();
      }, 500); // Espera 500 ms tras la última pulsación de tecla
    });
  });
}

// Función asíncrona que calcula la probabilidad de éxito del crowdfunding
async function calcularViabilidad() {
  // Obtiene los valores de los inputs del formulario
  const categoria = document.getElementById('categoria').value;
  const meta_financiera = document.getElementById('meta_financiera').value;
  const dinero_recaudado = document.getElementById('dinero_recaudado').value;
  const duracion = document.getElementById('duracion').value;
  const numero_patrocinadores = document.getElementById('numero_patrocinadores').value;

  // Si alguno de los campos está vacío, limpia el resultado y detiene la ejecución de la función
  if (!categoria || !meta_financiera || !dinero_recaudado || !duracion || !numero_patrocinadores) {
    document.getElementById('resultado').innerHTML = "";
    return;
  }

  try {
    // Realiza una solicitud fetch al servidor Python con los parámetros correspondientes
    let respuesta = await fetch(`${URL_PYTHON}/crowdfunding/prediccion?categoria=${categoria}&meta_financiera=${meta_financiera}&dinero_recaudado=${dinero_recaudado}&duracion=${duracion}&numero_patrocinadores=${numero_patrocinadores}`);
    respuesta = await respuesta.json(); // Convierte la respuesta en formato JSON

    // Muestra la probabilidad de éxito en el elemento con id 'resultado'
    document.getElementById('resultado').innerHTML = `<p>Probabilidad de éxito: ${respuesta.probabilidad_exito}</p>`;
  } catch (error) {
    // Muestra un mensaje de error si la solicitud falla
    console.error("Error al calcular la viabilidad del proyecto:", error);
    document.getElementById('resultado').innerHTML = "<span class='text-warning'>Error al calcular la viabilidad</span>";
  }
}

// Llama a la función para cargar las categorías al cargar la página
cargarCategorias();

// Llama a la función inicializar para configurar los eventos del formulario
inicializar();
