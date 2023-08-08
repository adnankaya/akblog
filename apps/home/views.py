from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _

# internals
from apps.aboutus.models import MainService


def index(request):
    
    mainservices = MainService.objects.prefetch_related(
        "service_set"
    ).order_by("index")
    ctx = {
        "mainservices": mainservices
    }
    return render(request, "home/index.html", ctx)

