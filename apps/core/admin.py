from django.contrib import admin

# Register your models here.
from .models import Website, Mail, Phone, SocialAccount, UrlHit, HitCount, EmailSubscriber

admin.site.register([
    Website, Mail, Phone, SocialAccount, UrlHit, HitCount,
    EmailSubscriber
])