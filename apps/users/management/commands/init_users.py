from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

User = get_user_model()

FIRSTNAMES = ["adnan","ibrahim","murat"]
LASTNAMES = ["kaya","kayace","kaya"]

class Command(BaseCommand):
    help = 'Generate users'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("\nProcess started...{}\n").format(__name__))
        with transaction.atomic():
            try:
                for i in range(0, len(FIRSTNAMES)):
                    user = User.objects.create_user(
                        username=f"{FIRSTNAMES[i]}",
                        email=f"{FIRSTNAMES[i]}@example.com",
                        password="qwert",
                        first_name=FIRSTNAMES[i],
                        last_name=LASTNAMES[i],
                        email_verified=True,
                        agreement_accepted=True,
                    )
            except:
                pass

        self.stdout.write(self.style.SUCCESS("Process finished"))
