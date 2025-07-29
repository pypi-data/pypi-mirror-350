"""
Interfaz de línea de comandos para el normalizador de nombres.
"""

import argparse
import sys
from pathlib import Path
from nombre_normalizer import NombreNormalizer, procesar_csv


def main():
    """Función principal de la CLI."""
    parser = argparse.ArgumentParser(
        description="Normaliza nombres y apellidos en archivos CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  %(prog)s archivo.csv -o resultado.csv -n nombre
  %(prog)s datos.csv -o limpio.csv -n nombre -a apellidos
  %(prog)s personas.csv -o norm.csv -n "nombre completo" --problemas
        """
    )
    
    parser.add_argument(
        "archivo_entrada",
        help="Archivo CSV de entrada"
    )
    
    parser.add_argument(
        "-o", "--output",
        dest="archivo_salida",
        required=True,
        help="Archivo CSV de salida"
    )
    
    parser.add_argument(
        "-n", "--nombre",
        dest="col_nombre",
        required=True,
        help="Nombre de la columna que contiene los nombres"
    )
    
    parser.add_argument(
        "-a", "--apellido",
        dest="col_apellido",
        help="Nombre de la columna que contiene los apellidos (opcional)"
    )
    
    parser.add_argument(
        "--problemas",
        action="store_true",
        help="Exportar casos problemáticos a archivo separado"
    )
    
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="Codificación del archivo CSV (default: utf-8)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mostrar información detallada del procesamiento"
    )
    
    args = parser.parse_args()
    
    # Validar archivos
    entrada = Path(args.archivo_entrada)
    if not entrada.exists():
        print(f"Error: El archivo {entrada} no existe", file=sys.stderr)
        sys.exit(1)
    
    if not entrada.suffix.lower() == '.csv':
        print(f"Advertencia: El archivo {entrada} no tiene extensión .csv")
    
    try:
        # Procesar archivo
        if args.verbose:
            print(f"Procesando {entrada}...")
            print(f"Columna nombres: {args.col_nombre}")
            if args.col_apellido:
                print(f"Columna apellidos: {args.col_apellido}")
        
        procesar_csv(
            str(entrada),
            args.archivo_salida,
            args.col_nombre,
            args.col_apellido
        )
        
        if args.verbose:
            print(f"✓ Procesamiento completado: {args.archivo_salida}")
        
    except Exception as e:
        print(f"Error durante el procesamiento: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()