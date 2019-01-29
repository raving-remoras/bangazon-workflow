import unittest
import datetime
from django.test import TestCase
from django.urls import reverse
from ..models import *


class EmployeeTest(TestCase):
    """Defines tests for Employee model and view

    Author: Rachel Daniel
    Methods:
        test_list_employees
    """

    def test_list_employees(self):
        """Tests the employee list view: creates a new employee and dept then ensures that data is present in context and content"""

        now = datetime.datetime.now()

        department = Department.objects.create(
            name = "Accounting",
            budget = 1000
        )

        new_employee = Employee.objects.create(
            first_name = "Deborah",
            last_name = "Smith",
            start_date = now,
            is_supervisor = False,
            department = department
        )

        response = self.client.get(reverse('agileHR:employee'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['employee_list']), 1)
        self.assertIn(new_employee.first_name.encode(), response.content)
        self.assertIn(new_employee.last_name.encode(), response.content)
        self.assertIn(new_employee.department.name.encode(), response.content)


class EmployeeDetailTest(TestCase):
    """Defines tests for Employee Detail view

    Author: Rachel Daniel
    Methods:
        test_employee_details
    """

    def test_employee_details(self):
        """Tests the employee list view: creates a new employee, department, computer, training and join tables, then ensures that all data is present in context and content"""

        now = datetime.datetime.now()

        department = Department.objects.create(
            name = "Accounting",
            budget = 1000
        )

        new_employee = Employee.objects.create(
            first_name = "Deborah",
            last_name = "Smith",
            start_date = now,
            is_supervisor = False,
            department = department
        )

        new_computer = Computer.objects.create(
            make = "Apple",
            model = "iMac",
            purchase_date = now,
            serial_no = "LKADLKNA7120129",
            retire_date = None,
        )

        new_training = Training.objects.create(
            title = "Taking Care of Business",
            start_date = now,
            end_date = now,
            max_attendees = 30
        )

        employee_computer = EmployeeComputer.objects.create(
            computer = new_computer,
            employee = new_employee,
            date_assigned = now
        )

        employee_training = EmployeeTraining.objects.create(
            employee = new_employee,
            training = new_training
        )

        response = self.client.get(reverse('agileHR:employee_detail', args=(1,)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['employee_computer']), 1)
        self.assertIn(new_employee.first_name.encode(), response.content)
        self.assertIn(new_employee.last_name.encode(), response.content)
        self.assertIn(new_employee.department.name.encode(), response.content)
        self.assertIn(new_computer.make.encode(), response.content)
        self.assertIn(new_training.title.title().encode(), response.content)

class EmployeeAddTest(TestCase):
    """Defines tests for Employee Add view

    Author: Rachel Daniel
    Methods:
        test_employee_form
    """

    def test_employee_form(self):
        """Tests that the employee add form page loads with expected fields"""

        response = self.client.get(reverse("agileHR:employee_add"))

        self.assertIn('<input type="text" class="form-control" name="first_name" id="first_name" />'.encode(), response.content)
        self.assertIn('<input type="text" class="form-control" name="last_name" id="last_name" />'.encode(), response.content)
        self.assertIn('<select class="form-control" name="department" id="department">'.encode(), response.content)
        self.assertIn('<input type="date" class="form-control" name="start_date" id="start_date" />'.encode(), response.content)
        self.assertIn('<input type="checkbox" class="form-check-input" name="is_supervisor" id="is_supervisor" />'.encode(), response.content)

    def test_employee_add(self):
        """Tests that the employee post view successfully posts new employees"""

        response = self.client.post(reverse('agileHR:employee_add'), {})

