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
        response = view(request)
        print(repr(response))

    def test_get_persons_list_with_client(self):
        response = self.client.get('/friends/')
