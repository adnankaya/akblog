from rest_framework import routers
from django.urls import path, include

from . import views
from .views_api import PostViewSet

app_name = "post"

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet, basename='api-posts')

urlpatterns = [
    path('posts/', views.index, name="index"),
    path('posts/new/', views.create_post, name='create'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/<int:pk>/', views.detail, name='post-detail'),
    path('posts/<int:pk>/report/', views.flag_post, name='flag-post'),
    path('posts/<int:post_pk>/images/<int:postimg_pk>/', views.remove_post_image, name='remove-post-image'),


    path('posts/packages/', views.packages_index, name="packages-index"),
    # must be end of the urlpatterns
    path('posts/<slug:tag_slug>/', views.index, name='posts-by-tag'),

]

# API urls
urlpatterns.extend([
    path("api/v1/", include(router.urls)),
])
