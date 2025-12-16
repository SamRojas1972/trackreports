# Hallazgos del Análisis Completo del Sistema

**Fecha**: 16 de Diciembre, 2025
**Análisis**: Flujo completo de generación de reportes (2024-2025)
**Reportes analizados**: 3 (Licenciatura, Especialidad, Maestría)

---

## Resumen Ejecutivo

Se ejecutó el flujo completo de generación de reportes para detectar errores, inconsistencias y posibles mejoras. El sistema generó exitosamente los 3 reportes en aproximadamente 2 minutos y 23 segundos.

### ✅ Aspectos Positivos

1. **Generación exitosa**: Los 3 reportes se generaron sin errores fatales
2. **Estructura completa**: Todos tienen las 5 hojas esperadas
3. **Queries corregidas**: No se detectaron duplicados en los conteos
4. **Rendimiento aceptable**: ~2.5 minutos para generar 3 reportes completos
5. **Datos extraídos**:
   - **LL**: 50 NI + 572 Reinscritos = 622 registros
   - **EL**: 1,302 NI + 15,873 Reinscritos = 17,175 registros
   - **ML**: 3,284 NI + 42,207 Reinscritos = 45,491 registros

---

## 🐛 Problemas Críticos Detectados

### 1. **Columna "program" con valor incorrecto ("No copiar. Formula.")**

**Problema**: La columna "program" contiene el texto literal "No copiar. Formula." en lugar del código de programa

**Ubicación**: Hojas NI y Reinscritos

**Valor actual**:
```
programa_id: ML-BIOG-18
program: No copiar. Formula.  ← ❌ INCORRECTO
```

**Valor esperado**:
```
programa_id: ML-BIOG-18
program: ML-BIOG  ← ✅ CORRECTO (sin últimos 3 caracteres)
```

**Impacto**:
- **CRÍTICO**: Columna inútil para análisis
- Pérdida de información importante
- No coincide con reportes originales

**Causa**:
En las queries de nuevo ingreso y reinscritos se puso un texto literal en lugar de calcular el valor:
```sql
'No copiar. Formula.' AS "program",  -- ❌ INCORRECTO
```

**Solución**:
```sql
-- Opción 1: Usar LEFT con LENGTH
LEFT(pr.id, LENGTH(pr.id) - 3) AS "program",

-- Opción 2: Usar SUBSTRING
SUBSTRING(pr.id, 1, LENGTH(pr.id) - 3) AS "program",

-- Opción 3: Usar regex_replace (más robusto)
REGEXP_REPLACE(pr.id, '-\d+$', '') AS "program",
```

**Archivos a modificar**:
- `src/backend/db/queries.py`:
  - `get_estudiantes_nuevo_ingreso()`
  - `get_estudiantes_reinscritos()`
- `config/queries.sql`: documentación de referencia

---

### 2. **Columnas sin nombres correctos (Unnamed: 1, Unnamed: 2, etc.)**

**Problema**: Todas las hojas tienen columnas con nombres genéricos "Unnamed: X"

**Ejemplo**:
```
Columnas (8):
   1. Datos Consolidados
   2. Unnamed: 1
   3. Unnamed: 2
   4. Unnamed: 3
   ...
```

**Impacto**:
- Dificulta la lectura programática de los archivos
- No coincide con los reportes originales
- Confusión para el usuario final

**Causa probable**:
- Los encabezados están en la segunda fila en lugar de la primera
- La primera fila contiene el título de la hoja, no los nombres de columnas

**Solución propuesta**:
```python
# En excel_generator.py, ajustar la escritura de encabezados
# Opción 1: Escribir título en una celda merged, encabezados en siguiente fila
# Opción 2: Usar startrow=1 para dejar espacio al título
```

---

### 3. **Primera fila con valores NaN (nulos)**

**Problema**: Todas las hojas tienen una primera fila completamente vacía (NaN)

**Evidencia**:
```
⚠️  Valores nulos encontrados:
   Datos Consolidados: 1 (0.0%)
   Unnamed: 1: 1 (0.0%)
   Unnamed: 2: 1 (0.0%)
   ...
```

**Impacto**:
- Genera una fila vacía al leer con pandas/openpyxl
- Desperdicia espacio en el archivo
- Puede causar errores en procesamiento automatizado

**Solución propuesta**:
```python
# Revisar el método de escritura en excel_generator.py
# Asegurar que no se escriba una fila vacía inicial
```

---

### 4. **Hoja1 (Datos Consolidados) contiene TODOS los datos**

**Problema**: La Hoja1 tiene 114,171 filas PARA TODOS LOS GRADOS

**Evidencia**:
- Licenciatura: 114,171 filas (debería tener ~50-600)
- Especialidad: 114,171 filas (debería tener ~17,000)
- Maestría: 114,171 filas (debería tener ~45,000)

