"""
Módulo de conexión a PostgreSQL con pool de conexiones
"""
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, Generator
import time

from src.utils.config import config
from src.utils.logger import get_logger


logger = get_logger(__name__, config.paths.logs_dir)


class DatabaseConnection:
    """Manejador de conexiones a PostgreSQL con pool"""

    def __init__(self):
        self._pool: Optional[pool.SimpleConnectionPool] = None
        self._initialize_pool()

    def _initialize_pool(self):
        """Inicializa el pool de conexiones"""
        try:
            logger.info(f"Inicializando pool de conexiones a {config.database.host}:{config.database.port}")

            self._pool = psycopg2.pool.SimpleConnectionPool(
                minconn=1,
                maxconn=config.database.pool_size,
                host=config.database.host,
                port=config.database.port,
                database=config.database.database,
                user=config.database.user,
                password=config.database.password,
                cursor_factory=RealDictCursor,
                options=f'-c search_path={config.database.schema},public'
            )

            logger.info("Pool de conexiones inicializado exitosamente")

        except psycopg2.Error as e:
            logger.error(f"Error al inicializar pool de conexiones: {e}")
            raise

    @contextmanager
    def get_connection(self) -> Generator:
        """
        Context manager para obtener una conexión del pool

        Yields:
            Conexión de PostgreSQL

        Example:
            with db.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT * FROM table")
        """
        conn = None
        try:
            conn = self._pool.getconn()
            logger.debug("Conexión obtenida del pool")
            yield conn

        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            logger.error(f"Error en la conexión: {e}")
            raise

        finally:
            if conn:
                self._pool.putconn(conn)
                logger.debug("Conexión devuelta al pool")

    @contextmanager
    def get_cursor(self, commit: bool = False) -> Generator:
        """
        Context manager para obtener un cursor listo para usar

        Args:
            commit: Si True, hace commit automático al finalizar

        Yields:
            Cursor de PostgreSQL

        Example:
            with db.get_cursor(commit=True) as cur:
                cur.execute("INSERT INTO table VALUES (%s)", (value,))
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                if commit:
                    conn.commit()
                    logger.debug("Commit realizado")
            except Exception as e:
                conn.rollback()
                logger.error(f"Error en cursor, rollback realizado: {e}")
                raise
            finally:
                cursor.close()

    def execute_query(self, query: str, params: tuple = None, fetch: str = 'all'):
        """
        Ejecuta una query y retorna los resultados

        Args:
            query: Query SQL a ejecutar
            params: Parámetros de la query (opcional)
            fetch: Tipo de fetch ('all', 'one', 'many', None)

        Returns:
            Resultados de la query según el tipo de fetch
        """
        start_time = time.time()

        with self.get_cursor() as cursor:
            try:
                cursor.execute(query, params)

                if fetch == 'all':
                    results = cursor.fetchall()
                elif fetch == 'one':
                    results = cursor.fetchone()
                elif fetch == 'many':
                    results = cursor.fetchmany(size=1000)
                else:
                    results = None

                elapsed = time.time() - start_time
                logger.debug(f"Query ejecutada en {elapsed:.2f}s")

                return results

            except psycopg2.Error as e:
                logger.error(f"Error ejecutando query: {e}")
                logger.error(f"Query: {query[:200]}")
                raise

    def execute_many(self, query: str, params_list: list):
        """
        Ejecuta una query múltiples veces con diferentes parámetros

        Args:
            query: Query SQL a ejecutar
            params_list: Lista de tuplas con parámetros
        """
        with self.get_cursor(commit=True) as cursor:
            try:
                cursor.executemany(query, params_list)
                logger.info(f"Ejecutadas {len(params_list)} operaciones")
            except psycopg2.Error as e:
                logger.error(f"Error en execute_many: {e}")
                raise

    def test_connection(self) -> bool:
        """
        Prueba la conexión a la base de datos

        Returns:
            True si la conexión es exitosa
        """
        try:
            result = self.execute_query("SELECT 1 as test", fetch='one')
            logger.info(f"Test de conexión exitoso: {result}")
            return True
        except Exception as e:
            logger.error(f"Test de conexión fallido: {e}")
            return False

    def close(self):
        """Cierra el pool de conexiones"""
        if self._pool:
            self._pool.closeall()
            logger.info("Pool de conexiones cerrado")

    def __del__(self):
        """Destructor para asegurar cierre del pool"""
        self.close()


# Instancia global de conexión
db = DatabaseConnection()
