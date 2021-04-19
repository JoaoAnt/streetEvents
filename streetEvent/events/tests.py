from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from events.models import Event
from rest_framework.test import APIRequestFactory

class ModelTestCase(TestCase):
    """This class defines the test suite for the event model."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="nerd")
        self.description = "Write world class code"
        # specify owner of a event
        self.event = Event(description=self.description, owner=user)

    def test_model_can_create_a_event(self):
        """Test the event model can create a event."""
        old_count = Event.objects.count()
        self.event.save()
        new_count = Event.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewsTestCase(TestCase):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        user = User.objects.create(username="nerd")

        # Initialize client and force it to use authentication
        self.client = APIClient()
        self.client.force_authenticate(user=user)

        # Since user model instance is not serializable, use its Id/PK
        self.event_data = {'description': 'Go to Ibiza', 'owner': user.id}
        self.response = self.client.post('/events/', self.event_data, format='json')

    def test_api_can_create_a_event(self):
        """Test the api has creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_not_needed_get(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get('/events/', kwargs={'pk': 3}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)


    def test_authorization_needed_post2(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.post('/events/', kwargs={'pk': 3, 'description':'Nothing special'}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorization_needed_post(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        user = User.objects.create(username="nerd3")
        res = new_client.post('/events/', kwargs={'pk': 3, 'description':'Nothing special', 'state': 'VALIDATED', 'owner': user.id}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
