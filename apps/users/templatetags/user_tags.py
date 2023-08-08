from django.utils.safestring import mark_safe
from django import template
from django.db.models import Count
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import get_user_model
# internals

User = get_user_model()
register = template.Library()


@register.simple_tag
def is_profile_rated_by_user_before(profile, user):
    if not profile:
        return False
    return user.profilerate_set.filter(profile=profile).exists()


@register.simple_tag
def get_member_count():
    key = settings.KEY_PREFIX_USER_COUNT
    qs_data = cache.get(key=key)
    if not qs_data:
        qs_data = User.objects.aggregate(total_users=Count("id"))
        cache.set(key=key, value=qs_data)
    return qs_data.get("total_users")
