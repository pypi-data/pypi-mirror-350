from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Manager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import BaseModelQuerySet, ActiveOrNotQuerySet, BaseActiveOrNotQuerySet
from .utils import is_celery_ready


class BaseModel(models.Model):
    _created_at = models.DateTimeField(
        name="created_at", auto_now_add=True, null=False, blank=True, editable=False, verbose_name=_("Дата создания")
    )
    _updated_at = models.DateTimeField(
        name="updated_at", auto_now=True, null=False, blank=True, editable=False,
        verbose_name=_("Время последнего обновления")
    )

    objects = Manager.from_queryset(BaseModelQuerySet)()

    @property
    def created_at(self):
        return self._created_at

    @property
    def updated_at(self):
        return self._updated_at

    class Meta:
        abstract = True
        ordering = ['-updated_at']


class ActiveOrNotModel(models.Model):
    _is_active = models.BooleanField(
        db_column='is_active',
        default=True,
        null=False, blank=True,
        verbose_name=_("Активность")
    )

    active_start = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Начало активности")
    )
    active_end = models.DateTimeField(
        null=True, blank=True,
        verbose_name=_("Конец активности")
    )

    objects = Manager.from_queryset(ActiveOrNotQuerySet)()

    def clean(self):
        super().clean()
        if self.active_start and self.active_end and self.active_end < self.active_start:
            raise ValidationError("Конец активности не может быть раньше начала")

    def activate(self):
        self._is_active = True
        self.save()

    def deactivate(self):
        self._is_active = False
        self.save()

    @property
    def is_active(self):
        if is_celery_ready():
            return self._is_active

        if not self.active_start and not self.active_end:
            return self._is_active

        now = timezone.now()
        active_start = self.active_start or now
        return (active_start <= now) and (self.active_end >= now if self.active_end else True)

    @is_active.setter
    def is_active(self, is_active: bool):
        self._is_active = is_active

    class Meta:
        abstract = True
        indexes = [
            # Для запросов типа .filter(is_active=True)
            models.Index(fields=['is_active']),

            # Для временных диапазонов
            models.Index(fields=['active_start', 'active_end']),

            # Для часто используемых комбинаций
            models.Index(fields=['is_active', 'active_start']),
            models.Index(fields=['is_active', 'active_end']),

            models.Index(fields=['is_active', 'active_start', 'active_end']),
            models.Index(fields=['active_start']),
            models.Index(fields=['active_end']),
        ]


class BaseActiveOrNotModel(BaseModel, ActiveOrNotModel):
    objects = Manager.from_queryset(BaseActiveOrNotQuerySet)()

    class Meta:
        abstract = True
