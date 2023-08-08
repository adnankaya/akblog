from django.shortcuts import render
from django.db import transaction
from django.conf import settings
from django.contrib import messages
from django.utils.translation import gettext as _
from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from taggit.models import Tag
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
import logging
import uuid
# internals
from apps.core.pagination import paginate_objects
from apps.core.services import hit_count_service
from .models import Developer, Skill
from .forms import DeveloperForm, DeveloperUpdateForm
from apps.users.services import UserService
from .services import DeveloperService

# globals
db_logger = logging.getLogger('db')
User = get_user_model()



def update(request):
    ctx = {}
    user_service = UserService()
    dev_service = DeveloperService()
    form = DeveloperUpdateForm()

    ctx.update({
        "form": form,
        "skills": Skill.objects.all()
    })
    return render(request, "developers/create.html", ctx)


def create(request):
    ctx = {}
    user_service = UserService()
    dev_service = DeveloperService()
    form = DeveloperForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            developer = dev_service.create_developer(request, form)
            current_site = get_current_site(request)
            user_service.send_email_verification(developer.user, current_site)
            messages.success(request, _(
                "You joined to the developers board. To be displayed in board please verify your email"))

            return HttpResponseRedirect(reverse_lazy("developers:developers-job-seekers"))
        except ValueError as ve:
            messages.error(request, str(ve))
            return HttpResponseRedirect(reverse_lazy("developers:developer-create"))

    ctx.update({
        "form": form,
        "skills": Skill.objects.all()
    })
    return render(request, "developers/create.html", ctx)


def skills_view(request):
    skills = Skill.objects.values("id", "name")
    return JsonResponse(list(skills), safe=False)


def index(request):
    all_devs = Developer.objects.filter(user__email_verified=True)
    ctx = {}
    page = request.GET.get('page')
    limit = request.GET.get("limit", settings.DEVELOPERS_LIMIT_PER_PAGE)
    paginated_devs = paginate_objects(all_devs, page, per_page=limit)

    ctx.update({
        "paginated_devs": paginated_devs,
        "page": page,
    })

    return render(request, "developers/index.html", ctx)


def detail(request, id):
    """
    Course RETRIEVE & UPDATE view.
    """
    pass
