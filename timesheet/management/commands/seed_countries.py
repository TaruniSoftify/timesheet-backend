from django.core.management.base import BaseCommand
from timesheet.models import Country
from django_countries import countries

class Command(BaseCommand):
    help = "Seed all countries into the Country table"

    def handle(self, *args, **kwargs):
        for code, name in countries:
            Country.objects.get_or_create(name=code)
        self.stdout.write(self.style.SUCCESS("Countries seeded successfully"))
