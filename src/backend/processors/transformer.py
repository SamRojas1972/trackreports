"""
Módulo de transformación de datos para reportes
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional

from src.utils.logger import get_logger
from src.utils.config import config


logger = get_logger(__name__, config.paths.logs_dir)


class TrayectoriaTransformer:
    """Transformador de datos para análisis de trayectoria"""

    def create_trayectoria_table(
        self,
        df_nuevo_ingreso: pd.DataFrame,
        df_reinscritos: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Crea tabla de trayectoria con seguimiento por cohorte

        Args:
            df_nuevo_ingreso: DataFrame con estudiantes de nuevo ingreso
            df_reinscritos: DataFrame con estudiantes reinscritos

        Returns:
            DataFrame con trayectoria por generación (P1, P2, P3, etc.)
        """
        logger.info("Creando tabla de trayectoria")

        try:
            # Combinar ambos dataframes
            df_all = pd.concat([df_nuevo_ingreso, df_reinscritos], ignore_index=True)

            if df_all.empty:
                logger.warning("No hay datos para crear tabla de trayectoria")
                return pd.DataFrame()

            # Extraer año y número de periodo
            df_all['periodo_id'] = df_all['periodo_id'].astype(str)
            df_all['año'] = df_all['periodo_id'].str[:4].astype(int)
            df_all['num_periodo'] = df_all['periodo_id'].str[4:].astype(int)

            # Identificar generación (periodo de ingreso)
            estudiantes_ingreso = df_all[df_all['tipo'] == 'NI'][['estudiante_id', 'periodo_id']].copy()
            estudiantes_ingreso.rename(columns={'periodo_id': 'generacion'}, inplace=True)
            estudiantes_ingreso = estudiantes_ingreso.drop_duplicates('estudiante_id')

            # Merge para agregar generación a todos los registros
            df_all = df_all.merge(estudiantes_ingreso, on='estudiante_id', how='left')

            # Filtrar solo registros con generación válida (excluir NaN)
            df_all = df_all[df_all['generacion'].notna()].copy()

            # Calcular número de periodo desde ingreso
            df_all['generacion_año'] = df_all['generacion'].str[:4].astype(int)
            df_all['generacion_num'] = df_all['generacion'].str[4:].astype(int)

            # Calcular periodos transcurridos
            df_all['periodos_desde_ingreso'] = (
                (df_all['año'] - df_all['generacion_año']) * 10 +
                (df_all['num_periodo'] - df_all['generacion_num'])
            )

            # Crear tabla pivote por generación
            generaciones = sorted(df_all['generacion'].dropna().unique())

            # Calcular el número máximo de periodos necesarios (matriz cuadrada)
            # El número de columnas debe ser igual al número de generaciones
            max_periodos = len(generaciones)

            rows = []
            for gen in generaciones:
                df_gen = df_all[df_all['generacion'] == gen]

                row = {'Generación': gen}

                # Contar estudiantes únicos por periodo (matriz cuadrada)
                for p in range(0, max_periodos):  # De 0 (nuevo ingreso) hasta max_periodos-1
                    estudiantes_en_periodo = df_gen[
                        df_gen['periodos_desde_ingreso'] == p
                    ]['estudiante_id'].nunique()

                    if p == 0:
                        row['Nuevo ingreso'] = estudiantes_en_periodo
                    else:
                        row[f'P{p+1}'] = estudiantes_en_periodo

                rows.append(row)

            df_trayectoria = pd.DataFrame(rows)

            # Rellenar NaN con 0
            df_trayectoria = df_trayectoria.fillna(0)

            # Convertir columna Generación a string
            df_trayectoria['Generación'] = df_trayectoria['Generación'].astype(str)

            # Convertir conteos a int
            for col in df_trayectoria.columns:
                if col != 'Generación':
                    df_trayectoria[col] = df_trayectoria[col].astype(int)

            logger.info(f"Tabla de trayectoria creada: {len(df_trayectoria)} generaciones")

            return df_trayectoria

        except Exception as e:
            logger.error(f"Error creando tabla de trayectoria: {e}")
            raise

    def create_cuadro_fimpes(self, df_trayectoria: pd.DataFrame) -> pd.DataFrame:
        """
        Crea cuadro de indicadores FIMPES

        Args:
            df_trayectoria: DataFrame con trayectoria por generación

        Returns:
            DataFrame con indicadores FIMPES
        """
        logger.info("Creando cuadro FIMPES")

        try:
            if df_trayectoria.empty:
                return pd.DataFrame()

            df_fimpes = df_trayectoria.copy()

            # Renombrar primera columna
            df_fimpes.rename(columns={'Generación': 'Cohorte'}, inplace=True)

            # Calcular métricas FIMPES
            if 'Nuevo ingreso' in df_fimpes.columns:
                df_fimpes['Alumnos de Nuevo Ingreso'] = df_fimpes['Nuevo ingreso']

            # Eficiencia de retención 1er año (P2 / Nuevo Ingreso)
            if 'P2' in df_fimpes.columns and 'Nuevo ingreso' in df_fimpes.columns:
                df_fimpes['Eficiencia de retención 1er año'] = (
                    df_fimpes['P2'] / df_fimpes['Nuevo ingreso'].replace(0, np.nan)
                ).round(4)

            # Abandono (calculado posteriormente con más datos)
            df_fimpes['Abandono'] = None

            # Activos (última columna P disponible)
            p_cols = [col for col in df_fimpes.columns if col.startswith('P')]
            if p_cols:
                ultima_p = p_cols[-1]
                df_fimpes['Activo '] = df_fimpes[ultima_p]

            # Cambios de carrera (requiere datos adicionales)
            df_fimpes['Cambios de carrera'] = None

            # Rezago (estudiantes que continúan / nuevo ingreso)
            if 'Activo ' in df_fimpes.columns and 'Nuevo ingreso' in df_fimpes.columns:
                df_fimpes['% Rezago'] = (
                    df_fimpes['Activo '] / df_fimpes['Nuevo ingreso'].replace(0, np.nan)
                ).round(4)

            # Egresados (aproximación: último periodo con datos)
            if p_cols and len(p_cols) >= 6:
                df_fimpes['Egresados'] = df_fimpes['P6']
            else:
                df_fimpes['Egresados'] = 0

            # Seleccionar solo columnas FIMPES
            fimpes_cols = [
                'Cohorte',
                'Alumnos de Nuevo Ingreso',
                'Eficiencia de retención 1er año',
                'Abandono',
                'Activo ',
                'Cambios de carrera',
                '% Rezago',
                'Egresados'
            ]

            df_fimpes = df_fimpes[[col for col in fimpes_cols if col in df_fimpes.columns]]

            logger.info(f"Cuadro FIMPES creado: {len(df_fimpes)} cohortes")

            return df_fimpes

        except Exception as e:
            logger.error(f"Error creando cuadro FIMPES: {e}")
            raise

    def aggregate_by_programa(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Agrega datos por programa

        Args:
            df: DataFrame con datos individuales

        Returns:
            DataFrame agregado por programa
        """
        if 'programa_id' not in df.columns:
            logger.warning("No se encontró columna 'programa_id' para agregación")
            return df

        agg_cols = {
            'estudiante_id': 'count'
        }

        df_agg = df.groupby(['programa_id', 'periodo_id']).agg(agg_cols).reset_index()
        df_agg.rename(columns={'estudiante_id': 'total_estudiantes'}, inplace=True)

        return df_agg

    def calculate_retention_metrics(self, df_trayectoria: pd.DataFrame) -> Dict:
        """
        Calcula métricas de retención

        Args:
            df_trayectoria: DataFrame con trayectoria

        Returns:
            Diccionario con métricas agregadas
        """
        metrics = {}

        if df_trayectoria.empty:
            return metrics

        try:
            # Retención promedio P1 a P2
            if 'Nuevo ingreso' in df_trayectoria.columns and 'P2' in df_trayectoria.columns:
                mask = df_trayectoria['Nuevo ingreso'] > 0
                retention = (
                    df_trayectoria.loc[mask, 'P2'] /
                    df_trayectoria.loc[mask, 'Nuevo ingreso']
                )
                metrics['retention_p1_p2_avg'] = retention.mean()
                metrics['retention_p1_p2_median'] = retention.median()

            # Total de ingresos
            if 'Nuevo ingreso' in df_trayectoria.columns:
                metrics['total_nuevo_ingreso'] = df_trayectoria['Nuevo ingreso'].sum()

            # Total de egresados
            if 'P6' in df_trayectoria.columns:
                metrics['total_egresados_p6'] = df_trayectoria['P6'].sum()

            logger.info(f"Métricas de retención calculadas: {len(metrics)} indicadores")

        except Exception as e:
            logger.error(f"Error calculando métricas de retención: {e}")

        return metrics


def test_transformer():
    """Función de prueba para el transformer"""
    logger.info("=== Iniciando test de transformer ===")

    # Datos de ejemplo
    df_ni = pd.DataFrame({
        'estudiante_id': [1, 2, 3, 4, 5],
        'periodo_id': ['202101', '202101', '202102', '202102', '202201'],
        'tipo': ['NI'] * 5
    })

    df_rei = pd.DataFrame({
        'estudiante_id': [1, 1, 2, 3, 3, 4],
        'periodo_id': ['202102', '202201', '202102', '202201', '202202', '202201'],
        'tipo': ['REI'] * 6
    })

    transformer = TrayectoriaTransformer()

    # Test trayectoria
    df_tray = transformer.create_trayectoria_table(df_ni, df_rei)
    print("\nTabla de Trayectoria:")
    print(df_tray)

    # Test FIMPES
    df_fimpes = transformer.create_cuadro_fimpes(df_tray)
    print("\nCuadro FIMPES:")
    print(df_fimpes)

    # Test métricas
    metrics = transformer.calculate_retention_metrics(df_tray)
    print("\nMétricas:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")

    logger.info("=== Test completado ===")


if __name__ == "__main__":
    test_transformer()
