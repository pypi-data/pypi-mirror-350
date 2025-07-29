from django.db import models
from django.utils import timezone
from polymorphic.query import PolymorphicQuerySet


class ActiveOrNotQuerySet(models.QuerySet):
    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)

    def activate(self):
        return self.update(is_active=True)

    def deactivate(self):
        return self.update(is_active=False)

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def all(self, only_active=False):
        if only_active:
            return self.active()

        return super().all()


class BaseModelQuerySet(models.QuerySet):
    def update(self, **kwargs):
        kwargs.update({'update_at': timezone.now()})
        return super().update(**kwargs)


class BaseActiveOrNotQuerySet(BaseModelQuerySet, ActiveOrNotQuerySet):
    pass


class PolymorphicActiveOrNotQuerySet(PolymorphicQuerySet, ActiveOrNotQuerySet):
    pass


class PolymorphicBaseModelQuerySet(PolymorphicQuerySet, BaseModelQuerySet):
    pass


class PolymorphicBaseActiveOrNotQuerySet(PolymorphicQuerySet, BaseActiveOrNotQuerySet):
    pass
