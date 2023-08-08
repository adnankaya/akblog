from django.urls import path


# internal
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('profile/<slug:username>/', views.profile, name='profile'),
    path('profile/<slug:username>/rate/', views.rate_profile, name='rate-profile'),
    path('search/', views.user_search, name='user-search'),
    path('request-email-verification/', views.request_email_verification, name='request-email-verification'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
   
]
