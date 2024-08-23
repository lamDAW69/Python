const urlPython = "http://localhost:5000/recetas";
let timeout = null;

async function obtenerRecetas(ingredientes) {
  const respuesta = await fetch(`${urlPython}?ingredientes=${encodeURIComponent(ingredientes)}`);
  let recetas = await respuesta.json();
  recetas = recetas.recetas;
  const resultado = document.getElementById('recetas');

  if (recetas && recetas.length > 0) {
    
    resultado.innerHTML = recetas.map(receta => `
      <p>${receta.receta} (${receta.similitud.toFixed(2)}%)</p>
    `).join('');
  }
  console.log(recetas);
}

function inicializar() {
  document.getElementById('ingredientes').addEventListener('input', function() {
    clearTimeout(timeout);

    timeout = setTimeout(() => {
      obtenerRecetas(this.value);
    }, 1000); // Espera 1 segundo tras la Ãºltima pulsaciÃ³n de tecla
  });
}

inicializar();


inicializar();