**Impacto**:
- **CRÍTICO**: Los datos no están filtrados por grado
- Los reportes incluyen datos de otros grados académicos
- Tamaño de archivo innecesariamente grande
- Confusión total para el usuario final

**Causa**:
La query `get_todos_los_datos()` NO filtra por grado académico

**Verificación en queries.py**:
```python
def get_todos_los_datos(year_start: int, year_end: int) -> str:
    # ❌ NO tiene filtro por grado
    # Falta: AND pr.id LIKE '{grado}%'
```

**Solución**:
```python
# 1. Modificar get_todos_los_datos() para aceptar parámetro 'grado'
# 2. Agregar filtro: AND pr.id LIKE '{grado}%'
# 3. Actualizar llamadas en extractor.py
```

---

### 5. **Cuadro FIMPES con columnas vacías (94.4% nulos)**

**Problema**: Las columnas "Unnamed: 3" y "Unnamed: 5" tienen 94.4% de valores nulos

**Evidencia**:
```
⚠️  Valores nulos encontrados:
   Unnamed: 3: 17 (94.4%)
   Unnamed: 5: 17 (94.4%)
```

**Impacto**:
- Columnas vacías ocupan espacio
- Formato inconsistente
- Posible error en la lógica de transformación

**Causa probable**:
- Columnas calculadas que no tienen datos suficientes
- Fórmulas o cálculos que no se ejecutan correctamente
- Estructura del dataframe mal definida

**Solución propuesta**:
```python
# Revisar transformer.py -> crear_cuadro_fimpes()
# Verificar la creación de todas las columnas
# Eliminar columnas innecesarias o llenarlas con valores por defecto
```

---

### 6. **Estructura de headers incorrecta**

**Problema**: Los encabezados reales están en la segunda fila

**Evidencia al leer con pandas**:
```
Primeras 3 filas:
Datos Consolidados    Unnamed: 1     Unnamed: 2
              NaN           NaN            NaN
           Campus Periodo.de.consulta         ID
       México Sur            202592       00599407
```

**Formato esperado**:
```
Campus  Periodo.de.consulta  ID
México Sur  202592  00599407
```

**Impacto**:
- Herramientas de análisis de datos leen incorrectamente
- pandas requiere `header=1` o `skiprows=1`
- No es user-friendly

**Solución propuesta**:
```python
# Ajustar excel_generator.py para:
# 1. Usar to_excel con parámetro startrow correcto
# 2. Escribir título en merged cell arriba
# 3. O eliminar la fila de título completamente
```

---

## ⚠️ Inconsistencias Detectadas

### 7. **Hojas "Resumen" sin estadísticas mostradas**

**Problema**: El script de análisis no pudo extraer las columnas esperadas

**Evidencia**:
```python
📊 Estadísticas de Resumen:
# ← Vacío, no se encontraron columnas nuevo_ingreso, egresados, titulados
```

**Causa**: Columnas tienen nombres "Unnamed" en lugar de sus nombres reales

**Impacto medio**: Dificulta validación automática

---

### 8. **Todos los reportes muestran el mismo periodo en Hoja1**

**Observación**: Todos los reportes tienen periodo 202592 en la tercera fila

**Evidencia**:
```
México Sur    202592    00599407
```

**¿Es correcto?**: Necesita validación con usuario
- ¿Es el periodo más reciente?
- ¿Debería ordenarse diferente?

---

## 💡 Mejoras Propuestas

### 9. **Mejorar nombres de hojas**

**Actual**: `Hoja1`, `NI`, `Reinscritos`

**Propuesta**:
```python
'Datos Consolidados'  # En lugar de 'Hoja1'
'Nuevo Ingreso'       # En lugar de 'NI'
'Estudiantes Reinscritos'  # En lugar de 'Reinscritos'
```

**Beneficio**: Más descriptivo y profesional

---

### 10. **Optimizar tamaño de archivos**

**Actual**:
- LL: 6.0 MB (pero con 114K filas incorrectas)
- EL: 6.9 MB
- ML: 8.6 MB

**Propuesta**:
1. Filtrar Hoja1 por grado → reducirá tamaño ~90%
2. Eliminar columnas vacías en Cuadro FIMPES
3. Usar compresión de Excel si es posible

**Beneficio esperado**:
- LL: ~600 KB (reducción 90%)
- EL: ~2 MB (reducción 70%)
- ML: ~5 MB (reducción 40%)

---

### 11. **Agregar validación de datos**

**Propuesta**: Crear script de validación post-generación

```python
def validar_reporte(file_path, grado):
    """Valida que el reporte cumple con requisitos básicos"""

    # 1. Verificar 5 hojas
    # 2. Verificar que Hoja1 solo tiene datos del grado
    # 3. Verificar sin duplicados
    # 4. Verificar columnas esperadas
    # 5. Verificar sin filas vacías

    return {
        'valido': True/False,
        'errores': [...],
        'advertencias': [...]
    }
```

**Beneficio**: Detectar errores antes de entregar reportes

---

