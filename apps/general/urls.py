
from django.urls import path

from . import views

app_name = "general"

urlpatterns = [
    path('contact/', views.contact_us, name="contact-us"),
    path('thank-you/', views.thankyou_view, name="thank-you"),
   



]
