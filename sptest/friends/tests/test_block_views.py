from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient

from sptest.friends.block_views import BlockView
from sptest.friends.tests.test_models import PersonTestCase


class BlockViewTestCase(SimpleTestCase):
    def setUp(self):
        PersonTestCase.setup_models()
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def tearDown(self):
        PersonTestCase.teardown_models()

    def test_get_issue05_happy(self):
        data = {
            "requestor": "user4@a.com",
            "target": "user5@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = BlockView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))

    def test_get_issue05_requestor_no_target(self):
        data = {
            "requestor": "user4@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = BlockView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_issue05_target_no_requestor(self):
        data = {
            "target": "user4@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = BlockView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_issue05_multirequestor(self):
        data = {
            "requestor": "user4@a.com",
            "requestor": "user5@a.com",
            "target": "user6@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = BlockView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))

    def test_get_issue05_requestor_target_same(self):
        data = {
            "requestor": "user4@a.com",
            "target": "user4@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = BlockView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_issue05_invalid_requestor(self):
        data = {
            "requestor": "user99@a.com",
            "target": "user4@a.com"
        }
        request = self.factory.post('/subscribe/', data, format='json')
        print(repr(request))
        view = BlockView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