### 12. **Mejorar logging de generación**

**Actual**:
```
Query 'Nuevo Ingreso LL' completada: 50 filas en 0.11s
```

**Propuesta adicional**:
```
Query 'Nuevo Ingreso LL' completada: 50 filas (esperadas: 40-60) ✅ en 0.11s
```

**Beneficio**: Detectar anomalías en los datos

---

### 13. **Agregar metadata al archivo Excel**

**Propuesta**: Usar openpyxl.properties para agregar:
```python
wb.properties.title = f"Reporte Trayectoria {grado_nombre}"
wb.properties.subject = "Trayectoria Académica"
wb.properties.creator = "Sistema Automatizado - Claude Code"
wb.properties.description = f"Periodo {year_start}-{year_end}"
wb.properties.created = datetime.now()
```

**Beneficio**: Profesionalismo y trazabilidad

---

### 14. **Implementar caché de queries grandes**

**Observación**: La query "Todos los Datos" tarda ~2.25s y se ejecuta 3 veces con el mismo resultado (114,169 filas)

**Propuesta**:
```python
# Ejecutar una vez y cachear
todos_datos_cache = None

def get_todos_datos():
    global todos_datos_cache
    if todos_datos_cache is None:
        todos_datos_cache = db.execute_query(...)
    return todos_datos_cache
```

**Beneficio**: Reducir tiempo de generación de ~7s a ~2.5s (70% más rápido)

---

## 📊 Estadísticas del Análisis

### Rendimiento

| Métrica | Valor |
|---------|-------|
| Tiempo total de generación | 2 min 23 seg |
| Reportes generados | 3/3 (100%) |
| Queries ejecutadas | 15 queries |
| Datos procesados | 405,843 filas totales |
| Tamaño total archivos | 21.5 MB |

### Conteos por Grado

| Grado | Nuevo Ingreso | Reinscritos | Total Estudiantes | Hoja1 (actual) |
|-------|---------------|-------------|-------------------|----------------|
| LL    | 50            | 572         | 622               | 114,171 ❌ |
| EL    | 1,302         | 15,873      | 17,175            | 114,171 ❌ |
| ML    | 3,284         | 42,207      | 45,491            | 114,171 ❌ |
| **Total** | **4,636** | **58,652** | **63,288** | **342,513** |

**Nota**: Los datos de Hoja1 están incorrectos y deben corregirse.

---

## 🎯 Prioridades de Corrección

### Prioridad ALTA (Crítico)

1. ✅ **Corregir columna "program" en hojas NI y Reinscritos** (Problema #1)
   - Cambiar `'No copiar. Formula.'` por cálculo real
   - Usar: `LEFT(pr.id, LENGTH(pr.id) - 3)` o `REGEXP_REPLACE(pr.id, '-\d+$', '')`
   - Ejemplo: ML-BIOG-18 → ML-BIOG

2. ✅ **Corregir filtro de Hoja1 por grado académico** (Problema #4)
   - Modificar `queries.py::get_todos_los_datos()`
   - Agregar parámetro `grado`
   - Probar con los 3 grados

3. ✅ **Arreglar estructura de encabezados** (Problemas #2, #3 y #6)
   - Revisar `excel_generator.py`
   - Eliminar fila vacía inicial
   - Asegurar nombres correctos de columnas

### Prioridad MEDIA

4. 🔍 **Corregir Cuadro FIMPES** (Problema #5)
   - Revisar `transformer.py::crear_cuadro_fimpes()`
   - Verificar todas las columnas
   - Eliminar columnas vacías

5. 🔍 **Implementar validación post-generación** (Mejora #11)

### Prioridad BAJA (Nice to have)

6. 💡 Mejorar nombres de hojas (Mejora #9)
7. 💡 Agregar metadata (Mejora #13)
8. 💡 Optimizar con caché (Mejora #14)

---

## 📝 Próximos Pasos Recomendados

1. **Inmediato**:
   - Corregir columna "program" en queries de NI y Reinscritos
   - Corregir filtro de `get_todos_los_datos()` para incluir grado
   - Arreglar estructura de headers en Excel
   - Regenerar reportes y validar

2. **Corto plazo**:
   - Revisar y corregir Cuadro FIMPES
   - Crear script de validación automática
   - Comparar con reportes originales del usuario

3. **Mediano plazo**:
   - Optimizar rendimiento con caché
   - Mejorar logging y monitoreo
   - Documentar formato esperado de cada hoja

---

## ✅ Conclusión

El sistema está **funcionalmente operativo** pero requiere **correcciones críticas** en:
1. Columna "program" con texto en lugar de cálculo
2. Filtrado de datos por grado (Hoja1)
3. Estructura de encabezados Excel

Una vez corregidos estos 3 puntos críticos, el sistema estará listo para producción.

**Tiempo estimado de corrección**: 45-90 minutos

---

**Generado por**: Claude Code Analysis
**Última actualización**: 2025-12-16
