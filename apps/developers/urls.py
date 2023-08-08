from rest_framework import routers
from django.urls import path, include

from . import views

app_name = "developers"



urlpatterns = [
    path('', views.index, name="developers-job-seekers"),
    path('create/', views.create, name="developer-create"),
    path('update/', views.update, name="developer-update"),
    path('skills/', views.skills_view, name="developer-skills"),
    path('<int:id>/', views.detail, name='developer-detail'),
   

]


