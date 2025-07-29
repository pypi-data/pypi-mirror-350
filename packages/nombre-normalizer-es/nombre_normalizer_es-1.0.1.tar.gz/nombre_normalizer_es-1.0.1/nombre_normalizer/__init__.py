"""
Normalizador de Nombres y Apellidos en Español
==============================================

Un paquete Python para normalizar nombres y apellidos en español,
manejando correctamente las partículas y la separación nombre/apellido.

Uso básico:
    from nombre_normalizer import NombreNormalizer, normalizar_nombre_simple
    
    # Uso simple
    resultado = normalizar_nombre_simple("juan carlos garcia de la torre")
    print(resultado['nombres'])  # "Juan Carlos"
    print(resultado['apellidos'])  # "García de la Torre"
    
    # Uso avanzado
    normalizador = NombreNormalizer()
    df_normalizado = normalizador.procesar_dataframe(df, 'nombre', 'apellido')

Funciones principales:
    - NombreNormalizer: Clase principal del normalizador
    - normalizar_nombre_simple: Función de conveniencia para casos simples
    - procesar_csv: Función de conveniencia para procesar archivos CSV
"""

from nombre_normalizer.nombre_normalizer import (
    NombreNormalizer,
    normalizar_nombre_simple,
    procesar_csv
)

__version__ = "1.0.0"
__author__ = "Assistant"
__email__ = "assistant@example.com"
__all__ = [
    "NombreNormalizer",
    "normalizar_nombre_simple", 
    "procesar_csv"
]


# Información del paquete
__title__ = "nombre-normalizer"
__description__ = "Normalizador de nombres y apellidos en español"
__url__ = "https://github.com/usuario/nombre-normalizer"
__license__ = "MIT"
__copyright__ = "Copyright 2025"