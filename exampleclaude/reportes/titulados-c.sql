-- CORREGIDO SIN ESTUDIANTES REPETIDOS.

-- HECHO Reporte 1
SELECT
    pe.id AS "periodo_id",
    pr.id AS "programa_id",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id = pr.id
        AND ep.periodo_ingreso_id = pe.id
    ) AS "nuevo_ingreso",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id = pr.id
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "egresados",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        JOIN core.titulado AS t ON (ep.estudiante_id, ep.programa_id) = (t.estudiante_id, t.programa_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id = pr.id
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "titulados"
FROM core.periodo AS pe
CROSS JOIN core.programa AS pr
WHERE pe."year" BETWEEN 2021 AND 2024
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
ORDER BY pe.id ASC, pr.id ASC
;

-- HECHO Reporte 2 LL
SELECT
    pe.id AS "periodo_id",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'LL%'
        AND ep.periodo_ingreso_id = pe.id
    ) AS "nuevo_ingreso",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'LL%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "egresados",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        JOIN core.titulado AS t ON (ep.estudiante_id, ep.programa_id) = (t.estudiante_id, t.programa_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'LL%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "titulados"
FROM core.periodo AS pe
WHERE pe."year" BETWEEN 2021 AND 2024
ORDER BY pe.id ASC
;

-- HECHO Reporte 2 EL
SELECT
    pe.id AS "periodo_id",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'EL%'
        AND ep.periodo_ingreso_id = pe.id
    ) AS "nuevo_ingreso",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'EL%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "egresados",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        JOIN core.titulado AS t ON (ep.estudiante_id, ep.programa_id) = (t.estudiante_id, t.programa_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'EL%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "titulados"
FROM core.periodo AS pe
WHERE pe."year" BETWEEN 2021 AND 2024
ORDER BY pe.id ASC
;

-- HECHO Reporte 2 ML
SELECT
    pe.id AS "periodo_id",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'ML%'
        AND ep.periodo_ingreso_id = pe.id
    ) AS "nuevo_ingreso",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'ML%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "egresados",
    (
        SELECT count( DISTINCT la.estudiante_id )
        FROM core.lista_asistencia AS la
        JOIN core.estudiante AS e ON la.estudiante_id = e.id
        JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
        JOIN core.titulado AS t ON (ep.estudiante_id, ep.programa_id) = (t.estudiante_id, t.programa_id)
        WHERE la.periodo_id = pe.id AND ep.programa_id IN (SELECT clave_programa FROM core.programas_titulados)
        AND ep.programa_id LIKE 'ML%'
        AND ep.periodo_ingreso_id = pe.id AND ep.estatus_academico_id = 'EG'
    ) AS "titulados"
FROM core.periodo AS pe
WHERE pe."year" BETWEEN 2021 AND 2024
ORDER BY pe.id ASC
;

-- HECHO Trayectoria online LL NI
SELECT DISTINCT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.',
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'NI'
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2024
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id = pe.id
AND ep.programa_id LIKE 'LL%'
ORDER BY pe.id ASC, pr.id ASC
;

-- HECHO Trayectoria online LL Reinscritos
SELECT DISTINCT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.',
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'REI'
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2024
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id <> pe.id
AND ep.programa_id LIKE 'LL%'
ORDER BY pe.id ASC, pr.id ASC
;

-- HECHO Trayectoria online EL NI
SELECT DISTINCT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.',
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'NI'
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2024
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id = pe.id
AND ep.programa_id LIKE 'EL%'
ORDER BY pe.id ASC, pr.id ASC
;

-- HECHO Trayectoria online EL Reinscritos
SELECT DISTINCT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.',
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'REI'
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2024
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id <> pe.id
AND ep.programa_id LIKE 'EL%'
ORDER BY pe.id ASC, pr.id ASC
;

-- HECHO Trayectoria online ML NI
SELECT DISTINCT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.',
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'NI'
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2024
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id = pe.id
AND ep.programa_id LIKE 'ML%'
ORDER BY pe.id ASC, pr.id ASC
;

-- Trayectoria online ML Reinscritos
SELECT DISTINCT
    pr.campus,
    pe.id AS "periodo_id",
    e.id AS "estudiante_id",
    e.apellidos || ' ' || e.nombres AS "estudiante_nombre",
    cga.descripcion AS "nivel",
    pr.id AS "programa_id",
    'No copiar. Formula.',
    pr.escuela,
    pr.nombre || ' ' || pr.plan AS "programa",
    'REI'
FROM core.periodo AS pe
JOIN core.lista_asistencia AS la ON pe.id = la.periodo_id
JOIN core.estudiante AS e ON la.estudiante_id = e.id
JOIN core.estudiante_programa AS ep ON (e.id) = (ep.estudiante_id)
JOIN core.programa AS pr ON ep.programa_id = pr.id
JOIN core.cat_grado_academico AS cga ON pr.grado_academico_id = cga.id
WHERE pe."year" BETWEEN 2021 AND 2024
AND pr.id IN (SELECT clave_programa FROM core.programas_titulados)
AND ep.periodo_ingreso_id <> pe.id
AND ep.programa_id LIKE 'ML%'
ORDER BY pe.id ASC, pr.id ASC
;
