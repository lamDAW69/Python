const urlPython = "http://localhost:5000//mascotas";
let timeout = null;

async function obtenerMascotas(caractersticas) {
  let respuesta = await fetch(`${urlPython}?caracteristicas=${encodeURIComponent(caractersticas)}`);
  mascotas = await respuesta.json();

  console.log(mascotas)
  
  const resultado = document.getElementById('mascotas');

  if (mascotas && mascotas.length > 0) {
    resultado.innerHTML = mascotas.map(mascota => `
      <p>${mascota.mascota} (${mascota.similitud.toFixed(2)}%)</p>
    `).join('');
  }
}

function inicializar() {
  document.getElementById('caracteristicas').addEventListener('input', function() {
    clearTimeout(timeout);

    timeout = setTimeout(() => {
      obtenerMascotas(this.value);
    }, 1000); // Espera 1 segundo tras la Ãºltima pulsaciÃ³n de tecla
  });
}

inicializar();