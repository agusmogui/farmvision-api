import pymssql
import os

def get_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")

    conn = pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database
    )
    return conn

# Test de conexión si se ejecuta directamente
if __name__ == "__main__":
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.tables")
        print("Tablas encontradas:")
        for row in cursor.fetchall():
            print("-", row[0])
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error al conectar:", e)

