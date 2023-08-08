

from django.shortcuts import redirect
from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin)
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.exceptions import PermissionDenied
from functools import wraps
import time
# internals
from .services import UserService
from .models import Profile


def post_creation_permission_required(view):
    @wraps(view)
    def _view(request, *args, **kwargs):
        user = request.user
        is_user_new = UserService.is_user_joined_in_a_month(user)
        is_user_created_post_today = UserService.is_user_created_a_post_today(
            user)
        is_user_created_post_this_week = UserService.is_user_created_a_post_this_week(
            user)
        if not user.has_active_post_package():
            if is_user_new and is_user_created_post_today:
                err_msg = """
                You do not have permission to publish a post today. Please contact to BUY a package.
                """
                messages.error(request, _(err_msg))
                time.sleep(0.5)
                return redirect("post:packages-index")

            if not is_user_new and is_user_created_post_this_week:
                err_msg = """
                You do not have permission to publish a post this week. Please contact to BUY a package.
                """
                messages.error(request, _(err_msg))
                time.sleep(0.5)
                return redirect("post:packages-index")
        # project view
        return view(request, *args, **kwargs)
    return _view

