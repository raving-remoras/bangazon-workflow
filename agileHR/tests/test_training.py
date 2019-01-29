import unittest
from django.test import TestCase
from django.urls import reverse
from ..models import Training, Employee, EmployeeTraining
from datetime import datetime
from datetime import timedelta

class TrainingTest(TestCase):
    """Defines tests for Training Models and Views

        Author: Kelly Morin

        Methods:
            test_list_training
            test_get_training_detail
    """


    def test_list_training(self):
        """Test case verifies that the training sessions are listed when the navbar's 'training' link is clicked"""

        future_date = datetime.now(tz=None)+ timedelta(days=2)
        new_training = Training.objects.create(
            title="Test Training",
            start_date= datetime.now(tz=None),
            end_date= future_date,
            max_attendees= 41
        )

        # Issue a GET request
        response = self.client.get(reverse('agileHR:training'))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains 1 training session
        self.assertEqual(len(response.context['training_list']), 1)

        # .encode converts from unicode utf-8
        self.assertIn(new_training.title.encode(), response.content)

    def test_get_training_detail(self):
        """Test case verifies that a specific training session's name and assigned employees are rendereed when a particular training session is clicked in the training list"""

        future_date = datetime.now(tz=None)+ timedelta(days=2)
        new_training = Training.objects.create(
            title="Test Training",
            start_date= datetime.now(tz=None),
            end_date= future_date,
            max_attendees= 41
        )

        new_employee = Employee.objects.create(
            first_name = "Rob",
            last_name = "Boss",
            start_date = "2016-03-07 05:53:53",
            end_date = None,
            is_supervisor = 0,
            department_id = None,
        )

        join = EmployeeTraining.objects.create(
            employee = new_employee,
            training = new_training
        )

        response = self.client.get(reverse('agileHR:traindetail', args=(1,)))

        # Check that the response is 200 ok
        self.assertEqual(response.status_code, 200)

        # Test that the department name is in the HTML response content
        self.assertEqual(response.context['training_details'], new_training)

        # Training title appears in HTML response content
        self.assertIn(new_training.title.encode(), response.content)

        # Employee first name appears in HTML response content
        self.assertIn(new_employee.first_name.encode(), response.content)

    # def test_display_form(self):
    # Testing the display of the form
    # get assertin with input from template using .encode


    def test_new_training(self):
        future_date = datetime.now(tz=None)+ timedelta(days=2)
        response = self.client.post(reverse('agileHR:training_add'), {
            "title":"Test Training",
            "start_date": datetime.now(tz=None),
            "end_date": future_date,
            "max_attendees": 41
        })

        # status code is 302
        self.assertEqual(response.status_code, 302)



