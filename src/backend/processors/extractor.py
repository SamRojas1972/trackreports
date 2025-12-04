"""
Módulo de extracción de datos desde PostgreSQL
"""
import pandas as pd
from typing import Optional, Dict, Any
from datetime import datetime

from src.backend.db import db, QueryBuilder
from src.utils.config import config
from src.utils.logger import get_logger


logger = get_logger(__name__, config.paths.logs_dir)


class DataExtractor:
    """Extractor de datos para reportes de trayectoria"""

    def __init__(self, year_start: Optional[int] = None, year_end: Optional[int] = None):
        """
        Inicializa el extractor

        Args:
            year_start: Año inicial (por defecto desde config)
            year_end: Año final (por defecto desde config)
        """
        self.year_start = year_start or config.reports.year_start
        self.year_end = year_end or config.reports.year_end
        self.query_builder = QueryBuilder(self.year_start, self.year_end)
        logger.info(f"DataExtractor inicializado para años {self.year_start}-{self.year_end}")

    def _query_to_dataframe(self, query: str, query_name: str = "") -> pd.DataFrame:
        """
        Ejecuta una query y retorna un DataFrame

        Args:
            query: Query SQL a ejecutar
            query_name: Nombre descriptivo de la query (para logs)

        Returns:
            DataFrame con los resultados
        """
        try:
            logger.info(f"Ejecutando query: {query_name}")
            start_time = datetime.now()

            results = db.execute_query(query, fetch='all')

            if not results:
                logger.warning(f"Query '{query_name}' no retornó resultados")
                return pd.DataFrame()

            # Convertir a DataFrame
            df = pd.DataFrame(results)

            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"Query '{query_name}' completada: {len(df)} filas en {elapsed:.2f}s")

            return df

        except Exception as e:
            logger.error(f"Error ejecutando query '{query_name}': {e}")
            raise

    def extract_reporte_periodo_programa(self) -> pd.DataFrame:
        """
        Extrae reporte por periodo y programa

        Returns:
            DataFrame con columnas: periodo_id, programa_id, nuevo_ingreso, egresados, titulados
        """
        query = self.query_builder.get_query('periodo_programa')
        return self._query_to_dataframe(query, "Reporte Periodo-Programa")

    def extract_resumen_grado(self, grado: str) -> pd.DataFrame:
        """
        Extrae resumen por grado académico

        Args:
            grado: Grado académico (LL, EL, ML)

        Returns:
            DataFrame con totales por periodo
        """
        query = self.query_builder.get_query('resumen', grado=grado)
        return self._query_to_dataframe(query, f"Resumen {grado}")

    def extract_nuevo_ingreso(self, grado: str) -> pd.DataFrame:
        """
        Extrae estudiantes de nuevo ingreso

        Args:
            grado: Grado académico (LL, EL, ML)

        Returns:
            DataFrame con estudiantes de nuevo ingreso
        """
        query = self.query_builder.get_query('nuevo_ingreso', grado=grado)
        return self._query_to_dataframe(query, f"Nuevo Ingreso {grado}")

    def extract_reinscritos(self, grado: str) -> pd.DataFrame:
        """
        Extrae estudiantes reinscritos

        Args:
            grado: Grado académico (LL, EL, ML)

        Returns:
            DataFrame con estudiantes reinscritos
        """
        query = self.query_builder.get_query('reinscritos', grado=grado)
        return self._query_to_dataframe(query, f"Reinscritos {grado}")

    def extract_todos_datos(self) -> pd.DataFrame:
        """
        Extrae todos los datos consolidados

        Returns:
            DataFrame con todos los datos históricos
        """
        query = self.query_builder.get_query('todos')
        return self._query_to_dataframe(query, "Todos los Datos")

    def extract_all_for_grado(self, grado: str) -> Dict[str, pd.DataFrame]:
        """
        Extrae todos los datos necesarios para un grado académico

        Args:
            grado: Grado académico (LL, EL, ML)

        Returns:
            Diccionario con todos los DataFrames necesarios
        """
        logger.info(f"Extrayendo todos los datos para grado {grado}")

        try:
            data = {
                'resumen': self.extract_resumen_grado(grado),
                'nuevo_ingreso': self.extract_nuevo_ingreso(grado),
                'reinscritos': self.extract_reinscritos(grado),
                'todos': self.extract_todos_datos()
            }

            # Log de resumen
            total_rows = sum(len(df) for df in data.values())
            logger.info(f"Extracción completada para {grado}: {total_rows} filas totales")

            for key, df in data.items():
                logger.debug(f"  - {key}: {len(df)} filas")

            return data

        except Exception as e:
            logger.error(f"Error en extracción completa para {grado}: {e}")
            raise

    def extract_custom_query(self, query: str, query_name: str = "Custom") -> pd.DataFrame:
        """
        Ejecuta una query personalizada

        Args:
            query: Query SQL a ejecutar
            query_name: Nombre descriptivo

        Returns:
            DataFrame con resultados
        """
        return self._query_to_dataframe(query, query_name)

    def get_periodos_disponibles(self) -> pd.DataFrame:
        """
        Obtiene la lista de periodos disponibles

        Returns:
            DataFrame con periodos
        """
        query = f"""
        SELECT DISTINCT id, "year", descripcion
        FROM core.periodo
        WHERE "year" BETWEEN {self.year_start} AND {self.year_end}
        ORDER BY id
        """
        return self._query_to_dataframe(query, "Periodos Disponibles")

    def get_programas_disponibles(self, grado: Optional[str] = None) -> pd.DataFrame:
        """
        Obtiene la lista de programas disponibles

        Args:
            grado: Filtrar por grado (opcional)

        Returns:
            DataFrame con programas
        """
        grado_filter = f"AND id LIKE '{grado}%'" if grado else ""

        query = f"""
        SELECT DISTINCT
            id,
            nombre,
            plan,
            escuela,
            campus,
            grado_academico_id
        FROM core.programa
        WHERE id IN (SELECT clave_programa FROM core.programas_titulados)
        {grado_filter}
        ORDER BY id
        """
        return self._query_to_dataframe(query, f"Programas {grado or 'Todos'}")


def test_extraction():
    """Función de prueba para el extractor"""
    logger.info("=== Iniciando test de extracción ===")

    try:
        # Test de conexión
        if not db.test_connection():
            logger.error("No se pudo conectar a la base de datos")
            return

        extractor = DataExtractor(year_start=2024, year_end=2025)

        # Test de extracción para LL
        logger.info("\nTest: Extrayendo datos para LL")
        data_ll = extractor.extract_all_for_grado('LL')

        for key, df in data_ll.items():
            print(f"\n{key.upper()}:")
            print(f"  Filas: {len(df)}")
            if not df.empty:
                print(f"  Columnas: {list(df.columns)}")
                print(f"  Muestra:")
                print(df.head(3).to_string(index=False))

        logger.info("\n=== Test completado exitosamente ===")

    except Exception as e:
        logger.error(f"Error en test: {e}")
        raise


if __name__ == "__main__":
    test_extraction()
