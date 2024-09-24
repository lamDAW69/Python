const PYTHON_URL = 'http://localhost:5000';

async function obtenerGrafica(year, circuit, session, driver1, driver2) {
    // Crea la URL de la solicitud con los parámetros
    const url = `${PYTHON_URL}/?year=${year}&circuit=${circuit}&session=${session}&driver1=${driver1}&driver2=${driver2}`;
    
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Error en la solicitud: ' + response.statusText);
        }

        // Convierte la respuesta a blob
        const blob = await response.blob();
        
        // Crea un URL de objeto para el blob
        const imgUrl = URL.createObjectURL(blob);
        
        // Establece la URL de la imagen en el elemento img
        const imgElement = document.getElementById("lap-image");
        imgElement.src = imgUrl; 
        imgElement.style.display = 'block'; // Asegúrate de que se muestre
    } catch (error) {
        console.error('Error al obtener la gráfica:', error);
    }
}

function inicializar() {
    const formulario = document.getElementById("lap-form");
    
    formulario.addEventListener('submit', async function(event) {
        event.preventDefault(); // Evita que se recargue la página
        
        // Obtén los valores del formulario
        const year = document.getElementById("year").value;
        const circuit = document.getElementById("circuits").value;
        const session = document.getElementById("session").value;
        const driver1 = document.getElementById("driver1").value;
        const driver2 = document.getElementById("driver2").value;

        // Llama a la función para obtener la gráfica
        await obtenerGrafica(year, circuit, session, driver1, driver2);
    });
}

inicializar();
