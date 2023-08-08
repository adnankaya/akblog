from django.contrib import admin

# Register your models here.
from .models import Slide, ThankYou
admin.site.register([
    Slide, ThankYou
])