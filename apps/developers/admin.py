from django.contrib import admin

# Register your models here.
from .models import Developer, Skill

admin.site.register([
    Developer,
    Skill
])