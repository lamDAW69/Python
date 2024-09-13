import pandas as pd 
import matplotlib.pyplot as plt


# Leer el archivo CSV
df = pd.read_csv('pruebas_data.csv')

# Convertir la columna 'fecha' en tipo datetime
df['fecha'] = pd.to_datetime(df['fecha'])

# Crear el gráfico
plt.figure(figsize=(10, 5))
plt.plot(df['fecha'], df['produccion'], marker='o', linestyle='-', color='r')
plt.xlabel('Fecha')
plt.ylabel('Producción KWh')
plt.title('Producción Solar')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()