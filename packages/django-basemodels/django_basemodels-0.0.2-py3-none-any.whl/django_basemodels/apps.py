import logging
from pathlib import Path

from celery.signals import beat_init
from django.apps import AppConfig
from django.conf import settings
from django.core.checks import Error, register
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


class DjangoBaseModels(AppConfig):
    name = 'django_basemodels'
    verbose_name = _("Базовые модели")

    def ready(self):
        package_path = Path(__file__).parent
        locale_path = str(package_path / "locale")
        if locale_path not in settings.LOCALE_PATHS:
            settings.LOCALE_PATHS += (locale_path,)

        beat_init.connect(DjangoBaseModels._setup_periodic_task)

    @staticmethod
    def _setup_periodic_task(*args, **kwargs):
        from django_celery_beat.models import IntervalSchedule, PeriodicTask

        """Автоматически добавляем задачу в расписание при инициализации Celery"""
        schedule, _created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.MINUTES,
        )
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Models activity update',
            task='django-basemodels.update_activity_status',
        )
        logger.info("Added periodic activity update task to Celery beat schedule")


@register
def check_dependencies(app_configs, **kwargs):
    errors = []
    required_apps = ['polymorphic']

    for app in required_apps:
        if app not in settings.INSTALLED_APPS:
            errors.append(
                Error(
                    f"{app} must be in INSTALLED_APPS.",
                    hint=f"Please, add '{app}' to INSTALLED_APPS",
                    id='django-basemodels.E001',
                )
            )
    return errors
