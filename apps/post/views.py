import logging
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import (
    CreateView,
)
from django.views.decorators.vary import vary_on_cookie
from django.views.decorators.cache import cache_page
from django.db import transaction
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from django.urls import reverse_lazy
from taggit.models import Tag
# internals
from .models import (Post, InappropriatePost, Package, Category,
                     PostPackage, OrderedPackage, PostImage)
from .forms import PostForm, PostSearchForm, PostImageForm, PostUpdateForm
from apps.core.pagination import paginate_objects
from .services import PostService
from apps.core.models import Website
from apps.core.services import hit_count_service
from apps.core.utils import query_debugger

db_logger = logging.getLogger('db')



def index(request, tag_slug=None):
    """
    Users can list post
    """
    all_posts = Post.actives.all()
    categories = Category.objects.all()
    ctx = {}
    category_ids = request.GET.getlist("cid")
    if category_ids:
        all_posts = all_posts.filter(category_id__in=category_ids)
    if "query" in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            all_posts = all_posts.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query)
            )
            ctx.update(
                {
                    "query": query,
                }
            )
    # filtering by clicked tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        all_posts = all_posts.filter(tags__in=[tag])
    page = request.GET.get('page')
    limit = request.GET.get("limit", settings.POST_LIMIT_PER_PAGE)
    paginated_posts = paginate_objects(all_posts, page, per_page=limit)

    ctx.update({
        "paginated_posts": paginated_posts,
        "page": page,
        "tag": tag,
        "categories": categories,
    })
    return render(request, "post/index.html", ctx)


def detail(request, year, month, day, slug, pk):
    """
    Post RETRIEVE & UPDATE view.
    """
    ctx = {}
    try:
        post = Post.objects.filter(
            is_deleted=False
        ).select_related(
            "created_by",
            "created_by__profile",
            "category").prefetch_related(
            "tags", "postimage_set").get(pk=pk)
        form = PostUpdateForm(request.POST or None, instance=post)
        if request.method == "POST":
            is_deleted = request.POST.get("is_deleted", None)
            if is_deleted:
                post.is_deleted = True
                post.save()
                messages.info(request, _("Deleted successfully!"))
                return redirect(reverse_lazy("users:myprofile"))
            try:
                if form.is_valid():
                    success_msg = _("Updated successfully!")
                    post = form.save()
                    messages.success(request, success_msg)
                    PostService.create_post_images(request, post)
                    return HttpResponseRedirect(post.get_absolute_url())
                else:
                    messages.error(request, form.errors)
            except Exception as e:
                db_logger.exception(e)
    except Post.DoesNotExist:
        post = None
        messages.error(request, _("Could not found the post!"))
    else:
        ctx.update({
            "post": post,
            "title": post.title,
            "remaining_image_upload": settings.MAX_POST_IMAGES_LEN - post.postimage_set.count(),
            "total_image_upload": settings.MAX_POST_IMAGES_LEN,
            "form": form,
            "similar_posts": PostService.get_similar_posts(post, 6)
        })
        #  to count views
        hit_count = hit_count_service(request)
        ctx.update({"hit_count": hit_count})
    return render(request, "post/detail.html", ctx)


@login_required
def create_post(request):
    """
    Users can create post
    """
    template_name = "post/new.html"
    if request.method == "POST":
        post_form = PostForm(request.POST)
        try:
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.created_by = request.user
                if request.user.email_verified:
                    post.is_active = True
                post.save()
                messages.success(request, _(
                    "Created new post successfully!"))
                PostService.create_post_tags(request, post)
            return HttpResponseRedirect(post.get_absolute_url())
        except IntegrityError as ie:
            msg = f"""
            You already opeend a post with this title! 
            Please enter a different title.
            """
            db_logger.exception(ie)
            messages.error(request, _(msg))
            return render(request,  template_name, ctx)
        except Exception as e:
            db_logger.exception(e)
            messages.error(request, post_form.errors.as_text())

    ctx = {
        "categories": Category.objects.all().order_by("name"),
    }
    return render(request, template_name, ctx)


def remove_post_image(request, post_pk, postimg_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post_img = get_object_or_404(PostImage, pk=postimg_pk, post=post)
    post_img.delete()
    messages.success(request, _("Image deleted."))
    return HttpResponseRedirect(post.get_absolute_url())


def flag_post(request, pk):
    """
    Users can report a post as inappropriate
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        reason = request.POST.get("reason")
        InappropriatePost.objects.create(
            post=post, reason=reason, reported_by=request.user
        )
        messages.warning(request, _("Thanks for reporting the post!"))
        return HttpResponseRedirect(post.get_absolute_url())




def packages_index(request):
    website = Website.objects.prefetch_related(
        "phone_set", "mail_set"
    ).first()
    ctx = {
        "packages": Package.objects.all(),
        "website": website,
    }
    return render(request, "post/packages/index.html", ctx)
