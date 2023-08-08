from rest_framework import routers
from django.urls import path, include

from . import views

app_name = "categories"



urlpatterns = [
    path('', views.index, name="categories-index"),
    path('<slug:category_slug>/posts', views.categorized_posts, name='posts-by-category'),

]


