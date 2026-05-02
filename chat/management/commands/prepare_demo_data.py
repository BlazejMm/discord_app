from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from chat.models import Channel


class Command(BaseCommand):
    help = "Prepare clean demo accounts and channels for the Komunikator project."

    def handle(self, *args, **options):
        User = get_user_model()

        old_demo_users = ["Izabela", "Pawel", "Karol", "Anna"]
        removed_count, _ = User.objects.filter(username__in=old_demo_users).delete()

        accounts = [
            {
                "username": "admin",
                "email": "admin@komunikator.local",
                "password": "Admin12345",
                "role": "admin",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "username": "moderator",
                "email": "moderator@komunikator.local",
                "password": "Moderator12345",
                "role": "mod",
                "is_staff": False,
                "is_superuser": False,
            },
        ]

        for account in accounts:
            password = account.pop("password")
            user, _ = User.objects.get_or_create(username=account["username"])
            for field, value in account.items():
                setattr(user, field, value)
            user.is_blocked = False
            user.set_password(password)
            user.save()

        for name in ["ogolny", "prywatny", "projekty", "materialy"]:
            Channel.objects.get_or_create(name=name)

        self.stdout.write(
            self.style.SUCCESS(
                f"Prepared Komunikator demo data. Removed old records: {removed_count}."
            )
        )
