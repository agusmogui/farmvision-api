from db_connect import get_connection

def insertar_datos():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # === Inserción de CHASIS ===
        chasis_data = [
            ("Sembradora Neumática 12 surcos", "Chasis para siembra directa, adaptable a varios tipos de cultivo.", 3200000, 5),
            ("Pulverizadora Autopropulsada 2500L", "Chasis con cabina y brazos extensibles, base para sistema de pulverización.", 5500000, 3),
            ("Fertilizadora de arrastre 5000L", "Chasis reforzado con sistema de doble eje para fertilización a granel.", 2800000, 6),
            ("Cosechadora Compacta Serie 400", "Chasis estructural para cosecha de trigo, soja y maíz.", 6200000, 2),
            ("Tolva Autodescargable 18tn", "Chasis con eje reforzado y sinfín interno.", 4100000, 4)
        ]

        cursor.executemany("""
            INSERT INTO chasis (nombre_chasis, descripcion, precio_base, stock)
            VALUES (?, ?, ?, ?)
        """, chasis_data)

        # === Inserción de COMPONENTES ===
        componentes_data = [
            ("Motor Diésel 180HP Perkins", "motor", 1150000, 10),
            ("Motor Diésel 240HP Cummins", "motor", 1750000, 8),
            ("Motor Eléctrico 90kW", "motor", 980000, 6),
            ("Batería de Ion-Litio 120Ah", "energía", 370000, 15),
            ("Rodado Agrícola 36\" Michelin", "rodado", 185000, 20),
            ("Rodado Doble 42\" Firestone", "rodado", 310000, 12),
            ("Eje delantero reforzado con pivote", "estructura", 220000, 10),
            ("Eje trasero con sistema de arrastre", "estructura", 240000, 10),
            ("Módulo hidráulico de 3 salidas", "hidráulico", 135000, 20),
            ("Kit de válvulas electrónicas de control", "electrónico", 180000, 25),
            ("Display digital con GPS", "cabina", 320000, 10),
            ("Sensor de humedad y temperatura", "sensor", 80000, 30),
            ("Tolva plástica 3000L", "tolva", 290000, 14),
            ("Tolva metálica 5000L con tapa", "tolva", 430000, 12),
            ("Tanque pulverizador 2500L", "tanque", 360000, 8),
            ("Kit de sinfín para tolva", "tolva", 180000, 18),
            ("Pintura epoxi anti-óxido gris", "pintura", 45000, 50),
            ("Faros LED de alta potencia x2", "iluminación", 60000, 40)
        ]

        cursor.executemany("""
            INSERT INTO componentes (descripcion_componente, tipo_componente, costo_componente, stock)
            VALUES (?, ?, ?, ?)
        """, componentes_data)

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Datos insertados correctamente.")

    except Exception as e:
        print("❌ Error al insertar datos:", e)

if __name__ == "__main__":
    insertar_datos()
