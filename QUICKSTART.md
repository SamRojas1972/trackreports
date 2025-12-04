# Guía Rápida de Inicio

Esta guía te ayudará a configurar y ejecutar el sistema en menos de 10 minutos.

## 1. Pre-requisitos

Asegúrate de tener instalado:

- Python 3.11 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

## 2. Instalación Rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales de PostgreSQL
```

## 3. Configuración Básica

Edita el archivo `.env` con tus datos:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_SCHEMA=core
```

## 4. Verificar Conexión

```bash
python main.py --test-connection
```

Deberías ver: ✅ Conexión exitosa!

## 5. Generar tu Primer Reporte

```bash
# Genera reportes para todos los grados (LL, EL, ML)
python main.py --generate

# O genera solo para un grado específico
python main.py --generate --grados LL
```

Los reportes se guardarán en: `data/reportes_generados/`

## 6. Explorar el Dashboard Web

```bash
python main.py --dashboard
```

Abre tu navegador en: http://localhost:8501

## Comandos Útiles

### Generar reportes para un año específico

```bash
python main.py --generate --year-start 2024 --year-end 2024
```

### Generar solo Licenciatura y Especialidad

```bash
python main.py --generate --grados LL EL
```

### Ver ayuda completa

```bash
python main.py --help
```

## Estructura de los Reportes Generados

Cada archivo Excel contiene:

- **Hoja1**: Datos consolidados completos
- **Resumen**: Trayectoria por cohorte (P1-P6)
- **NI**: Nuevo Ingreso
- **Reinscritos**: Estudiantes reinscritos
- **Cuadro FIMPES**: Indicadores institucionales

## Programación Automática

Para que los reportes se generen automáticamente cada día:

```bash
# Edita config/config.yaml y configura:
scheduler:
  enabled: true
  schedule_time: "08:00"  # Hora deseada
  timezone: "America/Mexico_City"

# Luego ejecuta:
python -m src.backend.scheduler.tasks
```

Esto mantendrá el scheduler corriendo y generará reportes diariamente.

## Solución de Problemas Comunes

### Error de conexión a PostgreSQL

1. Verifica que PostgreSQL esté corriendo
2. Confirma que las credenciales en `.env` sean correctas
3. Prueba conectarte manualmente: `psql -h localhost -U tu_usuario -d tu_base`

### No se generan archivos Excel

1. Verifica que el directorio `data/reportes_generados/` exista
2. Revisa los logs en `logs/` para ver errores específicos
3. Confirma que haya datos en tu base de datos PostgreSQL

### Dashboard no inicia

```bash
# Reinstala Streamlit
pip install --upgrade streamlit

# Ejecuta directamente
streamlit run src/dashboard/app.py
```

## Próximos Pasos

1. Explora el dashboard web para visualizaciones interactivas
2. Configura la generación automática según tus necesidades
3. Revisa `ARQUITECTURA.md` para entender el sistema completo
4. Lee `README.md` para funcionalidades avanzadas

## Soporte

Si encuentras problemas:

1. Revisa los logs en `logs/`
2. Consulta la documentación en `README.md`
3. Verifica la arquitectura en `ARQUITECTURA.md`
