from rest_framework import views, viewsets, generics, mixins
from rest_framework.permissions import IsAuthenticated
# internals

from .models import Post
from .serializers import PostSerializer
from apps.core.pagination_api import CustomPagination

class PostViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'put']
    permission_classes = (IsAuthenticated, )
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = Post.objects.all()
        return qs
