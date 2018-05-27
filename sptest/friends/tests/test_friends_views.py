from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, APIClient

from sptest.friends.friends_views import FriendsView
from sptest.friends.tests.test_models import PersonTestCase


class FriendsViewTestCase(SimpleTestCase):
    def setUp(self):
        PersonTestCase.setup_models()
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def tearDown(self):
        PersonTestCase.teardown_models()

    def test_get_issue00_persons_list_with_factory(self):
        request = self.factory.get('/friends/')
        print(repr(request))
        view = FriendsView.as_view()
        print(repr(view))
        self.assertIsNotNone(view)
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))

    def test_get_issue00_persons_list_with_client(self):
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
        print(repr(request))
        view = FriendsView.as_view()
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
        print(repr(request))
        view = FriendsView.as_view()
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
        print(repr(request))
        view = FriendsView.as_view()
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
        print(repr(request))
        view = FriendsView.as_view()
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
        print(repr(request))
        view = FriendsView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        print(response.status_code)
        self.assertTrue(status.is_success(response.status_code))

    def test_get_issue02_friends_by_email(self):
        data = {
            "email": "user1@a.com"
        }
        request = self.factory.get('/friends/', data, format='json')
        print(repr(request))
        view = FriendsView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))

    def test_get_issue02_friends_by_email_no_friend(self):
        data = {
            "email": "user4@a.com"
        }
        request = self.factory.get('/friends/', data, format='json')
        print(repr(request))
        view = FriendsView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))

    def test_get_issue03_common_friends(self):
        data = {
            "friends": [
                "user2@a.com",
                "user3@a.com"
            ]
        }
        request = self.factory.get('/friends/', data, format='json')
        print(repr(request))
        view = FriendsView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))

    def test_get_issue03_only_one_friend(self):
        data = {
            "friends": [
                "user2@a.com"
            ]
        }
        request = self.factory.get('/friends/', data, format='json')
        print(repr(request))
        view = FriendsView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_issue03_three_friends(self):
        data = {
            "friends": [
                "user1@a.com",
                "user2@a.com",
                "user3@a.com"
            ]
        }
        request = self.factory.get('/friends/', data, format='json')
        print(repr(request))
        view = FriendsView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_get_issue05_trying_to_friend_blocked(self):
        data = {
            "friends": [
                "user5@a.com",
                "user1@a.com"
            ]
        }
        request = self.factory.get('/friends/', data, format='json')
        print(repr(request))
        view = FriendsView.as_view()
        response = view(request)
        self.assertIsNotNone(response)
        print(repr(response))
        self.assertIsNotNone(response.data)
        print(repr(response.data))
        self.assertTrue(status.is_success(response.status_code))
