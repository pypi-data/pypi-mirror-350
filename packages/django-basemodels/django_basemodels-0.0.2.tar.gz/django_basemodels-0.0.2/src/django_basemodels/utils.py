import logging
import celery_hchecker
import warnings

logger = logging.getLogger(__name__)


class CeleryHealthCheckerNotInitialized(UserWarning):
    pass


def is_celery_ready() -> bool:
    """
    Возвращает True, если Celery доступен и воркеры запущены.
    Бросает RuntimeError, если CeleryHealthChecker не инициализирован.
    """
    checker = celery_hchecker.CeleryHealthChecker.get_instance()
    if checker is None:
        warnings.warn(
            'Warning: Celery health checker is not initialized. '
            'Please create celery health checker instance if you use celery.',
            CeleryHealthCheckerNotInitialized
        )
        return False
    try:
        return checker.is_healthy()
    except Exception as e:
        logger.error(f"Error checking Celery health: {e}")
        return False
