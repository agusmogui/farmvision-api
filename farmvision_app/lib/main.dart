import 'package:flutter/material.dart';
import 'cotizacion.dart';

void main() {
  runApp(const FarmVisionApp());
}

class FarmVisionApp extends StatelessWidget {
  const FarmVisionApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'FarmVision Cotizador',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF121212),
        colorScheme: ColorScheme.dark(
          primary: Colors.greenAccent,
          secondary: Colors.tealAccent,
        ),
      ),
      home: const CotizacionScreen(),
    );
  }
}
