from flask import Flask, jsonify, request
from db_connect import get_connection

app = Flask(__name__)

@app.route("/")
def home():
    return "🚜 FarmVision API Activa"

@app.route("/chasis", methods=["GET"])
def get_chasis():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_chasis, nombre_chasis, descripcion, precio_base, stock FROM chasis")
        data = cursor.fetchall()
        columnas = [column[0] for column in cursor.description]
        resultado = [dict(zip(columnas, row)) for row in data]
        conn.close()
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Error en /chasis: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/componentes", methods=["GET"])
def get_componentes():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_componente, descripcion_componente, tipo_componente, costo_componente, stock FROM componentes")
        data = cursor.fetchall()
        columnas = [column[0] for column in cursor.description]
        resultado = [dict(zip(columnas, row)) for row in data]
        conn.close()
        return jsonify(resultado)
    except Exception as e:
        print(f"❌ Error en /componentes: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/cotizar", methods=["POST"])
def cotizar():
    try:
        datos = request.json
        id_chasis = datos.get("id_chasis")
        componentes = datos.get("componentes", [])
        ganancia = datos.get("ganancia", 0.20)

        conn = get_connection()
        cursor = conn.cursor()

        # Precio del chasis
        cursor.execute("SELECT precio_base FROM chasis WHERE id_chasis = %s", (id_chasis,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Chasis no encontrado"}), 404
        precio_total = row[0]

        # Precios de los componentes
        if componentes:
            placeholders = ",".join(["%s"] * len(componentes))
            cursor.execute(
                f"SELECT SUM(costo_componente) FROM componentes WHERE id_componente IN ({placeholders})",
                componentes
            )
            comp_total = cursor.fetchone()[0] or 0
            precio_total += comp_total

        # Aplicar ganancia
        precio_final = round(precio_total * (1 + ganancia), 2)

        conn.close()
        return jsonify({
            "precio_base": precio_total,
            "precio_final": precio_final,
            "ganancia_aplicada": f"{int(ganancia * 100)}%"
        })

    except Exception as e:
        print(f"❌ Error en /cotizar: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))  # Railway configura esta variable automáticamente
    app.run(host='0.0.0.0', port=port)
