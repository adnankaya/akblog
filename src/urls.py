
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.flatpages import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap 
from apps.post.sitemaps import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
    name='django.contrib.sitemaps.views.sitemap')
]

urlpatterns += i18n_patterns(
    path('users/', include("apps.users.urls")),
    path('general/', include("apps.general.urls")),
    path('aboutus/', include("apps.aboutus.urls")),
    path('terms-of-use/', views.flatpage, {'url': '/terms-of-use/'}, name='terms-of-use'),
    path('', include("apps.post.urls")),
    path('', include("apps.home.urls")),
    path('courses/', include("apps.courses.urls")),
    path('core/', include("apps.core.urls")),
    path('categories/', include("apps.categories.urls")),
    path('developers/', include("apps.developers.urls")),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
)

# handler500 = "apps.core.views.custom_http_500_page"
# handler404 = "apps.core.views.custom_http_404_page"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.STATIC_URL,
    #                       document_root=settings.STATIC_ROOT)


urlpatterns.extend([
    path('ckeditor/', include('ckeditor_uploader.urls')),

                    ])