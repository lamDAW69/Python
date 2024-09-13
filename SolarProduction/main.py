import pandas as pd 


#cargar los datos del modelo csv

df = pd.read_csv('data.csv') 

#necesito transformar la columna de period_end a datetime
df['period_end'] = pd.to_datetime(df['period_end'])
print(df.head())

#Agregar datos a Intervalos diarios para simplificar los datos de GHI a intervalos diarios

df_daily = df.resample('D', on='period_end').mean()
#Rellenar los Valores nan con 0 si es necesario 
df_daily.fillna(0, inplace=True)
#Verificar los primeros registros diarios 
print(df_daily.head())