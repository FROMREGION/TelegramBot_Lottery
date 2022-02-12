from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from TeleShop.settings import DJANGO_STAFF


class Command(BaseCommand):
    help = 'Initialization of the Django staff'

    def handle(self, *args, **options):
        if User.objects.count() >= len(DJANGO_STAFF):
            print('Checking Django users... OK')
        else:
            print('Creating Django users... ', end='')
            for employee in DJANGO_STAFF:
                self.__init_employee(**employee)
            print('OK')

    @staticmethod
    def __init_employee(username, email, password):
        user = User.objects.create_superuser(username, email, password)
        user.save()
