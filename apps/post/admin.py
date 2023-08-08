from django.contrib import admin

# Register your models here.
from .models import (Post, Category, Package, PostPackage,
                     InappropriatePost, OrderedPackage, PostCreateRule,
                     PostImage,)

admin.site.register(
    [
        Post, PostImage, Category, InappropriatePost,
        Package, PostPackage, OrderedPackage, PostCreateRule
    ]
)

