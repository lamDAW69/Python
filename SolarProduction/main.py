import pandas as pd

# Cargar los datos desde el archivo CSV
df = pd.read_csv('data.csv')

# Verificar algunas entradas de la columna period_en para identificar problemas
print(df['period_en'].head(10))

# Intentar convertir la columna period_en a datetime con errores coerce
df['period_en'] = pd.to_datetime(df['period_en'], errors='coerce')

# Eliminar filas con valores NaT en period_en
df = df.dropna(subset=['period_en'])

# Establecer period_en como índice
df.set_index('period_en', inplace=True)

# Agrupar los datos en intervalos diarios y calcular la media de GHI
df_daily = df.resample('D').agg({'ghi': 'mean'}) # GHI: Global Horizontal Irradiance

# Rellenar valores NaN con 0 si es necesario
df_daily.fillna(0, inplace=True)

# Verificar los primeros registros diarios
print(df_daily.head())
