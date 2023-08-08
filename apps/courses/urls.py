from rest_framework import routers
from django.urls import path, include

from . import views

app_name = "courses"



urlpatterns = [
    path('', views.index, name="courses-index"),
    path('<slug:slug>/', views.detail, name='course-detail'),
    # must be end of the urlpatterns
    path('<slug:tag_slug>/', views.index, name='courses-by-tag'),

]


