"""
Módulo de configuración centralizada
"""
import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
import yaml


@dataclass
class DatabaseConfig:
    """Configuración de base de datos PostgreSQL"""
    host: str
    port: int
    database: str
    user: str
    password: str
    schema: str = "core"
    pool_size: int = 5
    max_overflow: int = 10

    @property
    def connection_string(self) -> str:
        """Retorna string de conexión"""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class PathConfig:
    """Configuración de rutas del proyecto"""
    root_dir: Path
    data_dir: Path
    reports_dir: Path
    templates_dir: Path
    logs_dir: Path

    @classmethod
    def from_root(cls, root_dir: str | Path):
        """Crea configuración desde directorio raíz"""
        root = Path(root_dir)
        return cls(
            root_dir=root,
            data_dir=root / "data",
            reports_dir=root / "data" / "reportes_generados",
            templates_dir=root / "data" / "templates",
            logs_dir=root / "logs"
        )


@dataclass
class ReportConfig:
    """Configuración de reportes"""
    year_start: int = 2021
    year_end: int = 2025
    grados: list[str] = None

    def __post_init__(self):
        if self.grados is None:
            self.grados = ["LL", "EL", "ML"]  # Licenciatura, Especialidad, Maestría


@dataclass
class SchedulerConfig:
    """Configuración de tareas programadas"""
    enabled: bool = True
    schedule_time: str = "08:00"  # Formato HH:MM
    timezone: str = "America/Mexico_City"


class Config:
    """Configuración principal del sistema"""

    def __init__(self, config_file: Optional[str | Path] = None):
        self.config_file = config_file
        self._load_config()

    def _load_config(self):
        """Carga configuración desde archivo YAML o variables de entorno"""
        if self.config_file and Path(self.config_file).exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
        else:
            config_data = {}

        # Database config (prioriza variables de entorno)
        db_config = config_data.get('database', {})
        self.database = DatabaseConfig(
            host=os.getenv('DB_HOST', db_config.get('host', 'localhost')),
            port=int(os.getenv('DB_PORT', db_config.get('port', 5432))),
            database=os.getenv('DB_NAME', db_config.get('database', 'trayectoria')),
            user=os.getenv('DB_USER', db_config.get('user', 'postgres')),
            password=os.getenv('DB_PASSWORD', db_config.get('password', '')),
            schema=os.getenv('DB_SCHEMA', db_config.get('schema', 'core')),
            pool_size=int(os.getenv('DB_POOL_SIZE', db_config.get('pool_size', 5))),
            max_overflow=int(os.getenv('DB_MAX_OVERFLOW', db_config.get('max_overflow', 10)))
        )

        # Path config
        root_dir = os.getenv('PROJECT_ROOT', str(Path(__file__).parent.parent.parent))
        self.paths = PathConfig.from_root(root_dir)

        # Report config
        report_config = config_data.get('reports', {})
        self.reports = ReportConfig(
            year_start=report_config.get('year_start', 2021),
            year_end=report_config.get('year_end', 2025),
            grados=report_config.get('grados', ["LL", "EL", "ML"])
        )

        # Scheduler config
        scheduler_config = config_data.get('scheduler', {})
        self.scheduler = SchedulerConfig(
            enabled=scheduler_config.get('enabled', True),
            schedule_time=scheduler_config.get('schedule_time', '08:00'),
            timezone=scheduler_config.get('timezone', 'America/Mexico_City')
        )

    def create_directories(self):
        """Crea directorios necesarios si no existen"""
        for path in [
            self.paths.data_dir,
            self.paths.reports_dir,
            self.paths.templates_dir,
            self.paths.logs_dir
        ]:
            path.mkdir(parents=True, exist_ok=True)


# Instancia global de configuración
config = Config(config_file=Path(__file__).parent.parent.parent / "config" / "config.yaml")
