from django.shortcuts import render

# internals
from .models import About, MainService


def index(request):
    about = About.objects.first()
    mainservices = MainService.objects.prefetch_related(
        "service_set"
    )
    context = {
        "about": about,
        "mainservices": mainservices
    }
    return render(request, "aboutus/index.html", context)
