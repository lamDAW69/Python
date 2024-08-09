# Lo primero que tenemos que hacer es instalar el conector de mysql
# pip install mysql-connector-python

import mysql.connector

# Establecer conexión
conexion = mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="administrador",
    database="eoi2",
    charset="utf8mb4",
    collation="utf8mb4_general_ci"
)


cursor = conexion.cursor()

cursor.execute("SELECT * FROM empleados")

resultados = cursor.fetchall()
for fila in resultados:
    print(fila)

cursor.close()
conexion.close()