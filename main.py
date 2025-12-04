#!/usr/bin/env python3
"""
Script principal para generación de reportes de trayectoria
"""
import argparse
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.backend.processors import ExcelGenerator
from src.backend.db import db
from src.utils.config import config
from src.utils.logger import get_logger


logger = get_logger(__name__, config.paths.logs_dir)


def generate_reports(grados=None, year_start=None, year_end=None):
    """
    Genera reportes para los grados especificados

    Args:
        grados: Lista de grados (LL, EL, ML). Si es None, genera todos
        year_start: Año inicial
        year_end: Año final
    """
    if grados is None:
        grados = config.reports.grados

    year_start = year_start or config.reports.year_start
    year_end = year_end or config.reports.year_end

    logger.info(f"Generando reportes para: {', '.join(grados)}")
    logger.info(f"Periodo: {year_start}-{year_end}")

    try:
        # Test de conexión
        if not db.test_connection():
            logger.error("No se pudo conectar a la base de datos")
            print("❌ Error: No se pudo conectar a la base de datos")
            print("Verifica la configuración en config/config.yaml o variables de entorno")
            return False

        generator = ExcelGenerator()

        results = {}
        for grado in grados:
            try:
                print(f"\n📊 Generando reporte para {grado}...")
                output_file = generator.generate_report_for_grado(
                    grado,
                    year_start=year_start,
                    year_end=year_end
                )
                results[grado] = output_file
                print(f"   ✅ Generado: {output_file}")

            except Exception as e:
                logger.error(f"Error generando {grado}: {e}")
                print(f"   ❌ Error: {str(e)}")
                results[grado] = None

        # Resumen
        print("\n" + "="*60)
        successful = sum(1 for v in results.values() if v is not None)
        print(f"Generación completada: {successful}/{len(grados)} reportes exitosos")
        print("="*60)

        return successful == len(grados)

    except Exception as e:
        logger.error(f"Error en generación de reportes: {e}")
        print(f"\n❌ Error general: {str(e)}")
        return False


def test_connection():
    """Prueba la conexión a la base de datos"""
    print("🔍 Probando conexión a PostgreSQL...")
    print(f"   Host: {config.database.host}")
    print(f"   Puerto: {config.database.port}")
    print(f"   Base de datos: {config.database.database}")
    print(f"   Usuario: {config.database.user}")

    if db.test_connection():
        print("\n✅ Conexión exitosa!")
        return True
    else:
        print("\n❌ Error en la conexión")
        print("Verifica la configuración y que PostgreSQL esté corriendo")
        return False


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(
        description='Sistema de Generación de Reportes de Trayectoria',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python main.py --generate                    # Genera todos los reportes
  python main.py --generate --grados LL EL     # Solo Licenciatura y Especialidad
  python main.py --generate --year-start 2024  # Solo año 2024
  python main.py --test-connection             # Prueba la conexión a BD
        """
    )

    parser.add_argument(
        '--generate', '-g',
        action='store_true',
        help='Genera reportes Excel'
    )

    parser.add_argument(
        '--grados',
        nargs='+',
        choices=['LL', 'EL', 'ML'],
        help='Grados académicos a procesar (por defecto: todos)'
    )

    parser.add_argument(
        '--year-start',
        type=int,
        help=f'Año inicial (por defecto: {config.reports.year_start})'
    )

    parser.add_argument(
        '--year-end',
        type=int,
        help=f'Año final (por defecto: {config.reports.year_end})'
    )

    parser.add_argument(
        '--test-connection', '-t',
        action='store_true',
        help='Prueba la conexión a la base de datos'
    )

    parser.add_argument(
        '--dashboard', '-d',
        action='store_true',
        help='Inicia el dashboard web'
    )

    args = parser.parse_args()

    # Si no se proporcionan argumentos, mostrar ayuda
    if len(sys.argv) == 1:
        parser.print_help()
        return

    # Test de conexión
    if args.test_connection:
        test_connection()
        return

    # Iniciar dashboard
    if args.dashboard:
        print("🚀 Iniciando dashboard web...")
        print(f"   URL: http://localhost:8501")
        print("\n   Presiona Ctrl+C para detener\n")
        import subprocess
        subprocess.run([
            'streamlit', 'run',
            'src/dashboard/app.py',
            '--server.port', '8501',
            '--server.address', '0.0.0.0'
        ])
        return

    # Generar reportes
    if args.generate:
        config.create_directories()

        success = generate_reports(
            grados=args.grados,
            year_start=args.year_start,
            year_end=args.year_end
        )

        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
