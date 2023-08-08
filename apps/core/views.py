from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext as _

# internals
from .models import EmailSubscriber

def custom_http_404_page(request, exception):
    context = {}
    return render(request, "errors/404.html", context)


def custom_http_500_page(request, template_name="errors/500.html"):
    context = {}
    return render(request, template_name, context)


def email_subscription(request):
    if request.method == "POST":
        email = request.POST.get('email')
        EmailSubscriber.objects.create(email=email)
        messages.success(request,_("Thank you for joining our email newsletter!"))
        return redirect(reverse_lazy("general:thank-you"))
    
    # TODO un-subscribe with http params


def set_theme(request):
    # Save the selected theme in the user's session or database
    request.session['theme'] = request.POST.get("theme")
    # Determine the URL of the current page
    current_url = request.META.get('HTTP_REFERER')
    if current_url:
        return redirect(current_url)
    else:
        return redirect(reverse_lazy("post:index"))
