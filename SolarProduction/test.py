# Leer el archivo
with open('data.csv', 'w') as file:
    lines = file.readlines()

# Eliminar la coma al final de cada línea
lines = [line.rstrip(',\n') for line in lines]
print(lines)
# Guardar los cambios en el archivo
with open('data.csv', 'w') as file:
    file.writelines(lines)