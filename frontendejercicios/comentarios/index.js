// Función que inicializa los eventos del formulario
function inicializar() {
  // Añade un evento de 'submit' para cuando se envíe el formulario
  document.getElementById('formulario').addEventListener('submit', function(event) {
    event.preventDefault(); // Previene el envío del formulario de forma tradicional
    verificarComentarios(); // Llama a la función que verificará los comentarios
  });

  // Añade un evento de 'reset' para cuando se reinicie el formulario
  document.getElementById('formulario').addEventListener('reset', function() {
    limpiarResultados(); // Llama a la función que limpia los resultados
  });
}

// Función asíncrona que verifica los comentarios introducidos por el usuario
async function verificarComentarios() {
  // Obtiene los comentarios del textarea y los divide por líneas
  const comentarios = document.getElementById('comentarios').value.trim().split('\n');
  const listaComentarios = document.getElementById('listaComentarios'); // Referencia al elemento donde se mostrarán los comentarios verificados
  const resultado = document.getElementById('resultado'); // Referencia al elemento donde se mostrarán los resultados

  // Verifica si hay comentarios para procesar
  if (comentarios.length === 0 || (comentarios.length === 1 && comentarios[0] === "")) {
    resultado.innerHTML = "<p class='text-warning'>No hay comentarios para verificar.</p>";
    return;
  }

  listaComentarios.innerHTML = ""; // Limpia la lista de comentarios previa

  let positivos = 0; // Contador de comentarios positivos
  let negativos = 0; // Contador de comentarios negativos

  // Itera sobre cada comentario
  for (let comentario of comentarios) {
    comentario = comentario.trim(); // Elimina espacios innecesarios
    if (comentario === "") continue; // Ignora comentarios vacíos

    try {
      // Realiza una solicitud fetch al servidor Python para verificar el comentario
      let respuesta = await fetch(`${URL_PYTHON}/comentarios?comentario=${encodeURIComponent(comentario)}`);
      respuesta = await respuesta.json(); // Convierte la respuesta en formato JSON

      // Extrae la probabilidad de que el comentario sea negativo
      const probabilidadNegativo = respuesta.probabilidad_negativo.toFixed(2);

      // Clasifica el comentario como positivo o negativo según la probabilidad
      if (probabilidadNegativo > 50) {
        negativos++;
        listaComentarios.innerHTML += `<li class="list-group-item">${comentario} <span class='text-danger'>(Negativo: ${probabilidadNegativo}%)</span></li>`;
      } else {
        positivos++;
        listaComentarios.innerHTML += `<li class="list-group-item">${comentario} <span class='text-success'>(Positivo: ${100 - probabilidadNegativo}%)</span></li>`;
      }
    } catch (error) {
      // Muestra un mensaje de error si la solicitud falla
      console.error("Error al verificar el comentario:", error);
      listaComentarios.innerHTML += `<li class="list-group-item">${comentario} <span class='text-warning'>(Error al verificar)</span></li>`;
    }
  }

  // Muestra los resultados finales de la verificación
  resultado.innerHTML = `
    <p>Total de comentarios: ${positivos + negativos}</p>
    <p>Comentarios Positivos: ${positivos}</p>
    <p>Comentarios Negativos: ${negativos}</p>
  `;
}

// Función que limpia los resultados de la verificación
function limpiarResultados() {
  document.getElementById('listaComentarios').innerHTML = ""; // Limpia la lista de comentarios
  document.getElementById('resultado').innerHTML = ""; // Limpia el resultado general
}

// Llama a la función inicializar para configurar los eventos del formulario
inicializar();
