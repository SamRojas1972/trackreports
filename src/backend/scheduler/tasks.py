"""
Módulo de tareas programadas para generación automática de reportes
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz

from src.backend.processors import ExcelGenerator
from src.utils.config import config
from src.utils.logger import get_logger


logger = get_logger(__name__, config.paths.logs_dir)


class ReportScheduler:
    """Scheduler para generación automática de reportes"""

    def __init__(self):
        """Inicializa el scheduler"""
        self.scheduler = BackgroundScheduler(timezone=config.scheduler.timezone)
        self.generator = ExcelGenerator()
        logger.info("ReportScheduler inicializado")

    def generate_all_reports_task(self):
        """Tarea que genera todos los reportes"""
        try:
            logger.info("=== Iniciando generación automática de reportes ===")
            start_time = datetime.now()

            results = self.generator.generate_all_reports(
                year_start=config.reports.year_start,
                year_end=config.reports.year_end
            )

            elapsed = (datetime.now() - start_time).total_seconds()

            successful = sum(1 for v in results.values() if v is not None)
            total = len(results)

            logger.info(f"Generación automática completada en {elapsed:.2f}s: {successful}/{total} exitosos")

            for grado, path in results.items():
                if path:
                    logger.info(f"  ✓ {grado}: {path}")
                else:
                    logger.error(f"  ✗ {grado}: Error")

            return results

        except Exception as e:
            logger.error(f"Error en generación automática: {e}")
            raise

    def schedule_daily_reports(self):
        """Programa generación diaria de reportes"""
        if not config.scheduler.enabled:
            logger.info("Scheduler deshabilitado en configuración")
            return

        try:
            # Parsear hora configurada
            hour, minute = map(int, config.scheduler.schedule_time.split(':'))

            # Crear trigger cron para ejecución diaria
            trigger = CronTrigger(
                hour=hour,
                minute=minute,
                timezone=pytz.timezone(config.scheduler.timezone)
            )

            # Agregar tarea
            self.scheduler.add_job(
                self.generate_all_reports_task,
                trigger=trigger,
                id='daily_report_generation',
                name='Generación Diaria de Reportes',
                replace_existing=True
            )

            logger.info(f"Tarea programada: Generación diaria a las {config.scheduler.schedule_time} {config.scheduler.timezone}")

        except Exception as e:
            logger.error(f"Error programando tarea: {e}")
            raise

    def start(self):
        """Inicia el scheduler"""
        try:
            self.schedule_daily_reports()
            self.scheduler.start()
            logger.info("Scheduler iniciado exitosamente")

            # Log de tareas programadas
            jobs = self.scheduler.get_jobs()
            logger.info(f"Tareas programadas: {len(jobs)}")
            for job in jobs:
                logger.info(f"  - {job.name}: próxima ejecución {job.next_run_time}")

        except Exception as e:
            logger.error(f"Error iniciando scheduler: {e}")
            raise

    def stop(self):
        """Detiene el scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler detenido")

    def run_now(self):
        """Ejecuta la generación de reportes inmediatamente"""
        logger.info("Ejecutando generación manual de reportes")
        return self.generate_all_reports_task()

    def get_next_run_time(self) -> datetime:
        """Obtiene la próxima hora de ejecución programada"""
        jobs = self.scheduler.get_jobs()
        if jobs:
            return jobs[0].next_run_time
        return None


def start_scheduler():
    """Función para iniciar el scheduler como servicio"""
    scheduler = ReportScheduler()
    scheduler.start()

    try:
        # Mantener el scheduler corriendo
        import time
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        scheduler.stop()
        logger.info("Scheduler detenido por usuario")


if __name__ == "__main__":
    logger.info("=== Iniciando servicio de scheduler ===")
    start_scheduler()
