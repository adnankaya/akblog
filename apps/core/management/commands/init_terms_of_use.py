# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _
from django.contrib.flatpages.models import FlatPage
from django.db import transaction
from django.urls import reverse
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Create website'

    @staticmethod
    def get_variable_name_as_str(var):
        return f"{var=}".split("=")[0]

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "\nProcess started...{}\n").format(__name__))
        try:
            with transaction.atomic():
                raw_html = """
                <!DOCTYPE html>
                <html lang="tr">
                <head>
                    <meta charset="UTF-8">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Terms of Use</title>
                </head>
                <body>
                    <h1>Update is necessary on admin panel</h1>
                </body>
                </html>
                """
                terms_of_use = FlatPage(
                    url=reverse("terms-of-use"),
                    title=_("Terms of Use"),
                    content=raw_html
                )
                terms_of_use.save()
                terms_of_use.sites.add(Site.objects.get_current())
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Process failed {e}"))

        self.stdout.write(self.style.SUCCESS("Process finished"))
