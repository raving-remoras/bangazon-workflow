import unittest
from django.test import TestCase
from django.urls import reverse
from ..models import Department, Employee

# Testing expectations for sprint 1 in Django
# Context: What we send to the template
# Content: The rendered HTML
# Response_codes

class DepartmentTest(TestCase):
    """Defines tests for Department list view

    Author: Brendan McCray
    Methods:
        test_list_department
    """

    def test_list_department(self):
        """Test case (test_list_department) verifies that departments are listed when the navbar's 'departments' link is clicked"""

        new_dept = Department.objects.create(
            name = "Nashville Software School",
            budget = 12345678
        )

        # Issue a GET request
        response = self.client.get(reverse('agileHR:department'))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 1 department
        self.assertEqual(len(response.context['departments']), 1)

        # .encode converts from unicode utf-8 (note that department names are in all CAPS)
        self.assertIn(new_dept.name.upper().encode(), response.content)


class DepartmentDetailTest(TestCase):
    """Defines tests for Department detail view

    Author: Brendan McCray
    Methods:
        test_get_department_detail
    """

    def test_get_department_detail(self):
        """Test case (test_get_department_detail) verifies that a specific department's name and assigned employees are rendered when a particular department name is clicked in the departments list"""

        new_dept = Department.objects.create(
            id = 2,
            name = "Nashville Software School Department",
            budget = 23456789
        )

        new_employee = Employee.objects.create(
            first_name = "Rob",
            last_name = "Boss",
            start_date = "2016-03-07 05:53:53",
            end_date = None,
            is_supervisor = 0,
            department_id = 2
        )

        new_employee2 = Employee.objects.create(
            first_name = "Dave",
            last_name = "Matthews",
            start_date = "2017-03-07 05:53:54",
            end_date = None,
            is_supervisor = 0,
            department_id = 1 # note this department ID is not the arg passed in below
        )

        response = self.client.get(reverse('agileHR:department_detail', args=(2,)))

        # Test that department name in context matches the created value
        self.assertEqual(response.context["department"].name, "Nashville Software School Department")

        # Test that department name is in the HTML response content
        self.assertIn(new_dept.name.upper().encode(), response.content)

        # Employee first and last names appear in HTML response content
        self.assertIn(new_employee.first_name.encode(), response.content)
        self.assertIn(new_employee.last_name.encode(), response.content)

        # Employee 2 will not appear on page (department IDs do not match)
        self.assertNotIn(new_employee2.first_name.encode(), response.content)
        self.assertNotIn(new_employee2.last_name.encode(), response.content)

        # Establish new department with no employees assigned (no employees created with department_id = 3)
        new_dept = Department.objects.create(
            id = 3,
            name = "Nashville Software School Department 2",
            budget = 34567890
        )

        response = self.client.get(reverse('agileHR:department_detail', args=(3,)))

        # Ensure response is correct when no employees are assigned to the selected department
        self.assertIn("No employees are assigned to this department.".encode(), response.content)

class DepartmentPostTest(TestCase):
    """Defines tests for Department form and database POST

    Author: Brendan McCray
    Methods:
        test_department_form
    """

    def test_department_form(self):
        """Test case (test_get_department_form) verifies that the rendered form contains two required input elements"""
        response = self.client.get(reverse('agileHR:departmentadd'))

        # verify that the content of the response has the required input fields.
        self.assertIn("<input type='text' name='dept_name' />".encode(), response.content)
        self.assertIn("<input type='number' name='dept_budget' />".encode(), response.content)



# Your test suite must verify that when a POST operation is performed to the corresponding URL, then a successful response is received (i.e. status code must be 200)