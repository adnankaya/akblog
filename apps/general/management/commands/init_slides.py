# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.general.models import Slide


class Command(BaseCommand):
    help = 'Generate slides'

    def create_slides(self, len, position="header"):
        for i in range(1, len):
            slide, created = Slide.objects.get_or_create(
                index=i,
                interval=i*2000,
                title=f"This is {i*2} sec. dynamic slide",
                description="",
                image=None,
                user=None,
                position=position,
            )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "\nProcess started...{}\n").format(__name__))

        try:
            with transaction.atomic():
                self.create_slides(4, position=Slide.Position.HEADER)
                self.create_slides(4, position=Slide.Position.RIGHTBAR1)
                self.create_slides(4, position=Slide.Position.RIGHTBAR2)
        except Exception as e:
            raise e

        self.stdout.write(self.style.SUCCESS("Process finished"))
