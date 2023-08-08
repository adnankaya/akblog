from rest_framework import routers
from django.urls import path, include

from . import views

app_name = "core"



urlpatterns = [
    path('', views.email_subscription, name="email-subscription"),
    path('set-theme/', views.set_theme, name='set_theme'),
    

]


