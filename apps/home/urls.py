from rest_framework import routers
from django.urls import path, include

from . import views

app_name = "home"



urlpatterns = [
    path('', views.index, name="home-index"),
    

]


