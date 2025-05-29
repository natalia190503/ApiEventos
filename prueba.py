import pymysql

conn = pymysql.connect(
    host='34.9.135.98',
    user='natalia',
    password='TuContraseña123',
    database='eventosdb',
    port=3306
)

print("Conectado a MySQL correctamente!")
conn.close()
