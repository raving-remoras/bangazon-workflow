import unittest
from django.test import TestCase
from django.urls import reverse
from ..models import Training
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
        future_date = datetime.now(tz=None)+ timedelta(days=2)
        training = Training.objects.create(
            title="Test Training",
            start_date= datetime.now(tz=None),
            end_date= future_date,
            max_attendees= 41
        )

        response = self.client.get(reverse('agileHR:traindetail', args=(1,)))
        self.assertEqual(response.context["training"].title, "Test Training")