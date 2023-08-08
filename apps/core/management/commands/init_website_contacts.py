# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import os
from django.apps import apps
from django.db import transaction


class Command(BaseCommand):
    help = 'Create website'

    @staticmethod
    def get_variable_name_as_str(var):
        return f"{var=}".split("=")[0]

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "\nProcess started...{}\n").format(__name__))
        Website = apps.get_model("core", "Website")
        Mail = apps.get_model("core", "Mail")
        Phone = apps.get_model("core", "Phone")
        SocialAccount = apps.get_model("core", "SocialAccount")
        try:
            with transaction.atomic():
                ws_name = os.environ.get("WEBSITE", "example.com")
                website = Website.objects.create(is_active=True, name=ws_name)

                emails = os.environ.get(
                    "WEBSITE_EMAILS", "adnankaya@example.com")
                emails = emails.split(" ")
                for i, email in enumerate(emails):
                    Mail.objects.create(
                        email=email, slug=f"mail-{i}", website=website)

                phones = os.environ.get(
                    "WEBSITE_PHONES", "5555555555")
                phones = phones.split(" ")
                for i, phone_num in enumerate(phones):
                    Phone.objects.create(
                        number=phone_num, slug=f"phone-{i}", website=website)

                twitter = os.environ.get("TWITTER")
                facebook = os.environ.get("FACEBOOK")
                instagram = os.environ.get("INSTAGRAM")
                linkedin = os.environ.get("LINKEDIN")

                SocialAccount.objects.create(slug="twitter",
                                             url=f"www.twitter.com/{twitter}", website=website)
                SocialAccount.objects.create(slug="facebook",
                                             url=f"www.facebook.com/{facebook}", website=website)
                SocialAccount.objects.create(slug="instagram",
                                             url=f"www.instagram.com/{instagram}", website=website)
                SocialAccount.objects.create(slug="linkedin",
                                             url=f"www.linkedin.com/in/{linkedin}", website=website)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Process FAILED: \n{e}"))

        self.stdout.write(self.style.SUCCESS("Process finished"))
