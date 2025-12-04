"""
Módulo de logging centralizado
"""
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(
    name: str,
    log_file: str | Path | None = None,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configura y retorna un logger

    Args:
        name: Nombre del logger
        log_file: Ruta del archivo de log (opcional)
        level: Nivel de logging
        max_bytes: Tamaño máximo del archivo antes de rotar
        backup_count: Número de archivos de respaldo a mantener

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicación de handlers
    if logger.handlers:
        return logger

    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para archivo (si se proporciona)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str, log_dir: str | Path | None = None) -> logging.Logger:
    """
    Obtiene o crea un logger con configuración por defecto

    Args:
        name: Nombre del módulo/logger
        log_dir: Directorio de logs (opcional)

    Returns:
        Logger configurado
    """
    log_file = None
    if log_dir:
        log_dir_path = Path(log_dir)
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = log_dir_path / f"{name}_{date_str}.log"

    return setup_logger(name, log_file)
