from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache

"""
When any Model(s) object created, clear the cache!
"""
"""@receiver(post_save)
def clear_the_cache(**kwargs):
    cache.clear()"""