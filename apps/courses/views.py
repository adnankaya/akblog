from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from taggit.models import Tag
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _

# internals
from apps.core.pagination import paginate_objects
from apps.core.services import hit_count_service
from .models import Course, Lecture, UserLecture


def index(request):
    all_courses = Course.objects.all()
    ctx = {}
    # filtering by clicked tag
    tag = request.GET.get("tag")
    if tag:
        qs_filtered = all_courses.filter(tags__name__in=[tag])
        if not qs_filtered:
            messages.warning(request, _("Courses not found with this tag! See others."))
        else:
            all_courses = qs_filtered

    page = request.GET.get('page')
    limit = request.GET.get("limit", settings.COURSE_LIMIT_PER_PAGE)
    paginated_courses = paginate_objects(all_courses, page, per_page=limit)

    ctx.update({
        "paginated_courses": paginated_courses,
        "page": page,
        "tag": tag,
    })
    return render(request, "courses/index.html", ctx)


def detail(request, slug):
    """
    Course RETRIEVE & UPDATE view.
    """
    ctx = {}
    try:
        course = Course.objects.filter(

        ).select_related(
            "tutor",
            "tutor__profile",
            "category").prefetch_related(
            "tags",).get(slug=slug)

    except Course.DoesNotExist:
        course = None
        messages.error(request, _("Could not find the course!"))

    ctx.update({
        "course": course,
        # "similar_courses": CourseService.get_similar_courses(course, 6)
    })
    #  to count views
    hit_count = hit_count_service(request)
    ctx.update({"hit_count": hit_count})
    return render(request, "courses/detail.html", ctx)
