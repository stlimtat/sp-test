from django.test import SimpleTestCase
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from sptest.friends.models import Person
from sptest.friends.serializers import PersonSerializer, FriendsRequestSerializer
from sptest.friends.tests.test_models import PersonTestCase


class PersonSerializerTestCase(SimpleTestCase):
    def setUp(self):
        PersonTestCase.setup_models()
        self.persons = Person.nodes.all()

    def tearDown(self):
        PersonTestCase.teardown_models()

    def test_repr_serializer(self):
        serializer = PersonSerializer()
        print(repr(serializer))

    def test_serialize_persons(self):
        serializer = PersonSerializer(self.persons, many=True)
        self.assertIsNotNone(serializer.data)
        print(repr(serializer))
        print(repr(serializer.data))

    def test_serialize_person_user7(self):
        person = Person(email='user7@a.com')
        serializer = PersonSerializer(person)
        self.assertIsNotNone(serializer.data)
        print(repr(serializer.data))

    def test_serialize_person_user8(self):
        person = Person(email='user8@a.com')
        serializer = PersonSerializer(person)
        json = JSONRenderer().render(serializer.data)
        print(repr(json))
        stream = BytesIO(json)
        data = JSONParser().parse(stream)
        serializer = PersonSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        print(repr(serializer.data))

    def test_serialize_person_user9_invalid(self):
        serializer = PersonSerializer(data={'email': 'user9a.com'})
        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors)
        print(repr(serializer.errors))

    def test_serialize_friendsrequestserializer(self):
        serializer = FriendsRequestSerializer(data={
            'friends': ['user1@a.com', 'user2@a.com']
        })
        self.assertTrue(serializer.is_valid())

    def test_serialize_friendsrequestserializer_friends_fail(self):
        serializer = FriendsRequestSerializer(data={
            'notfriends': ['user1@a.com', 'user2@a.com']
        })
        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors)
        print(repr(serializer.errors))

    def test_serialize_friendsrequestserializer_email_fail(self):
        serializer = FriendsRequestSerializer(data={
            'friends': ['user1a.com', 'user2@a.com']
        })
        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors)
        print(repr(serializer.errors))
