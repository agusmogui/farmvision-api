from db_connect import get_connection

def crear_tablas():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Tabla chasis
        cursor.execute("""
        IF OBJECT_ID('chasis', 'U') IS NULL
        BEGIN
            CREATE TABLE chasis (
                id_chasis INT IDENTITY PRIMARY KEY,
                nombre_chasis VARCHAR(100),
                descripcion TEXT,
                precio_base DECIMAL(18,2),
                stock INT
            )
        END
        """)

        # Tabla componentes
        cursor.execute("""
        IF OBJECT_ID('componentes', 'U') IS NULL
        BEGIN
            CREATE TABLE componentes (
                id_componente INT IDENTITY PRIMARY KEY,
                descripcion_componente VARCHAR(150),
                tipo_componente VARCHAR(50),
                costo_componente DECIMAL(18,2),
                stock INT
            )
        END
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Tablas 'chasis' y 'componentes' creadas correctamente.")

    except Exception as e:
        print("❌ Error al crear tablas:", e)

if __name__ == "__main__":
    crear_tablas()
