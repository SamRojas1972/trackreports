-- ============================================================================
-- GUÍA DE QUERIES SQL - Sistema de Reportes de Trayectoria
-- ============================================================================
--
-- Este archivo documenta todas las queries SQL utilizadas en el sistema
-- Basado en: exampleclaude/reportes/titulados.sql
-- Schema: core
--
-- ============================================================================

-- ============================================================================
-- REPORTE 1: Datos por Periodo y Programa
-- ============================================================================
-- Descripción: Obtiene nuevo ingreso, egresados y titulados por periodo/programa
-- Uso: Hoja de resumen general
-- Parámetros: {year_start}, {year_end}
-- ============================================================================

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
WHERE pe."year" BETWEEN 2021 AND 2025
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
ORDER BY pe.id ASC, pr.id ASC;


-- ============================================================================
-- REPORTE 2: Resumen por Grado Académico (LL - Licenciatura)
-- ============================================================================
-- Descripción: Totales por periodo para Licenciatura en Línea
-- Uso: Hoja "Resumen" en Trayectoria online LL.xlsb
-- Parámetros: {year_start}, {year_end}
-- ============================================================================

SELECT
    pe.id AS "periodo_id",
    (
        SELECT count(*)
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'LL%'
        AND ep.periodo_ingreso_id = pe.id
    ) AS "nuevo_ingreso",
    (
        SELECT count(*)
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'LL%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "egresados",
    (
        SELECT count(*)
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        JOIN core.titulado AS t ON (ep.estudiante_id, ep.programa_id) = (t.estudiante_id, t.programa_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'LL%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "titulados"
FROM core.periodo AS pe
WHERE pe."year" BETWEEN 2021 AND 2025
ORDER BY pe.id ASC;


-- ============================================================================
-- REPORTE 2: Resumen por Grado Académico (EL - Especialidad)
-- ============================================================================
-- Descripción: Totales por periodo para Especialidad en Línea
-- Uso: Hoja "Resumen" en Trayectoria online EL.xlsb
-- Parámetros: {year_start}, {year_end}
-- ============================================================================

SELECT
    pe.id AS "periodo_id",
    (
        SELECT count(*)
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'EL%'
        AND ep.periodo_ingreso_id = pe.id
    ) AS "nuevo_ingreso",
    (
        SELECT count(*)
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'EL%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "egresados",
    (
        SELECT count(*)
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        JOIN core.titulado AS t ON (ep.estudiante_id, ep.programa_id) = (t.estudiante_id, t.programa_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'EL%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "titulados"
FROM core.periodo AS pe
WHERE pe."year" BETWEEN 2021 AND 2025
ORDER BY pe.id ASC;


-- ============================================================================
-- REPORTE 2: Resumen por Grado Académico (ML - Maestría)
-- ============================================================================
-- Descripción: Totales por periodo para Maestría en Línea
-- Uso: Hoja "Resumen" en Trayectoria online ML.xlsb
-- Parámetros: {year_start}, {year_end}
-- ============================================================================

SELECT
    pe.id AS "periodo_id",
    (
        SELECT count(*)
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'ML%'
        AND ep.periodo_ingreso_id = pe.id
    ) AS "nuevo_ingreso",
    (
        SELECT count(*)
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'ML%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "egresados",
    (
        SELECT count(*)
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        JOIN core.titulado AS t ON (ep.estudiante_id, ep.programa_id) = (t.estudiante_id, t.programa_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'ML%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "titulados"
FROM core.periodo AS pe
WHERE pe."year" BETWEEN 2021 AND 2025
ORDER BY pe.id ASC;


-- ============================================================================
-- REPORTE 3: Estudiantes de Nuevo Ingreso (LL - Licenciatura)
-- ============================================================================
-- Descripción: Listado detallado de estudiantes de nuevo ingreso
-- Uso: Hoja "NI" en Trayectoria online LL.xlsb
-- Parámetros: {year_start}, {year_end}
-- ============================================================================

SELECT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.' AS "placeholder_formula",
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'NI' AS "tipo"
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2025
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id = pe.id
AND ep.programa_id LIKE 'LL%'
ORDER BY pe.id ASC, pr.id ASC;


-- ============================================================================
-- REPORTE 3: Estudiantes de Nuevo Ingreso (EL - Especialidad)
-- ============================================================================
-- Descripción: Listado detallado de estudiantes de nuevo ingreso
-- Uso: Hoja "NI" en Trayectoria online EL.xlsb
-- Parámetros: {year_start}, {year_end}
-- ============================================================================

SELECT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.' AS "placeholder_formula",
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'NI' AS "tipo"
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2025
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id = pe.id
AND ep.programa_id LIKE 'EL%'
ORDER BY pe.id ASC, pr.id ASC;


-- ============================================================================
-- REPORTE 3: Estudiantes de Nuevo Ingreso (ML - Maestría)
-- ============================================================================
-- Descripción: Listado detallado de estudiantes de nuevo ingreso
-- Uso: Hoja "NI" en Trayectoria online ML.xlsb
-- Parámetros: {year_start}, {year_end}
-- ============================================================================

SELECT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.' AS "placeholder_formula",
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'NI' AS "tipo"
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2025
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id = pe.id
AND ep.programa_id LIKE 'ML%'
ORDER BY pe.id ASC, pr.id ASC;


-- ============================================================================
-- REPORTE 4: Estudiantes Reinscritos (LL - Licenciatura)
-- ============================================================================
-- Descripción: Listado detallado de estudiantes reinscritos (no nuevo ingreso)
-- Uso: Hoja "Reinscritos" en Trayectoria online LL.xlsb
-- Parámetros: {year_start}, {year_end}
-- Condición clave: ep.periodo_ingreso_id <> pe.id
-- ============================================================================

SELECT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.' AS "placeholder_formula",
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'REI' AS "tipo"
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2025
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id <> pe.id
AND ep.programa_id LIKE 'LL%'
ORDER BY pe.id ASC, pr.id ASC;


-- ============================================================================
-- REPORTE 4: Estudiantes Reinscritos (EL - Especialidad)
-- ============================================================================
-- Descripción: Listado detallado de estudiantes reinscritos (no nuevo ingreso)
-- Uso: Hoja "Reinscritos" en Trayectoria online EL.xlsb
-- Parámetros: {year_start}, {year_end}
-- ============================================================================

SELECT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.' AS "placeholder_formula",
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'REI' AS "tipo"
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2025
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id <> pe.id
AND ep.programa_id LIKE 'EL%'
ORDER BY pe.id ASC, pr.id ASC;


-- ============================================================================
-- REPORTE 4: Estudiantes Reinscritos (ML - Maestría)
-- ============================================================================
-- Descripción: Listado detallado de estudiantes reinscritos (no nuevo ingreso)
-- Uso: Hoja "Reinscritos" en Trayectoria online ML.xlsb
-- Parámetros: {year_start}, {year_end}
-- ============================================================================

SELECT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.' AS "placeholder_formula",
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'REI' AS "tipo"
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2025
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id <> pe.id
AND ep.programa_id LIKE 'ML%'
ORDER BY pe.id ASC, pr.id ASC;


-- ============================================================================
-- REPORTE 5: Datos Consolidados Completos (Hoja1)
-- ============================================================================
-- Descripción: Todos los datos históricos consolidados
-- Uso: Hoja "Hoja1" en todos los reportes Excel
-- Parámetros: {year_start}, {year_end}
-- Nota: Esta query retorna ~5000 registros
-- ============================================================================

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
WHERE pe."year" BETWEEN 2021 AND 2025
ORDER BY pe.id DESC, e.apellidos ASC;


-- ============================================================================
-- QUERIES AUXILIARES
-- ============================================================================

-- Listar periodos disponibles
-- ----------------------------------------------------------------------------
SELECT DISTINCT
    id,
    "year",
    descripcion
FROM core.periodo
WHERE "year" BETWEEN 2021 AND 2025
ORDER BY id;


-- Listar programas disponibles
-- ----------------------------------------------------------------------------
SELECT DISTINCT
    id,
    nombre,
    plan,
    escuela,
    campus,
    grado_academico_id
FROM core.programa
WHERE id IN (SELECT clave_programa FROM core.programas_titulados)
ORDER BY id;


-- Listar programas por grado académico
-- ----------------------------------------------------------------------------
SELECT DISTINCT
    id,
    nombre,
    plan,
    escuela,
    campus,
    grado_academico_id
FROM core.programa
WHERE id IN (SELECT clave_programa FROM core.programas_titulados)
AND id LIKE 'LL%'  -- Cambiar por 'EL%' o 'ML%' según necesidad
ORDER BY id;


-- Contar estudiantes por periodo
-- ----------------------------------------------------------------------------
SELECT
    pe.id AS periodo,
    COUNT(DISTINCT e.id) AS total_estudiantes
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
WHERE pe."year" BETWEEN 2021 AND 2025
GROUP BY pe.id
ORDER BY pe.id;


-- Contar estudiantes por programa
-- ----------------------------------------------------------------------------
SELECT
    pr.id AS programa,
    pr.nombre,
    COUNT(DISTINCT e.id) AS total_estudiantes
FROM core.programa AS pr
JOIN core.estudiante_programa AS ep ON pr.id = ep.programa_id
JOIN core.estudiante AS e ON ep.estudiante_id = e.id
WHERE pr.id IN (SELECT clave_programa FROM core.programas_titulados)
GROUP BY pr.id, pr.nombre
ORDER BY total_estudiantes DESC;


-- ============================================================================
-- NOTAS IMPORTANTES
-- ============================================================================
--
-- 1. GRADOS ACADÉMICOS:
--    - LL: Licenciatura en Línea
--    - EL: Especialidad en Línea
--    - ML: Maestría en Línea
--
-- 2. ESTATUS ACADÉMICOS:
--    - 'EG': Egresado
--    - Otros valores según catálogo institucional
--
-- 3. TIPOS DE ESTUDIANTE:
--    - 'NI': Nuevo Ingreso (ep.periodo_ingreso_id = pe.id)
--    - 'REI': Reinscrito (ep.periodo_ingreso_id <> pe.id)
--
-- 4. FORMATO DE PERIODOS:
--    - Formato: YYYYPP (ej: 202461)
--    - YYYY: Año (ej: 2024)
--    - PP: Número de periodo (ej: 61, 11, 32)
--
-- 5. TABLAS PRINCIPALES:
--    - core.periodo: Periodos académicos
--    - core.programa: Programas académicos
--    - core.estudiante: Datos de estudiantes
--    - core.estudiante_programa: Relación estudiante-programa
--    - core.lista_asistencia: Inscripciones por periodo
--    - core.titulado: Estudiantes titulados
--    - core.cat_grado_academico: Catálogo de grados
--    - core.programas_titulados: Programas que se consideran para reportes
--
-- 6. OPTIMIZACIONES SUGERIDAS:
--    - Crear índices en: periodo.year, programa.id, estudiante_programa.programa_id
--    - Considerar materializar core.programas_titulados si es una vista
--    - Evaluar particionamiento de lista_asistencia por periodo
--
-- 7. USO EN EL SISTEMA:
--    - Todas estas queries están implementadas en: src/backend/db/queries.py
--    - Se ejecutan mediante: src/backend/processors/extractor.py
--    - Los resultados se transforman en: src/backend/processors/transformer.py
--    - Los reportes se generan en: src/backend/processors/excel_generator.py
--
-- ============================================================================
-- Última actualización: Diciembre 2024
-- Versión: 1.0
-- ============================================================================
