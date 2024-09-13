import pandas as pd

# Cargar el archivo CSV
input_file = 'data.csv'  # Nombre del archivo CSV de entrada
output_file = 'dataclean.csv'  # Nombre del archivo CSV de salida

# Leer el archivo CSV
df = pd.read_csv(input_file)

# Función para parsear fechas
def parse_dates(date_str):
    try:
        # Intentar parsear la fecha con el formato completo
        return pd.to_datetime(date_str, format='%Y-%m-%dT%H:%M:%S%z', errors='coerce')
    except ValueError:
        # Si hay un error, devolver NaT (Not a Time)
        return pd.NaT

# Aplicar la función de parseo a la columna de fechas
df['period_en'] = df['period_en'].apply(parse_dates)

# Opcional: Mostrar filas con fechas inválidas para depuración
invalid_dates = df[df['period_en'].isna()]
if not invalid_dates.empty:
    print("Fechas inválidas encontradas:")
    print(invalid_dates)

# Rellenar NaT con una fecha predeterminada o eliminar filas con NaT
# Rellenar NaT con una fecha predeterminada (opcional)
df['period_en'] = df['period_en'].fillna(pd.Timestamp('1970-01-01'))

# Convertir el formato de la fecha a 'YYYY-MM-DD HH:MM:SS'
df['period_en'] = df['period_en'].dt.strftime('%Y-%m-%d %H:%M:%S')

# Guardar el DataFrame modificado en un nuevo archivo CSV
df.to_csv(output_file, index=False)

print(f'Las fechas han sido convertidas y guardadas en {output_file}')
