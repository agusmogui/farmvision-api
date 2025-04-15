import pyodbc
import os

def get_connection():
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_NAME")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")

    conn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password}'
    )
    return conn

# Opcional: test de conexión local
if __name__ == "__main__":
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sys.tables")
        print("Tablas encontradas:")
        for row in cursor.fetchall():
            print("-", row.name)
        cursor.close()
        conn.close()
    except Exception as e:
        print("❌ Error al conectar:", e)
