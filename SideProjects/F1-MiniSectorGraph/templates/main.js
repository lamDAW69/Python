const PYTHON_URL = 'http://localhost:5000';

async function obtenerGrafica(year, circuit, session, driver1, driver2) {
    const lapImageElement = document.getElementById("lap-image");
    const url = `${PYTHON_URL}/?year=${year}&circuit=${circuit}&session=${session}&driver1=${driver1}&driver2=${driver2}`;
    lapImageElement.src = url;

    lapImageElement.onload = function() {
        lapImageElement.classList.add('show');
    };

    lapImageElement.onerror = function() {
        lapImageElement.classList.remove('show');
        alert('Error al cargar estadisticas, el piloto seleccionado no tiene datos para la temporada seleccionada');
    };
    
}

function inicializar() {
    const formulario = document.getElementById("lap-form");
    
    formulario.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const year = document.getElementById("year").value;
        const circuit = document.getElementById("circuits").value;
        const session = document.getElementById("session").value;
        const driver1 = document.getElementById("driver1").value;
        const driver2 = document.getElementById("driver2").value;

        await obtenerGrafica(year, circuit, session, driver1, driver2);
    });
}

inicializar();


//Proyecto finalizado con éxito