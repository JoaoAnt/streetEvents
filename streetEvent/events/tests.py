from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from .models import Event
from django.contrib.auth.models import User


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

    def test_model_returns_readable_representation(self):
        """Test a readable string is returned for the model instance."""
        self.assertEqual(str(self.event), self.description)


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
        self.response = self.client.post(
            reverse('create'),
            self.event_data,
            format="json")

    def test_api_can_create_a_event(self):
        """Test the api has bucket creation capability."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_is_enforced(self):
        """Test that the api has user authorization."""
        new_client = APIClient()
        res = new_client.get('/events/', kwargs={'pk': 3, 'state': 'VALIDATED'}, format="json")
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_get_a_event(self):
        """Test the api can get a given event."""
        event = Event.objects.get(id=1)
        response = self.client.get(
            '/events/',
            kwargs={'pk': event.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, event)

    def test_api_can_update_event(self):
        """Test the api can update a given event."""
        event = Event.objects.get()
        change_event = {'description': 'Something new'}
        res = self.client.put(
            reverse('details', kwargs={'pk': event.id}),
            change_event, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_event(self):
        """Test the api can delete a event."""
        event = Event.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': event.id}),
            format='json',
            follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
