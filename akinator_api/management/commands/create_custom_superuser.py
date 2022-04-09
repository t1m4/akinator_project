from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            user = User.objects.get(username='ruslan')
        except User.DoesNotExist:
            user = User.objects.create_superuser(settings.ADMIN_USERNAME, settings.ADMIN_EMAIL, settings.ADMIN_PASSWORD)
            print('created new user - {}'.format(user))
            return

        print('user already exists - {}'.format(user))
        user.delete()