from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient

from sptest.friends.views import PersonListView


class PersonListViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_get_persons_list_with_factory(self):
        request = self.factory.get('/friends/')
        print(repr(request))
        view = PersonListView.as_view()
        print(repr(view))
        self.assertIsNotNone(view)
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))

    def test_get_persons_list_with_client(self):
        print("Running client")
        response = self.client.get('/friends/')
        print(repr(response))

    def test_post_issue01(self):
        data = {
            "friends": {
                "andy@example.com",
                "john@example.com"
            }
        }
        request = self.factory.post('/friends/', data, format='json')
        view = PersonListView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
