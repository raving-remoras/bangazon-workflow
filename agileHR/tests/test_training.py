import unittest
from django.test import TestCase
from django.urls import reverse
from datetime import datetime, timedelta
from ..models import Training, Employee, EmployeeTraining

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

        # Check that the training title appears in the rendered HTML content
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

    def test_display_add_form(self):
        """Test case verifies that all required input fields have been correctly rendered when an add form is requested"""
        response = self.client.get(reverse('agileHR:training_add'))

        # Training title input field appears in HTML response content
        self.assertIn('<input type="text" class="form-control" name="training_title" value=""/>'.encode(), response.content)

        # Training start date input field appears in HTML response content
        self.assertIn('<input type="date" class="form-control" name="start_date" value=""/>'.encode(), response.content)

        # Training end date input field appears in HTML response content
        self.assertIn(' <input type="date" class="form-control" name="end_date" value=""/>'.encode(), response.content)

        # Training maximum attendees input field appears in HTML response content
        self.assertIn('<input type="number" class="form-control" name="max_attendees" value=""/>'.encode(), response.content)

    def test_new_training(self):
        """Test case verifies that when a POST operation is performed to the corresponding URL, a successful response is recieved."""
        future_date = datetime.now(tz=None)+ timedelta(days=2)

        response = self.client.post(reverse('agileHR:training_add'), {
            "title":"Test Training",
            "start_date": datetime.now(tz=None),
            "end_date": future_date,
            "max_attendees": 41
        })

        # Checks that the response is 200 ok
        self.assertEqual(response.status_code, 200)

    def test_display_edit_form(self):
        """Test case verifies that all required input fields have been correctly rendered when a edit form is requested"""
        future_date = datetime.now(tz=None)+ timedelta(days=2)

        new_training = Training.objects.create(
            title="Test Training",
            start_date= datetime.now(tz=None),
            end_date= future_date,
            max_attendees= 41
        )
        response = self.client.get(reverse('agileHR:training_edit', args=(1,)))

        # Training title input field appears in HTML response content
        self.assertIn('<input type="text" class="form-control" name="training_title" value="Test Training"/>'.encode(), response.content)

        # Training start date input field appears in HTML response content
        self.assertIn('<input type="date" class="form-control" name="start_date" value="'.encode(), response.content)

        # Training end date input field appears in HTML response content
        self.assertIn('<input type="date" class="form-control" name="end_date" value="'.encode(), response.content)

        # Training maximum attendees input field appears in HTML response content
        self.assertIn('<input type="number" class="form-control" name="max_attendees" value="41"/>'.encode(), response.content)


    def test_edit_training(self):
        """Test case verifies that when a PUT operation is performed to the corresponding URL, a successful response is recieved"""
        future_date = datetime.now(tz=None)+ timedelta(days=2)

        new_training = Training.objects.create(
            title="Test Training",
            start_date= datetime.now(tz=None),
            end_date= future_date,
            max_attendees= 41
        )

        response = self.client.get(reverse('agileHR:training_edit', args=(1,)))

        # Checks that the response is 200 ok
        self.assertEqual(response.status_code, 200)


class TrainingDeleteTest(TestCase):
    """Defines tests for Delete Training models and views

        Author: Brendan McCray

        Methods:
            test_delete_training
            test_delete_past_training
    """

    def test_delete_training(self):
        """Test case verifies that when a POST (delete) operation is performed to the corresponding URL (on an event with a future end date), a successful response is recieved"""
        future_date = datetime.now(tz=None) + timedelta(days=2)

        Training.objects.create(
            title="Test Training",
            start_date= datetime.now(tz=None),
            end_date= future_date,
            max_attendees= 41
        )

        response = self.client.get(reverse('agileHR:training_delete', args=(1,)))

        self.assertEqual(response.status_code, 200)

    # def test_delete_past_training(self):
    #     """Test case verifies that when a POST (delete) operation is performed on a past event, the server rejects the request"""

    #     past_date = datetime.now(tz=None) - timedelta(days=2)

    #     new_training = Training.objects.create(
    #         title="Test Training",
    #         start_date= datetime.now(tz=None),
    #         end_date= future_date,
    #         max_attendees= 41
    #     )

    #     response = self.client.get(reverse('agileHR:training_edit', args=(1,)))

    #     # Checks that the response is 200 ok
    #     self.assertEqual(response.status_code, 200)