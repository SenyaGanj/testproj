from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


User = get_user_model()


class Command(BaseCommand):
    help = "Create user. We can't use default command because we use custom user model and use email as login"

    def add_arguments(self, parser) -> None:
        parser.add_argument('-e', '--email', type=str, help='Email')
        parser.add_argument('-p', '--password', type=str, help='Password')

    def handle(self, email: str, password: str, *args, **kwargs):
        user = User.objects.create(
            email=email,
            password=make_password(password),
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        return f'new superuser id is {user.id}'
