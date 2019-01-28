import unittest
from django.test import TestCase
from django.urls import reverse
from ..models import Department, Employee

# Testing expectations for sprint 1 in Django
# Context: What we send to the template
# Content: The rendered HTML
# Response_codes

class DepartmentTest(TestCase):
    """[Test case 1 (test_list_department) verifies that departments are listed when the department link is clicked]"""


    def test_list_department(self):
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


    # def test_get_training_detail(self):
    #     new_training = Training.objects.create(
    #         title="Test Training",
    #         start_date= datetime.now(),
    #         end_date= datetime.datetime('2019-02-28 03:20:23'),
    #         max_attendees= 41
    #     )
    #     self.client.get(reverse('agileHR:traindetail', args=(1,)))
    #     self.assertEqual(response.context["training"].title, "Test Training")