from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
# internals


class BaseViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    http_method_names = ['get', 'post', 'put']
    permission_classes = (IsAuthenticated, )

