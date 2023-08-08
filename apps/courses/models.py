from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
from django.conf import settings
from django.urls import reverse
from slugify import slugify
from django.db import transaction

# internals
from apps.core.models import Base, Attachment

User = get_user_model()


class Course(Base):
    title = models.CharField(max_length=140)
    description = RichTextField()
    lesson_count = models.PositiveSmallIntegerField(default=0)
    duration = models.DurationField()
    tutor = models.ForeignKey(User, on_delete=models.PROTECT)
    tags = TaggableManager()
    intro_url = models.URLField(null=True, blank=True)
    is_paid = models.BooleanField(default=True)
    slug = models.SlugField(max_length=250, unique=True, default="course-slug")
    category = models.ForeignKey(
        "post.Category", on_delete=models.SET_NULL, null=True)
    custom_css_style = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "t_course"

    def __str__(self) -> str:
        return self.title

    def get_tags(self):
        return self.tags.all()

    def get_absolute_url(self):
        return reverse('courses:course-detail',
                       args=[
                           self.slug,
                       ])

    def save(self, *args, **kwargs):
        try:
            with transaction.atomic():
                self.slug = slugify(self.title)
                super(Course, self).save(*args, **kwargs)
        except Exception as e:
            raise ValueError(e)


class Lecture(Base, Attachment):
    TARGET_ATTACHMENT = "lecture_attachments"

    title = models.CharField(max_length=140)
    description = RichTextField()
    duration = models.DurationField()
    video_url = models.URLField(null=True, blank=True)
    is_locked = models.BooleanField(default=True)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)

    class Meta:
        db_table = "t_lecture"

    def __str__(self) -> str:
        return self.title


class UserLecture(Base):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    lecture = models.ForeignKey(Lecture, on_delete=models.PROTECT)
    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "t_user_lecture"
