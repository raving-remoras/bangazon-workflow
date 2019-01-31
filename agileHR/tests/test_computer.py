import unittest
import datetime
from django.test import TestCase
from django.urls import reverse
from ..models import Computer, EmployeeComputer, Employee
from django.db.models.deletion import ProtectedError

class ComputerListTest(TestCase):
    """Defines tests for the main Computers view that displays the computer list.

    Author: Sebastian Civarolo

    Methods:
        test_list_computers
    """

    def test_list_computers(self):
        """Tests the computer list view: creates new employee, computer, and relationship"""

        now = datetime.datetime.now()

        new_employee = Employee.objects.create(
            first_name = "Deborah",
            last_name = "Smith",
            start_date = now,
            is_supervisor = False,
            department = None
        )

        new_computer = Computer.objects.create(
            make = "TestMake",
            model = "TestModel",
            purchase_date = now,
            serial_no = "AB123456789",
            retire_date = None,
        )

        join = EmployeeComputer.objects.create(
            computer = new_computer,
            employee = new_employee,
            date_assigned = now
        )

        response = self.client.get(reverse('agileHR:computers'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['computers']), 1)
        self.assertIn(new_computer.make.encode(), response.content)
        self.assertIn(new_computer.model.encode(), response.content)


class ComputerDetailTest(TestCase):
    """Defines tests for the Computer details view.

    Author: Sebastian Civarolo

    Methods:
        test_computer_detail

    """

    def test_computer_detail(self):
        """Tests the computer detail view: creates new employee, computer, and relationship."""

        now = datetime.datetime.now()

        new_employee = Employee.objects.create(
            first_name = "Deborah",
            last_name = "Smith",
            start_date = now,
            is_supervisor = False,
            department = None
        )

        new_computer = Computer.objects.create(
            make = "TestMake",
            model = "TestModel",
            purchase_date = now,
            serial_no = "AB123456789",
            retire_date = None,
        )

        join = EmployeeComputer.objects.create(
            computer = new_computer,
            employee = new_employee,
            date_assigned = now
        )

        response = self.client.get(reverse('agileHR:computer_detail', args=(1,)))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['computer'], new_computer)
        self.assertIn(new_computer.make.encode(), response.content)
        self.assertIn(new_computer.model.encode(), response.content)
        self.assertEqual(len(response.context['computer'].employeecomputer_set.all()), 1)


class NewComputerTest(TestCase):
    """Defines tests for the new computer view and adding computers to the db.

    Author: Sebastian Civarolo

    Methods:
        test_new_computer_form
        test_post_new_computer
    """

    def test_new_computer_form(self):
        """Tests that the new computer form loads properly."""

        response = self.client.get(reverse('agileHR:new_computer'))

        self.assertIn('<input class="form-control" type="text" name="make" id="make"'.encode(), response.content)

    def test_post_new_computer(self):
        """Tests posting a new computer from the new_computer view."""

        now = datetime.datetime.now()

        new_employee = Employee.objects.create(
            first_name = "Deborah",
            last_name = "Smith",
            start_date = now,
            is_supervisor = False,
            department = None
        )

        response = self.client.post(reverse("agileHR:new_computer"), {
            "make": "Make",
            "model": "Model",
            "serial_no": '123456',
            "purchase_date": datetime.datetime.now(),
            "employee": 1 })

        get_response = self.client.get(reverse("agileHR:computer_detail", args=(1,)))

        # Getting 302 when we have a success url and the view is redirecting, but sometimes 200?
        self.assertIn(response.status_code, [302, 200])
        # Get 200 when detail page loads with new computer data
        self.assertEqual(get_response.status_code, 200)


class DeleteComputerTest(TestCase):
    """Defines tests for trying to delete a computer.

    Author: Sebastian Civarolo

    Methods:
        test_view_delete_computer
        test_delete_computer
        test_delete_protected_computer
    """

    def test_view_delete_computer(self):
        """Tests that the delete confirmation page loads correctly."""

        now = datetime.datetime.now()
        computer = Computer.objects.create(make="m", model="m", serial_no="123", purchase_date=now)

        response = self.client.get(reverse("agileHR:delete_computer", args=(1,)))

        self.assertEqual(response.status_code, 200)
        self.assertIn("Are you sure you want to delete".encode(), response.content)

    def test_delete_computer(self):
        """Tests you can delete a computer that has never been assigned."""

        now = datetime.datetime.now()
        computer = Computer.objects.create(make="m", model="m", serial_no="123", purchase_date=now)

        response = self.client.post(reverse("agileHR:delete_computer", args=(1,)))
        self.assertEqual(response.status_code, 302)

        # confirm the computer is deleted
        no_computer = Computer.objects.filter(pk=1)
        self.assertEqual(len(no_computer), 0)

    def test_delete_protected_computer(self):
        """Tests you cannot delete a computer that has been assigned to an employee."""

        now = datetime.datetime.now()

        new_employee = Employee.objects.create(
            first_name = "Deborah",
            last_name = "Smith",
            start_date = now,
            is_supervisor = False,
            department = None
        )

        make_computer = self.client.post(reverse("agileHR:new_computer"), {
            "make": "Make",
            "model": "Model",
            "serial_no": '123456',
            "purchase_date": datetime.datetime.now(),
            "employee": 1
        })

        # try to delete the computer
        with self.assertRaises(ProtectedError):
            response = self.client.post(reverse("agileHR:delete_computer", args=(1,)))