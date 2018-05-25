from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient

from sptest.friends.subscribe_views import SubscribeView
from sptest.friends.test_models import PersonTestCase


class SubscribeViewTestCase(SimpleTestCase):
    def setUp(self):
        PersonTestCase.setup_models()
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def tearDown(self):
        pass
        PersonTestCase.teardown_models()

    def test_get_issue04_happy(self):
        data = {
            "requestor": "user4@a.com",
            "target": "user5@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = SubscribeView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))

    def test_get_issue04_requestor_no_target(self):
        data = {
            "requestor": "user4@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = SubscribeView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_issue04_target_no_requestor(self):
        data = {
            "target": "user4@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = SubscribeView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_issue04_multirequestor(self):
        data = {
            "requestor": "user4@a.com",
            "requestor": "user5@a.com",
            "target": "user6@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = SubscribeView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))

    def test_get_issue04_requestor_target_same(self):
        data = {
            "requestor": "user4@a.com",
            "target": "user4@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = SubscribeView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_issue04_invalid_requestor(self):
        data = {
            "requestor": "user99@a.com",
            "target": "user4@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = SubscribeView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
