from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory, APIClient

from sptest.apps import SptestConfig
from sptest.friends.test_models import PersonTestCase
from sptest.friends.views import PersonListView


class PersonListViewTestCase(SimpleTestCase):
    def setUp(self):
        SptestConfig.setup_models()
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def tearDown(self):
        PersonTestCase.teardown_models()

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
        self.assertIsNotNone(response.data)
        print(repr(response.data))
