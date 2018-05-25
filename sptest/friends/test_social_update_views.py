from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient

from sptest.friends.social_update_views import SocialUpdateView
from sptest.friends.test_models import PersonTestCase


class SocialUpdateViewTestCase(SimpleTestCase):
    def setUp(self):
        PersonTestCase.setup_models()
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def tearDown(self):
        # PersonTestCase.teardown_models()
        pass

    def test_get_issue06_happy(self):
        data = {
            "sender": "user1@a.com",
            "text": "Testing"
        }
        request = self.factory.post('/social-update/', data, format='json')
        print(repr(request))
        view = SocialUpdateView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))

    def test_get_issue06_sender_no_text(self):
        data = {
            "sender": "user1@a.com"
        }
        request = self.factory.post('/social-update/', data, format='json')
        print(repr(request))
        view = SocialUpdateView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_issue06_text_no_sender(self):
        data = {
            "text": "Text"
        }
        request = self.factory.post('/social-update/', data, format='json')
        print(repr(request))
        view = SocialUpdateView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_issue06_text_mention_blockers(self):
        data = {
            "sender": "user1@a.com",
            "text": "user5@a.com,user6@a.com,user9@a.com"
        }
        request = self.factory.post('/social-update/', data, format='json')
        print(repr(request))
        view = SocialUpdateView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))

    def test_get_issue06_invalid_sender(self):
        data = {
            "requestor": "user99@a.com",
            "target": "user4@a.com"
        }
        request = self.factory.post('/social-update/', data, format='json')
        print(repr(request))
        view = SocialUpdateView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
