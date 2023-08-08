from django.db import models
from django.db.models import Q, Avg
from hashlib import md5
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    MinValueValidator,
    MaxValueValidator)
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
# internals


class User(AbstractUser):
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=255,
        unique=True,
        error_messages={'unique': _("Use different email address.")}
    )
    email_verified = models.BooleanField(default=False)
    agreement_accepted = models.BooleanField(
        verbose_name=_("Agreement"), default=True)

    def qs_ordered_packages(self):
        return self.orderedpackage_set.prefetch_related(
            "postpackage_set").filter(
                is_active=True)

    def has_active_post_package(self):
        return self.qs_ordered_packages().exists()

    def get_active_ordered_package(self):
        qs = self.qs_ordered_packages()
        ordered_package = qs.earliest("due_date")
        return ordered_package

    def get_full_name(self) -> str:
        res = super().get_full_name()
        if not res:
            return self.username
        return res


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField("About", max_length=280, null=True, blank=True, default=_("New member"))

    phone = PhoneNumberField(max_length=13, validators=[
                             MinLengthValidator(13)])

    class Meta:
        db_table = "t_profile"
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self) -> str:
        return f"Profile {self.user.username}"

    def get_profile_rate(self):
        """Example return data is 3.0"""
        res_dict = self.profilerate_set.aggregate(avg_rate=Avg("rate"))
        return res_dict.get("avg_rate")


class ProfileRate(models.Model):
    profile = models.ForeignKey("Profile", verbose_name="Profil",
                                on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField("Rate",
                                            default=1,
                                            validators=[MinValueValidator(
                                                1), MaxValueValidator(5)]
                                            )
    rated_by = models.ForeignKey(User,
                                 verbose_name="Rated by",
                                 on_delete=models.CASCADE)

    class Meta:
        db_table = "t_profile_rate"
        unique_together = ["profile", "rated_by"]

    def __str__(self) -> str:
        return f"{self.profile} | {self.rate}"
