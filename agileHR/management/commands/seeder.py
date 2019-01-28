import random

from django.utils import timezone
from django.core.management.base import BaseCommand
from django_seed import Seed

from agileHR.models import *

seeder = Seed.seeder()

class Command(BaseCommand):

    def handle(self, *args, **options):
        """Creates fake data to populate the database."""

        # Seed data for Departments
        seeder.add_entity(Department, 75, {
            "name": lambda x: seeder.faker.bs(),
            "budget": lambda x: seeder.faker.ean8()
        })

        # Seed data for Employees
        seeder.add_entity(Employee, 75, {
            "first_name": lambda x: seeder.faker.first_name(),
            "last_name": lambda x: seeder.faker.last_name(),
            "start_date": lambda x: seeder.faker.date_time_this_decade(before_now=True, after_now=False),
            "end_date": None,
            "is_supervisor": False
        })


        # Seed data for Computers
        computer_makes = ["Apple", "Dell", "Samsung", "Lenovo", "MSI", "ASUS", "Potato"]
        computer_models = ["Model 1", "Model 2", "SilverBook", "ThoughtSheet", "YogaPose", "Orange Pro", "XPQ", "Inspiroff", "IsThisThingOn", "Cardboard", "Grandpa", "PieceOfCrap", "AbsoluteUnit", "Blinky", "Pinky", "Inky", "Clyde", "BigBrother"]

        seeder.add_entity(Computer, 75, {
            "make": lambda x: seeder.faker.word(ext_word_list=computer_makes),
            "model": lambda x: seeder.faker.word(ext_word_list=computer_models),
            "serial_no": lambda x: seeder.faker.bban(),
            "purchase_date": lambda x: seeder.faker.date_time_this_decade(before_now=True, after_now=False),
            "retire_date": None
        })

        seeder.add_entity(EmployeeComputer, 75, {
            "date_assigned": lambda x: timezone.now(),
            "date_revoked": lambda x: random.choice([timezone.now(), None, None, None, None, None])
        })

        # Seed data for Training
        max_attendees=[10, 15, 20, 22, 24, 27,28, 35, 40, 53]

        # Seed data for past training
        # seeder.add_entity(Training, 10, {
        #     "title":lambda x: seeder.faker.catch_phrase(),
        #     "start_date":lambda x: seeder.faker.date_time_this_decade(before_now=True, after_now=False),
        #     "end_date":lambda x: seeder.faker.date_time_this_decade(before_now=True, after_now=False),
        #     "max_attendees": lambda x: seeder.faker.word(ext_word_list=max_attendees),
        # })

        seeder.add_entity(Training, 20, {
            "title":lambda x: seeder.faker.catch_phrase(),
            "start_date":lambda x: seeder.faker.future_datetime(end_date="+60d"),
            "end_date":lambda x: seeder.faker.future_datetime(end_date="+90d"),
            "max_attendees": lambda x: seeder.faker.word(ext_word_list=max_attendees),
        })

        # seeder data for Employee Training Join Table
        seeder.add_entity(EmployeeTraining, 80)


        # Make the magic happen
        seeder.execute()