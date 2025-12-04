# Sistema de Automatización de Reportes de Trayectoria

Sistema híbrido de generación automática de reportes académicos con dashboard web interactivo y exportación a Excel.

## Características

- ✅ **Extracción automatizada** de datos desde PostgreSQL
- ✅ **Generación de reportes Excel** con formato profesional
- ✅ **Dashboard web interactivo** con visualizaciones
- ✅ **Programación automática** de reportes
- ✅ **Soporte para múltiples grados** académicos (Licenciatura, Especialidad, Maestría)
- ✅ **Métricas FIMPES** automatizadas

## Estructura del Proyecto

```
trayectoriacode/
├── src/
│   ├── backend/
│   │   ├── db/              # Conexión y queries a PostgreSQL
│   │   ├── processors/      # Extracción, transformación y generación
│   │   └── scheduler/       # Tareas programadas
│   ├── dashboard/           # Dashboard web con Streamlit
│   └── utils/               # Configuración y logging
├── data/
│   ├── reportes_generados/  # Reportes Excel generados
│   └── templates/           # Plantillas
├── config/
│   └── config.yaml          # Configuración principal
├── logs/                    # Archivos de log
├── main.py                  # Script principal
└── requirements.txt         # Dependencias
```

## Instalación

### 1. Clonar el repositorio

```bash
cd trayectoriacode
```

### 2. Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copia el archivo de ejemplo y configura tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` con tus datos de conexión a PostgreSQL:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=trayectoria_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_SCHEMA=core
```

### 5. Configurar el sistema

Edita `config/config.yaml` según tus necesidades:

```yaml
database:
  host: localhost
  port: 5432
  database: trayectoria_db
  schema: core

reports:
  year_start: 2021
  year_end: 2025
  grados:
    - LL  # Licenciatura
    - EL  # Especialidad
    - ML  # Maestría

scheduler:
  enabled: true
  schedule_time: "08:00"
  timezone: "America/Mexico_City"
```

## Uso

### Probar conexión a la base de datos

```bash
python main.py --test-connection
```

### Generar reportes manualmente

```bash
# Generar todos los reportes
python main.py --generate

# Generar solo para grados específicos
python main.py --generate --grados LL EL

# Generar para un año específico
python main.py --generate --year-start 2024 --year-end 2025
```

### Iniciar dashboard web

```bash
python main.py --dashboard
```

Luego abre tu navegador en: http://localhost:8501

### Iniciar generación automática programada

```bash
python -m src.backend.scheduler.tasks
```

Esto iniciará el scheduler que generará reportes automáticamente según la configuración.

## Reportes Generados

Cada reporte Excel contiene 5 hojas:

1. **Hoja1**: Datos consolidados de todos los periodos
2. **Resumen**: Trayectoria por cohorte (P1-P6)
3. **NI**: Estudiantes de nuevo ingreso
4. **Reinscritos**: Estudiantes reinscritos
5. **Cuadro FIMPES**: Indicadores institucionales

Los archivos se guardan en: `data/reportes_generados/`

## Dashboard Web

El dashboard incluye:

- 📈 **Visualización de Trayectoria**: Análisis de cohortes y seguimiento
- 📊 **Cuadro FIMPES**: Indicadores institucionales
- 📥 **Generación de Reportes**: Descarga bajo demanda
- ⚙️ **Configuración**: Ajustes del sistema

## Arquitectura

### Backend

- **PostgreSQL**: Base de datos fuente
- **psycopg2**: Conexión y pool de conexiones
- **pandas**: Procesamiento y transformación de datos
- **openpyxl**: Generación de archivos Excel

### Frontend

- **Streamlit**: Dashboard web interactivo
- **Plotly**: Visualizaciones gráficas

### Automatización

- **APScheduler**: Programación de tareas
- **Python logging**: Sistema de logs

## Desarrollo

### Ejecutar tests

```bash
pytest tests/
```

### Linting y formateo

```bash
black src/
flake8 src/
mypy src/
```

## Logs

Los logs se guardan en `logs/` con rotación automática:

- Nivel configurable (INFO, DEBUG, ERROR)
- Rotación a los 10MB
- Mantiene 5 archivos de respaldo

## Troubleshooting

### Error de conexión a PostgreSQL

1. Verifica que PostgreSQL esté corriendo
2. Confirma credenciales en `.env` o `config/config.yaml`
3. Verifica que el usuario tenga permisos en el schema `core`

### Error al generar Excel

1. Verifica que el directorio `data/reportes_generados/` exista
2. Confirma que haya datos en las tablas de PostgreSQL
3. Revisa los logs en `logs/`

### Dashboard no inicia

1. Instala Streamlit: `pip install streamlit`
2. Verifica que el puerto 8501 esté libre
3. Ejecuta: `streamlit run src/dashboard/app.py`

## Próximas Mejoras

- [ ] Cache de queries frecuentes (Redis)
- [ ] Notificaciones por email/Slack
- [ ] Exportación a PDF
- [ ] API REST para integración
- [ ] Autenticación de usuarios
- [ ] Dockerización completa

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto es de uso interno institucional.

## Contacto

Para soporte o preguntas, contacta al equipo de desarrollo.

## Documentación Adicional

- [Arquitectura del Sistema](ARQUITECTURA.md)
- [Guía de Queries SQL](config/queries.sql)
- Consulta los logs en `logs/` para troubleshooting detallado
