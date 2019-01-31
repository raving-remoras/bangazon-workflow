import random

from django.utils import timezone
from django.core.management.base import BaseCommand
from django_seed import Seed

from agileHR.models import *

seeder = Seed.seeder()

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Seed data for Departments
        seeder.add_entity(Department, 2, {
            "name": lambda x: seeder.faker.bs(),
            "budget": lambda x: seeder.faker.ean8()
        })

        # Seed data for Employees
        seeder.add_entity(Employee, 10, {
            "first_name": lambda x: seeder.faker.first_name(),
            "last_name": lambda x: seeder.faker.last_name(),
            "start_date": lambda x: seeder.faker.date_time_this_decade(before_now=True, after_now=False),
            "end_date": None,
            "is_supervisor": False
        })

        max_attendees=[10, 15, 20, 22, 24, 27,28, 35, 40, 53]

        seeder.add_entity(Training, 15, {
            "title": lambda x: seeder.faker.catch_phrase(),
            "max_attendees": lambda x: seeder.faker.word(ext_word_list=max_attendees),
            "start_date":lambda x: seeder.faker.past_datetime(start_date="-60d"),
            "end_date": lambda x: seeder.faker.past_datetime(start_date="-30d")
        })

        seeder.add_entity(EmployeeTraining, 20)

        seeder.execute()