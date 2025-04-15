import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class CotizacionScreen extends StatefulWidget {
  const CotizacionScreen({super.key});

  @override
  State<CotizacionScreen> createState() => _CotizacionScreenState();
}

class _CotizacionScreenState extends State<CotizacionScreen> {
  final String baseUrl = 'https://farmvision-api-production.up.railway.app';

  List<dynamic> chasisList = [];
  List<dynamic> componentesList = [];

  int? chasisSeleccionado;
  Set<int> componentesSeleccionados = {};

  double? precioFinal;

  @override
  void initState() {
    super.initState();
    fetchChasis();
    fetchComponentes();
  }

  Future<void> fetchChasis() async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/chasis'));
      if (res.statusCode == 200) {
        setState(() {
          chasisList = json.decode(res.body);
        });
      }
    } catch (e) {
      print("❌ Error al obtener chasis: $e");
    }
  }

  Future<void> fetchComponentes() async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/componentes'));
      if (res.statusCode == 200) {
        setState(() {
          componentesList = json.decode(res.body);
        });
      }
    } catch (e) {
      print("❌ Error al obtener componentes: $e");
    }
  }

  Future<void> cotizar() async {
    if (chasisSeleccionado == null || componentesSeleccionados.isEmpty) return;

    try {
      final res = await http.post(
        Uri.parse('$baseUrl/cotizar'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          "id_chasis": chasisSeleccionado,
          "componentes": componentesSeleccionados.toList(),
          "ganancia": 0.2,
        }),
      );

      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        setState(() {
          precioFinal = data['precio_final'];
        });
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Error al cotizar")),
        );
      }
    } catch (e) {
      print("❌ Error en cotización: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error de conexión: $e")),
      );
    }
  }

  Future<void> testPing() async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/chasis'));
      print("📶 Status: ${res.statusCode}");
      print("📦 Body: ${res.body}");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Conexión OK: ${res.statusCode}")),
      );
    } catch (e) {
      print("❌ Error de conexión: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("Error: $e")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Cotizador FarmVision")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            const Text("Seleccioná un chasis:"),
            DropdownButton<int>(
              isExpanded: true,
              value: chasisSeleccionado,
              hint: const Text("Elegí un chasis"),
              items: chasisList.map<DropdownMenuItem<int>>((chasis) {
                return DropdownMenuItem<int>(
                  value: chasis['id_chasis'],
                  child: Text(chasis['nombre_chasis']),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  chasisSeleccionado = value;
                });
              },
            ),
            const SizedBox(height: 20),
            const Text("Seleccioná los componentes:"),
            Expanded(
              child: ListView(
                children: componentesList.map((componente) {
                  final id = componente['id_componente'];
                  final descripcion = componente['descripcion_componente'];
                  return CheckboxListTile(
                    title: Text(descripcion),
                    value: componentesSeleccionados.contains(id),
                    onChanged: (selected) {
                      setState(() {
                        if (selected == true) {
                          componentesSeleccionados.add(id);
                        } else {
                          componentesSeleccionados.remove(id);
                        }
                      });
                    },
                  );
                }).toList(),
              ),
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: testPing,
                  child: const Text("Test de conexión"),
                ),
                ElevatedButton(
                  onPressed: cotizar,
                  child: const Text("Cotizar"),
                ),
              ],
            ),
            if (precioFinal != null)
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(
                  "Precio total: \$${precioFinal!.toStringAsFixed(2)}",
                  style: const TextStyle(fontSize: 20),
                ),
              ),
          ],
        ),
      ),
    );
  }
}
