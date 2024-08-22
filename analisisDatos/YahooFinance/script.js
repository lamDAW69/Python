const python_url = 'http://localhost:5000/finanzas/grafica?'

const empresas = [
    'apple',
    'google', 
    'amazon',  
    'tesla',
    'microsoft',
    'facebook',
    'netflix',
    'spotify',
    'uber',
    'adobe',
    'salesforce',
    'intel'
]
  
  function crearSelect() {
    const select = document.getElementById('empresa');
  
    empresas.forEach(empresa => {
      select.innerHTML += `<option>${empresa}</option>`;
    });
  
    select.addEventListener('change', function() {
      obtenerGrafica(this.value);
    })
  }
  
  function obtenerGrafica(empresa) {
    console.log(empresa)
    console.log("Empresa", empresa)
    
    finanzas = document.getElementById('finanzas');
  
    finanzas.innerHTML = `<img src="${python_url}empresa=${empresa}" class="img-fluid">`;
  }
  
  function inicializa() {
    crearSelect();
  }
  
  inicializa();