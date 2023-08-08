# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.aboutus.models import About, MainService, Service


class Command(BaseCommand):
    help = 'Generate about us'

    

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(
            "\nProcess started...{}\n").format(__name__))

        try:
            with transaction.atomic():
                About.objects.create(
                    title="Title for about us",
                    description="Description for about us",
                )
                for i in range(1, 5):
                    ms, created = MainService.objects.get_or_create(
                        name=f"main service name {i}",
                        description=f"main service description {i}"
                    )
                    for j in range(1,6):
                        s, created2 = Service.objects.get_or_create(
                            name=f"service name {i}.{j}",
                            description=f"service description {i}.{j}",
                            main_service = ms,
                        )

        except Exception as e:
            raise e

        self.stdout.write(self.style.SUCCESS("Process finished"))
