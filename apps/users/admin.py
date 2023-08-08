from django.contrib import admin

from apps.users.models import Profile, ProfileRate, User

# Register your models here.
admin.site.register([Profile, ProfileRate, User])