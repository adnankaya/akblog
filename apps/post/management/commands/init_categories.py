# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from apps.post.models import Category

CATEGORIES = [
    "python",
    "django",
    "flask",
]


class Command(BaseCommand):
    help = 'Generate categories'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("\nProcess started...{}\n").format(__name__))
        for category in CATEGORIES:
            Category.objects.get_or_create(
                name=category
            )

        self.stdout.write(self.style.SUCCESS("Process finished"))
