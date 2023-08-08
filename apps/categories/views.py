from django.shortcuts import render
from django.conf import settings
# internals
from apps.post.models import Post
from apps.core.pagination import paginate_objects


def index(request):
    context = {
        
    }
    return render(request, "categories/index.html",context)


def categorized_posts(request, category_slug):
    all_posts = Post.actives.filter(category__slug=category_slug)
    ctx = {}
    category_ids = request.GET.getlist("cid")
    if category_ids:
        all_posts = all_posts.filter(category_id__in=category_ids)
    
    
    page = request.GET.get('page')
    limit = request.GET.get("limit", settings.POST_LIMIT_PER_PAGE)
    paginated_posts = paginate_objects(all_posts, page, per_page=limit)

    ctx.update({
        "paginated_posts": paginated_posts,
        "page": page,
    })
    return render(request, "post/index.html", ctx)