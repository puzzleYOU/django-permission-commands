from django.core.management import BaseCommand
from django.contrib.auth.models import Group, User

from sample_app.models import Address, Employee


class Command(BaseCommand):
    def handle(self, **_):
        group_a = Group.objects.update_or_create(name="Group A")
        group_b = Group.objects.update_or_create(name="Group B")

        addr_1, _ = Address.objects.update_or_create(
            street="Rainbow Lane 1337",
            postcode="12345",
            city="Cape Town",
        )
        addr_2, _= Address.objects.update_or_create(
            street="Memory Lane 4711",
            postcode="54321",
            city="Training Season",
        )

        Employee.objects.update_or_create(
            surname="Brown",
            prename="Bob",
            address=addr_1,
        )
        Employee.objects.update_or_create(
            surname="Potter",
            prename="Teddy",
            address=addr_2,
        )

        # deserves an award for the most secure credentials of the year... not.
        user_a = User.objects.create(username="userA", password="userA")
        user_b = User.objects.create(username="userB", password="userB")
