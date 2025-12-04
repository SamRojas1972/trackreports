# Arquitectura de Automatización de Reportes de Trayectoria

## 1. Componentes del Sistema

### 1.1 Backend Python (`/src/backend/`)
- **Módulo de Conexión BD**: Conexión a PostgreSQL con pool de conexiones
- **Módulo de Extracción**: Ejecución de queries SQL parametrizadas
- **Generador de Excel**: Creación de archivos XLSB/XLSX con formato
- **API REST**: Endpoints para dashboard y generación bajo demanda
- **Scheduler**: Tareas programadas (cron/APScheduler)

### 1.2 Dashboard Web (`/src/dashboard/`)
- **Framework**: Streamlit o Dash (Python)
- **Visualizaciones**: Gráficos interactivos de trayectoria
- **Filtros**: Por periodo, campus, programa, grado académico
- **Exportación**: Descarga de Excel/CSV
- **Autenticación**: Control de acceso por equipo

### 1.3 Base de Datos
- **PostgreSQL**: Base de datos existente (core schema)
- **Cache Redis** (opcional): Para queries frecuentes

### 1.4 Sistema de Archivos
- **Reportes Generados**: `/reportes/generados/{fecha}/`
- **Templates**: `/reportes/templates/` (plantillas Excel)
- **Logs**: `/logs/` (auditoría y monitoreo)

## 2. Flujos de Trabajo

### 2.1 Generación Automática Programada
```
Scheduler (Cron)
    ↓
Extracción BD (SQL)
    ↓
Procesamiento de Datos (pandas)
    ↓
Generación Excel (openpyxl/xlsxwriter)
    ↓
Almacenamiento + Notificación (email/slack)
```

### 2.2 Generación Bajo Demanda
```
Usuario → Dashboard/API
    ↓
Parámetros (año, grado)
    ↓
Extracción + Procesamiento
    ↓
Descarga Directa
```

### 2.3 Visualización en Dashboard
```
Usuario → Dashboard
    ↓
Filtros Interactivos
    ↓
Query Optimizado (cache)
    ↓
Gráficos + Tablas Dinámicas
```

## 3. Tecnologías

### Backend
- **Python 3.11+**
- **psycopg2**: Conexión PostgreSQL
- **pandas**: Manipulación de datos
- **openpyxl/XlsxWriter**: Generación de Excel
- **FastAPI**: API REST (opcional si usas Streamlit)
- **APScheduler**: Tareas programadas

### Frontend/Dashboard
- **Streamlit**: Dashboard rápido e interactivo
  - Ventajas: Desarrollo rápido, Python nativo
  - Ideal para equipos técnicos
- **Alternativa Plotly Dash**: Más control de UI

### Infraestructura
- **Docker**: Contenedores para portabilidad
- **Nginx**: Proxy reverso (producción)
- **Systemd/Supervisor**: Gestión de procesos

## 4. Estructura de Directorios

```
trayectoriacode/
├── src/
│   ├── backend/
│   │   ├── db/
│   │   │   ├── connection.py
│   │   │   └── queries.py
│   │   ├── processors/
│   │   │   ├── extractor.py
│   │   │   ├── transformer.py
│   │   │   └── excel_generator.py
│   │   ├── api/
│   │   │   ├── main.py
│   │   │   └── routes.py
│   │   └── scheduler/
│   │       └── tasks.py
│   ├── dashboard/
│   │   ├── app.py
│   │   ├── pages/
│   │   │   ├── trayectoria.py
│   │   │   ├── resumen.py
│   │   │   └── fimpes.py
│   │   └── components/
│   │       ├── filters.py
│   │       └── charts.py
│   └── utils/
│       ├── config.py
│       └── logger.py
├── data/
│   ├── reportes_generados/
│   └── templates/
├── tests/
├── config/
│   ├── config.yaml
│   └── queries.sql
├── logs/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## 5. Roadmap de Implementación

### Fase 1: Backend Core (Semana 1-2)
- [x] Análisis de estructura actual
- [ ] Módulo de conexión a PostgreSQL
- [ ] Refactorización de queries SQL parametrizadas
- [ ] Extractor de datos con pandas
- [ ] Generador básico de Excel

### Fase 2: Generación Automatizada (Semana 2-3)
- [ ] Generador avanzado con formato (colores, anchos, fórmulas)
- [ ] Sistema de templates para cada tipo de reporte
- [ ] Scheduler para ejecución automática
- [ ] Sistema de notificaciones

### Fase 3: Dashboard Web (Semana 3-4)
- [ ] Dashboard básico con Streamlit
- [ ] Visualizaciones de trayectoria
- [ ] Filtros interactivos
- [ ] Exportación de datos
- [ ] Autenticación simple

### Fase 4: Optimización y Deploy (Semana 4-5)
- [ ] Caché de queries frecuentes
- [ ] Dockerización
- [ ] Documentación
- [ ] Testing
- [ ] Deploy en producción

## 6. Consideraciones

### Seguridad
- Credenciales en variables de entorno (`.env`)
- Conexiones SSL a PostgreSQL
- Autenticación para dashboard
- Auditoría de accesos

### Performance
- Connection pooling para BD
- Queries optimizadas con índices
- Cache para reportes frecuentes
- Procesamiento asíncrono para reportes grandes

### Mantenimiento
- Logs estructurados
- Monitoreo de errores
- Backups de reportes generados
- Versionado de queries SQL
