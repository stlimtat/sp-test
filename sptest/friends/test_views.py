from django.test import SimpleTestCase
from rest_framework import status
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
            "friends": [
                "andy01@example.com",
                "john01@example.com"
            ]
        }
        request = self.factory.post('/friends/', data, format='json')
        view = PersonListView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))

    def test_post_issue01_invalid_friends(self):
        data = {
            "misspelt": [
                "andy02@example.com",
                "john02@example.com"
            ]
        }
        request = self.factory.post('/friends/', data, format='json')
        view = PersonListView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_post_issue01_invalid_emails(self):
        data = {
            "friends": [
                "andy03example.com",
                "john03example.com"
            ]
        }
        request = self.factory.post('/friends/', data, format='json')
        view = PersonListView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_post_issue01_all_repeated_emails(self):
        data = {
            "friends": [
                "andy04@example.com",
                "andy04@example.com",
                "andy04@example.com"
            ]
        }
        request = self.factory.post('/friends/', data, format='json')
        view = PersonListView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_post_issue01_ten_emails(self):
        data = {
            "friends": [
                "user20@example.com",
                "user21@example.com",
                "user22@example.com",
                "user23@example.com",
                "user24@example.com",
                "user25@example.com",
                "user26@example.com",
                "user27@example.com",
                "user28@example.com",
                "user29@example.com"
            ]
        }
        request = self.factory.post('/friends/', data, format='json')
        view = PersonListView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))
