from django.contrib.sites.models import Site
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.conf import settings
from django.urls import reverse
from slugify import slugify
from django.db import transaction

# internals
from apps.core.models import Base, Attachment

User = get_user_model()


class Skill(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        db_table = "t_skill"

    def __str__(self) -> str:
        return self.name


def get_site():
    return Site.objects.first().domain


class Developer(Base):
    """
    Member of the site. Used for job seekers board.
    """
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    experience_years = models.PositiveSmallIntegerField(default=0)
    job_title = models.CharField(max_length=32)
    linkedin_pp_url = models.URLField(max_length=512, null=True, blank=True)
    linkedin = models.URLField(max_length=64, default=get_site)
    twitter = models.URLField(max_length=32, default=get_site)
    github = models.URLField(max_length=32, default=get_site)
    website = models.URLField(max_length=32, default=get_site)

    skills = models.ManyToManyField(Skill)

    class Meta:
        db_table = "t_developer"

    def __str__(self) -> str:
        return f"{self.user.email}"

    
