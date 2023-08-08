from django.db import models
from django.utils.translation import gettext as _
from ckeditor.fields import RichTextField
# internals
from apps.core.models import Base


class About(Base):
    title = models.CharField(max_length=120)
    description = RichTextField(null=True, blank=True)

    class Meta:
        db_table = "t_aboutus"
        verbose_name = _("About us")
        verbose_name_plural = _("About us")

    def __str__(self) -> str:
        return self.title


class MainService(Base):
    name = models.CharField(max_length=120)
    description = RichTextField(null=True, blank=True)
    icon_html = models.CharField(max_length=120, null=True, blank=True)
    path = models.CharField(max_length=32, default="/")
    index = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "t_aboutus_main_service"
        verbose_name = _("Main Service")
        verbose_name_plural = _("Main Services")

    def __str__(self) -> str:
        return self.name


class Service(Base):
    name = models.CharField(max_length=120)
    description = RichTextField(null=True, blank=True)
    main_service = models.ForeignKey(MainService, on_delete=models.CASCADE)
    icon_html = models.CharField(max_length=120, null=True, blank=True)
    path = models.CharField(max_length=32, default="/")

    class Meta:
        db_table = "t_aboutus_service"
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self) -> str:
        return self.name
