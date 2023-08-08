import logging
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.utils.translation import gettext as _
from django.views.generic.edit import View
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.template.response import TemplateResponse
from django.db.models import Q
from django.db import transaction
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.views.decorators.cache import never_cache
from django.views.decorators.vary import vary_on_cookie
from smtplib import SMTPAuthenticationError
# internals
from .forms import CustomUserLoginForm, CustomUserCreationForm, SearchForm
from .forms import UserUpdateForm, ProfileUpdateForm, ProfileCreationForm
from .tokens import get_account_activation_token
from .models import Profile, ProfileRate
from apps.post.services import PostService
from .services import UserService
from .tokens import get_account_activation_token
from apps.core.utils import query_debugger

User = get_user_model()
db_logger = logging.getLogger("db")

def request_email_verification(request):
    try:
        service = UserService()
        current_site = get_current_site(request)
        service.send_email_verification(request.user, current_site)
        messages.info(request,
                      _("""Email confirmation has been sent. Please checkout your inbox.. 
                            If you can not see email confirmation mail, check out Spam box."""
                        )
                      )
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as e:
        db_logger.exception(e)
        messages.error(request, str(e))


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    tkn = get_account_activation_token()
    if user is not None and tkn.check_token(user, token):
        user.email_verified = True
        user.save()
        PostService.activate_user_posts(user)
        return render(request, 'users/email_confirmation_done.html')
    else:
        return HttpResponse(_("Activation link is invalid!"))


def user_search(request):
    form = SearchForm()
    ctx = {"form": form}
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            results = User.objects.filter(Q(username__icontains=query))
            ctx.update(
                {
                    "query": query,
                    "users": results,
                }
            )
    return TemplateResponse(request, "users/search.html", ctx)


def register_view(request):
    user_form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST":
        try:
            with transaction.atomic():
                agreement = request.POST.get("agreement_accepted", False)
                if not agreement:
                    raise ValueError(
                        _("You can not use the platform without accepting terms of use.")
                    )
                if user_form.is_valid():
                    user = user_form.save(commit=False)
                    user.save()
                    messages.success(
                        request,
                        _("Successfully registered!")
                    )
                    try:
                        service = UserService()
                        current_site = get_current_site(request)
                        # TODO use async
                        service.send_email_verification(user, current_site)
                        messages.info(request, _(
                            "Confirmation email has been sent!"))
                    except ConnectionRefusedError:
                        messages.warning(request, _(
                            "Could not send email confirmation!"))
                    except SMTPAuthenticationError:
                        messages.warning(request, _(
                            """Could not send email confirmation! 
                            System administrators will investigate the problem."""
                            ))
                    return redirect(reverse_lazy("users:myprofile"))
        except Exception as e:
            db_logger.exception(e)
            messages.error(request, str(e))

    ctx = {
        "user_form": user_form,
    }
    return render(request, "users/register.html", ctx)

@never_cache
def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse_lazy("post:index"))
    form = CustomUserLoginForm(data=request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        raw_pass = form.cleaned_data.get("password")
        user = user = authenticate(
            request, username=username, password=raw_pass)
        login(request, user)
        next_url = request.GET.get('next') or reverse_lazy("post:index")
        return redirect(next_url)
    ctx = {
        "form": form,
    }
    return render(request, "users/login.html", ctx)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)


@login_required
def myprofile(request):
    """
    Authenticated user own profile
    """
    profile = request.user.profile
    ctx = {}
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         instance=profile)
        try:
            with transaction.atomic():
                if user_form.is_valid() and profile_form.is_valid():
                    user_form.save()
                    profile_form.save()
                    messages.success(request, _("Successfully updated!"))
                    return redirect("users:myprofile")
                else:
                    messages.error(request, user_form.errors)
                    messages.error(request, profile_form.errors)
        except Exception as e:
            db_logger.exception(e)
            messages.error(request, str(e))

    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=profile)
    ctx.update(
        {
            "profile": profile,
            "user_form": user_form,
            "profile_form": profile_form,
            "can_edit_profile": True if profile else False,
            "profile_posts": PostService.profile_posts(request.user),
        }
    )
    return render(request, "users/profile.html", ctx)


def profile(request, username=None):
    """
    Authenticated user somebody's profile
    """
    ctx = {}
    if username:
        user = User.objects.filter(
            username=username).select_related(
                "profile").first()
        can_edit_profile = user == request.user
        ctx.update(
            {
                "profile": user.profile if user else None,
                "can_edit_profile": can_edit_profile,
                "profile_posts": PostService.profile_posts(user),

            }
        )

    return render(request, "users/profile.html", ctx)


@login_required
def rate_profile(request, username=None):
    if request.method == "POST":
        try:
            rate = request.POST.get("rate")
            profile = Profile.objects.get(user__username=username)
            ProfileRate.objects.create(
                rate=rate, profile=profile, rated_by=request.user)
            messages.success(request,
                             _("Successfully rated! Thanks!")
                             )
            return redirect("users:profile", username=username)
        except Exception as e:
            db_logger.exception(e)
            raise ValueError("Raised an error while rating profile")
