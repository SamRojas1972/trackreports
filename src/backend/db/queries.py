"""
Módulo de queries SQL para reportes de trayectoria
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class QueryTemplate:
    """Template de query SQL con parámetros"""
    name: str
    sql: str
    description: str

    def format(self, **kwargs) -> str:
        """Formatea la query con los parámetros proporcionados"""
        return self.sql.format(**kwargs)


class TrayectoriaQueries:
    """Colección de queries para reportes de trayectoria"""

    @staticmethod
    def get_reporte_periodo_programa(year_start: int, year_end: int) -> str:
        """
        Reporte 1: Datos por periodo y programa

        Returns:
            Query SQL con nuevo ingreso, egresados y titulados por periodo/programa
        """
        return f"""
        SELECT
            pe.id AS "periodo_id",
            pr.id AS "programa_id",
            (
                SELECT count(*)
                FROM core.lista_asistencia AS la
                JOIN core.estudiante AS e ON la.estudiante_id = e.id
                JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
                WHERE la.periodo_id = pe.id AND ep.programa_id = pr.id
                AND ep.periodo_ingreso_id = pe.id
            ) AS "nuevo_ingreso",
            (
                SELECT count(*)
                FROM core.lista_asistencia AS la
                JOIN core.estudiante AS e ON la.estudiante_id = e.id
                JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
                WHERE la.periodo_id = pe.id AND ep.programa_id = pr.id
                AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
            ) AS "egresados",
            (
                SELECT count(*)
                FROM core.lista_asistencia AS la
                JOIN core.estudiante AS e ON la.estudiante_id = e.id
                JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
                JOIN core.titulado AS t ON (ep.estudiante_id, ep.programa_id) = (t.estudiante_id, t.programa_id)
                WHERE la.periodo_id = pe.id AND ep.programa_id = pr.id
                AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
            ) AS "titulados"
        FROM core.periodo AS pe
        CROSS JOIN core.programa AS pr
        WHERE pe."year" BETWEEN {year_start} AND {year_end}
        AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
        ORDER BY pe.id ASC, pr.id ASC
        """

    @staticmethod
    def get_reporte_resumen_grado(year_start: int, year_end: int, grado: str) -> str:
        """
        Reporte 2: Resumen por grado académico (LL/EL/ML)

        Args:
            year_start: Año inicial
            year_end: Año final
            grado: Grado académico (LL, EL, ML)

        Returns:
            Query SQL con totales por periodo y grado
        """
        return f"""
        SELECT
            pe.id AS "periodo_id",
            (
                SELECT count(*)
                FROM core.lista_asistencia AS la
                JOIN core.estudiante AS e ON la.estudiante_id = e.id
                JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
                WHERE la.periodo_id = pe.id
                AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
                AND ep.programa_id LIKE '{grado}%'
                AND ep.periodo_ingreso_id = pe.id
            ) AS "nuevo_ingreso",
            (
                SELECT count(*)
                FROM core.lista_asistencia AS la
                JOIN core.estudiante AS e ON la.estudiante_id = e.id
                JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
                WHERE la.periodo_id = pe.id
                AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
                AND ep.programa_id LIKE '{grado}%'
                AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
            ) AS "egresados",
            (
                SELECT count(*)
                FROM core.lista_asistencia AS la
                JOIN core.estudiante AS e ON la.estudiante_id = e.id
                JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
                JOIN core.titulado AS t ON (ep.estudiante_id, ep.programa_id) = (t.estudiante_id, t.programa_id)
                WHERE la.periodo_id = pe.id
                AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
                AND ep.programa_id LIKE '{grado}%'
                AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
            ) AS "titulados"
        FROM core.periodo AS pe
        WHERE pe."year" BETWEEN {year_start} AND {year_end}
        ORDER BY pe.id ASC
        """

    @staticmethod
    def get_estudiantes_nuevo_ingreso(year_start: int, year_end: int, grado: str) -> str:
        """
        Lista detallada de estudiantes de nuevo ingreso

        Args:
            year_start: Año inicial
            year_end: Año final
            grado: Grado académico (LL, EL, ML)

        Returns:
            Query SQL con listado de estudiantes nuevos
        """
        return f"""
        SELECT
            pr.campus,
            pe.id AS "periodo_id",
            e.id AS "estudiante_id",
            e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
            cga.descripcion AS "nivel",
            pr.id AS "programa_id",
            pr.escuela,
            pr.nombre || ' ' || pr.plan AS "programa",
            'NI' AS "tipo"
        FROM core.periodo AS pe
        JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        JOIN core.programa AS pr ON ep.programa_id = pr.id
        JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
        WHERE pe."year" BETWEEN {year_start} AND {year_end}
        AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.periodo_ingreso_id = pe.id
        AND ep.programa_id LIKE '{grado}%'
        ORDER BY pe.id ASC, pr.id ASC
        """

    @staticmethod
    def get_estudiantes_reinscritos(year_start: int, year_end: int, grado: str) -> str:
        """
        Lista detallada de estudiantes reinscritos

        Args:
            year_start: Año inicial
            year_end: Año final
            grado: Grado académico (LL, EL, ML)

        Returns:
            Query SQL con listado de estudiantes reinscritos
        """
        return f"""
        SELECT
            pr.campus,
            pe.id AS "periodo_id",
            e.id AS "estudiante_id",
            e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
            cga.descripcion AS "nivel",
            pr.id AS "programa_id",
            pr.escuela,
            pr.nombre || ' ' || pr.plan AS "programa",
            'REI' AS "tipo"
        FROM core.periodo AS pe
        JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        JOIN core.programa AS pr ON ep.programa_id = pr.id
        JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
        WHERE pe."year" BETWEEN {year_start} AND {year_end}
        AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.periodo_ingreso_id <> pe.id
        AND ep.programa_id LIKE '{grado}%'
        ORDER BY pe.id ASC, pr.id ASC
        """

    @staticmethod
    def get_todos_los_datos(year_start: int, year_end: int) -> str:
        """
        Obtiene todos los datos consolidados (equivalente a Hoja1)

        Returns:
            Query SQL con todos los datos históricos
        """
        return f"""
        SELECT
            pr.campus AS "Campus",
            pe.id AS "Periodo.de.consulta",
            e.id AS "ID",
            e.apellidos || ' ' || e.nombres AS "NOMBRE",
            cga.descripcion AS "NIVEL",
            pr.id AS "PROGRAMA",
            pr.escuela AS "ESCUELA",
            pr.nombre || ' ' || pr.plan AS "PROGRAMA_DESC"
        FROM core.periodo AS pe
        JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        JOIN core.programa AS pr ON ep.programa_id = pr.id
        JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
        WHERE pe."year" BETWEEN {year_start} AND {year_end}
        ORDER BY pe.id DESC, e.apellidos ASC
        """


class QueryBuilder:
    """Constructor de queries parametrizadas"""

    def __init__(self, year_start: int = 2021, year_end: int = 2025):
        self.year_start = year_start
        self.year_end = year_end

    def get_query(self, query_type: str, grado: Optional[str] = None) -> str:
        """
        Obtiene una query según el tipo solicitado

        Args:
            query_type: Tipo de query ('periodo_programa', 'resumen', 'nuevo_ingreso', 'reinscritos', 'todos')
            grado: Grado académico (LL, EL, ML) - requerido para algunas queries

        Returns:
            Query SQL formateada

        Raises:
            ValueError: Si el tipo de query no es válido
        """
        queries = TrayectoriaQueries()

        if query_type == 'periodo_programa':
            return queries.get_reporte_periodo_programa(self.year_start, self.year_end)

        elif query_type == 'resumen':
            if not grado:
                raise ValueError("Se requiere especificar el grado para query tipo 'resumen'")
            return queries.get_reporte_resumen_grado(self.year_start, self.year_end, grado)

        elif query_type == 'nuevo_ingreso':
            if not grado:
                raise ValueError("Se requiere especificar el grado para query tipo 'nuevo_ingreso'")
            return queries.get_estudiantes_nuevo_ingreso(self.year_start, self.year_end, grado)

        elif query_type == 'reinscritos':
            if not grado:
                raise ValueError("Se requiere especificar el grado para query tipo 'reinscritos'")
            return queries.get_estudiantes_reinscritos(self.year_start, self.year_end, grado)

        elif query_type == 'todos':
            return queries.get_todos_los_datos(self.year_start, self.year_end)

        else:
            raise ValueError(f"Tipo de query no válido: {query_type}")
