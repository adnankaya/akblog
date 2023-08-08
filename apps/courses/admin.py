from django.contrib import admin

# Register your models here.
from .models import Course, Lecture, UserLecture

admin.site.register([
    Course, Lecture, UserLecture
])