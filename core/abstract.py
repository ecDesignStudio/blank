from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from .managers import ActiveManager, PublishedManager, ReadOnlyManager


class ActiveModel(models.Model):
    """
    An abstract base class model that provides
    ``active`` field and a manager class.
    """
    active = models.BooleanField(
        _('active'),
        default=True
    )

    objects = models.Manager()
    actives = ActiveManager()

    class Meta:
        abstract = True


class PublishedModel(models.Model):
    """
    An abstract base class model that provides a manager and
    ``published_at`` and ``expired_at`` fields.
    """
    class Status(models.TextChoices):
        FINISHED = 'f', _('Finished')
        ONHOLD = 'o', _('On hold')
        PUBLISHED = 'p', _('Published')
        DRAFT = 'd', _('Draft')

    published_at = models.DateTimeField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        _('Publication status'),
        max_length=1,
        choices=Status.choices,
        default=Status.DRAFT
    )
    objects = models.Manager()
    published = PublishedManager()

    @property
    def active(self):
        return self.published_at < timezone.now().date() < self.expired_at

    @property
    def published(self):
        return self.status == self.Status.PUBLISHED and \
               self.expired_at > timezone.now().date()

    class Meta:
        abstract = True


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating
    ``created_at`` and ``modified_at`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SeoModel(models.Model):
    """
    An abstract base class model that provides seo tag
    ``meta_keywords`` , ``meta_title`` and ``meta_description`` fields.
    """
    meta_keywords = models.CharField(
        _('meta keywords'),
        max_length=160,
        blank=True
    )
    meta_title = models.CharField(
        _('meta title'),
        max_length=60,
        blank=True
    )
    meta_description = models.CharField(
        _('meta description'),
        max_length=300,
        blank=True
    )

    class Meta:
        abstract = True


class ReadOnlyModel(models.Model):
    """
    An abstract base class model that provides the ReadOnly manager.
    """
    objects = ReadOnlyManager()

    def save(self, *args, **kwargs):
        pass
        # raise NotImplemented

    def delete(self, *args, **kwargs):
        pass

    class Meta:
        managed = False
        abstract = True


class ModelIterable(models.Model):
    """
    An abstract base class model that which displays the fields of the model
    """
    def __iter__(self):
        field_names = [f.name for f in self._meta.fields]
        for field_name in field_names:
            value = getattr(self, field_name, None)
            yield (field_name, value)

    def show(self):
        for f in self:
            print(f)

    class Meta:
        abstract = True


class GeoModel(models.Model):
    """
    An abstract base class model that provides geolocation fields.
    ``latitude`` and ``longitude`` fields.
    """
    latitude = models.DecimalField(
        _('latitude'),
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        _('longitude'),
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True
    )
    # location = models.PointField()

    class Meta:
        abstract = True


class AddressModel(models.Model):
    """
    An abstract base class model that provides contacts fields
    ``address``, ``state``.``city``and ``longitude`` fields.
    """
    address = models.CharField(
        _('address'),
        max_length=200,
        blank=True,
        null=True
    )
    state = models.CharField(
        _('state'),
        max_length=100,
        blank=True,
        null=True
    )
    city = models.CharField(
        _('city'),
        max_length=100,
        blank=True,
        null=True
    )
    cp = models.CharField(
        _('postal code'),
        max_length=20,
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
