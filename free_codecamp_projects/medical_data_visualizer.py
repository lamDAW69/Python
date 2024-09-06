import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar los datos
df = pd.read_csv('medical_examination.csv')

# Calcular el BMI y crear la columna overweight
df['BMI'] = df['weight'] / (df['height'] / 100) ** 2
df['overweight'] = (df['BMI'] > 25).astype(int)

# Normalizar los datos
df['cholesterol'] = df['cholesterol'].apply(lambda x: 0 if x == 1 else 1)
df['gluc'] = df['gluc'].apply(lambda x: 0 if x == 1 else 1)

def draw_cat_plot():
    # Convertir a formato largo
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    
    # Agrupar y reformatear los datos
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='count')
    
    # Crear el gráfico
    fig = sns.catplot(x='variable', hue='value', col='cardio', data=df_cat, kind='bar', height=4, aspect=1.5)
    
    # Ajustar los ejes y títulos
    fig.set_axis_labels('variable', 'count')
    fig.set_titles('Cardio = {col_name}')
    
    return fig

def draw_heat_map():
    # Filtrar datos incorrectos
    df_heat = df[(df['height'] >= df['height'].quantile(0.025)) &
                 (df['height'] <= df['height'].quantile(0.975)) &
                 (df['weight'] >= df['weight'].quantile(0.025)) &
                 (df['weight'] <= df['weight'].quantile(0.975)) &
                 (df['ap_lo'] <= df['ap_hi'])]
    
    # Calcular la matriz de correlación
    corr = df_heat.corr()
    
    # Crear una máscara para el triángulo superior
    mask = np.triu(np.ones_like(corr, dtype=bool))
    
    # Configurar el tamaño de la figura
    plt.figure(figsize=(10, 8))
    
    # Crear el mapa de calor
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', cmap='coolwarm', center=0, square=True, linewidths=0.5)
    
    plt.show()
