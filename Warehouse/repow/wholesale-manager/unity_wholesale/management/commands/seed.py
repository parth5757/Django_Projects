
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, call_command
from allauth.account.admin import EmailAddress


class Command(BaseCommand):
    help = "Seed Migrations."

    def __init__(self):
        self.user_class = get_user_model()
        super().__init__()

    def handle(self, *args, **options):
        apps = settings.LOCAL_APPS
        for app in apps:
            
            call_command("makemigrations", app.split(".")[-1])
        call_command("migrate")
        self.create_super_user()

    def create_super_user(self):
        if self.user_class.objects.filter(
            email=settings.ADMIN_EMAIL,
        ).exists():
            self.stdout.write("Admin account : Already exist")
            return False

        super_user = self.user_class.objects.create(
            username=settings.ADMIN_USERNAME,
            email=settings.ADMIN_EMAIL,
            role=self.user_class.SUPER_ADMIN
        )   
        super_user.set_password(settings.ADMIN_PASSWORD)
        super_user.save()
        
        EmailAddress.objects.create(
            user=super_user,
            verified=True,
            primary=True,
            email=settings.ADMIN_EMAIL
        )

        self.stdout.write("Created {} admin account.".format(settings.ADMIN_EMAIL))
