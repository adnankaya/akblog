from django.contrib import admin

# Register your models here.
from .models import About, MainService, Service


admin.site.register([
    About, MainService, Service
])