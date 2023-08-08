from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile
from django.db.models import Q

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


from django.core.cache import cache
from django.conf import settings
# internals
from apps.post import models as post_models


@receiver(post_save, sender=User)
def clear_cache_user_count(**kwargs):
    cache.delete(key=settings.KEY_PREFIX_USER_COUNT)