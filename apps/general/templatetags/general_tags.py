from django.utils.safestring import mark_safe
from django import template
from django.db.models import Count
from django.core.cache import cache
# internals
from apps.general.models import Slide

register = template.Library()


@register.simple_tag
def get_header_slide_objects():
    key = "slide_header_"
    qs_data = cache.get(key=key)
    if not qs_data:
        qs_data = Slide.objects.filter(position="header").order_by("index")
        cache.set(key=key, value=qs_data)
    return qs_data


@register.simple_tag
def get_rightbar1_slides():
    key = "slide_rightbar1_"
    qs_data = cache.get(key=key)
    if not qs_data:
        qs_data = Slide.objects.filter(position="rightbar1").order_by("index")
        cache.set(key=key, value=qs_data)
    return qs_data


@register.simple_tag
def get_rightbar2_slides():
    key = "slide_rightbar2_"
    qs_data = cache.get(key=key)
    if not qs_data:
        qs_data = Slide.objects.filter(position="rightbar2").order_by("index")
        cache.set(key=key, value=qs_data)
    return qs_data


@register.simple_tag
def get_rightbar3_slides():
    key = "slide_rightbar3_"
    qs_data = cache.get(key=key)
    if not qs_data:
        qs_data = Slide.objects.filter(position="rightbar3").order_by("index")
        cache.set(key=key, value=qs_data)
    return qs_data
