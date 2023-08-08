from django.shortcuts import render

# internals
from apps.core.models import Website
from .models import ThankYou


def contact_us(request):
    website = Website.objects.filter(is_active=True).first()
    context = {
        "website": website
    }
    return render(request, "general/contactus.html", context)


def thankyou_view(request):

    context = {
        "thankyou": ThankYou.objects.last()
    }
    return render(request, "general/thankyou.html", context)
