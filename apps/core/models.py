from django.db import models
from slugify import slugify
from django.core.validators import (
    MinLengthValidator
)
from phonenumber_field.modelfields import PhoneNumberField


class Base(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        abstract = True
        default_manager_name = 'objects'


class Attachment(models.Model):
    TARGET_ATTACHMENT = "target_attachments"
    attachment = models.FileField(
        upload_to=TARGET_ATTACHMENT, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        abstract = True
        default_manager_name = 'objects'


class Website(models.Model):
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    name = models.CharField(max_length=60, default='demosite')

    class Meta:
        db_table = 't_website'
        verbose_name = "Website"
        verbose_name_plural = "Websites"

    def __str__(self) -> str:
        return self.name


class Mail(Base):
    """Used for website emails"""
    email = models.EmailField()
    slug = models.SlugField(max_length=24, unique=True)
    display = models.BooleanField(default=True)
    website = models.ForeignKey("Website", on_delete=models.CASCADE)

    class Meta:
        db_table = 't_mail'
        verbose_name = "Mail"
        verbose_name_plural = "Mails"

    def __str__(self) -> str:
        return f"Mail {self.email}"

class EmailSubscriber(Base):
    """Used for website emails"""
    email = models.EmailField()
    is_subscribed = models.BooleanField(default=True)

    class Meta:
        db_table = 't_email_subscriber'
        verbose_name = "Email Subscriber"
        verbose_name_plural = "Email Subscribers"

    def __str__(self) -> str:
        return f"Mail {self.email}"


class Phone(Base):
    """Used for website phones"""
    number = PhoneNumberField(max_length=13, validators=[
        MinLengthValidator(13)])
    slug = models.SlugField(max_length=24, unique=True)
    display = models.BooleanField(default=True)
    website = models.ForeignKey("Website", on_delete=models.CASCADE)

    class Meta:
        db_table = 't_phone'
        verbose_name = "Phone"
        verbose_name_plural = "Phones"

    def __str__(self) -> str:
        return f"Phone {self.slug} {self.number}"


class SocialAccount(Base):
    slug = models.SlugField(max_length=24)
    url = models.URLField()

    profile = models.ForeignKey('users.Profile', related_name="socialaccounts",
                                on_delete=models.SET_NULL, null=True, blank=True)
    website = models.ForeignKey('core.Website', related_name="socialaccounts",
                                on_delete=models.CASCADE)

    class Meta:
        db_table = 't_socialaccount'
        unique_together = [['slug', 'url']]

    def __str__(self) -> str:
        return f"{self.slug} {self.url}"

    def get_url(self):
        if self.url.startswith("https://"):
            return self.url[7:]
        return self.url

class UrlHit(models.Model):
    url = models.URLField()
    hits_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 't_urlhit'

    def __str__(self):
        return f"{self.hits_count} | {str(self.url)}"

    def increase(self):
        self.hits_count += 1
        self.save()


class HitCount(models.Model):
    url_hit = models.ForeignKey(
        UrlHit, editable=False, on_delete=models.CASCADE)
    ip = models.CharField(max_length=40)
    session = models.CharField(max_length=40)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 't_hitcount'
