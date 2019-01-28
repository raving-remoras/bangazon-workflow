import unittest
import datetime
from django.test import TestCase
from django.urls import reverse
from ..models import Employee, Department


class EmployeeTest(TestCase):
    """Defines tests for Employee model and views

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

        print("hi")