from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
# internals
from apps.core.models import Base

User = get_user_model()


class Slide(Base):
    """
    Header & Rightbar slides
    """
    class Position(models.TextChoices):
        HEADER = 'header', _('header')
        RIGHTBAR1 = 'rightbar1', _('rightbar1')
        RIGHTBAR2 = 'rightbar2', _('rightbar2')
        RIGHTBAR3 = 'rightbar3', _('rightbar3')

    index = models.SmallIntegerField()
    interval = models.PositiveSmallIntegerField(validators=[MinValueValidator(100), MaxValueValidator(20000)])
    title = models.CharField(max_length=140, null=True, blank=True)
    description = models.TextField(null=True, blank=True, default="")
    image = models.ImageField(_("Slide Image"), upload_to="images/slides/", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(
        max_length=24,
        choices=Position.choices,
        default=Position.RIGHTBAR3,
    )

    class Meta:
        db_table = "t_slide"
    
    def __str__(self) -> str:
        return f"{self.index} {self.position} {self.title}"


class ThankYou(models.Model):
    text = RichTextField()
    class Meta:
        db_table = "t_thankyou"
