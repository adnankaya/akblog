from django.utils.translation import gettext as _
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

# internals
from .tokens import get_account_activation_token

User = get_user_model()


class UserService(object):

    @staticmethod
    def is_user_joined_in_a_month(user: User) -> bool:
        today = timezone.make_aware(
            timezone.datetime.today(),
            timezone.get_default_timezone()
        )
        return user.date_joined > (today - timezone.timedelta(days=30))

    @staticmethod
    def is_user_created_a_post_today(user: User) -> bool:
        today = timezone.make_aware(
            timezone.datetime.today(),
            timezone.get_default_timezone()
        )
        return user.post_set.filter(created_date__date=today.date()).exists()

    @staticmethod
    def is_user_created_a_post_this_week(user: User):
        today = timezone.make_aware(
            timezone.datetime.today(),
            timezone.get_default_timezone()
        )
        this_week = today.date()-timezone.timedelta(days=7)
        return user.post_set.filter(
            created_date__date__gte=this_week
        ).exists()

    def send_email_verification(self, user, current_site):
        _template = 'users/activate_user.html'
        url = reverse_lazy('users:activate',
                           kwargs={
                               'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                               'token': get_account_activation_token().make_token(user),
                           })
        activate_url = '{}{}'.format(current_site.domain, url)
        _context = {
            'user': user,
            'activate_url': activate_url,
        }
        mail_subject = _('Email confirmation.')
        message = render_to_string(_template, _context)
        email = EmailMessage(
            subject=mail_subject, body=message, 
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.content_subtype = "html"
        email.send()

       