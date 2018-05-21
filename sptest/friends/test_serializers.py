from django.test import SimpleTestCase

from sptest.apps import SptestConfig
from sptest.friends.models import Person
from sptest.friends.serializers import PersonSerializer
from sptest.friends.test_models import PersonTestCase


class PersonSerializerTestCase(SimpleTestCase):
    def setUp(self):
        SptestConfig.setup_models()
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
        person = Person(email='user7@a.a')
        serializer = PersonSerializer(person)
        self.assertIsNotNone(serializer.data)
        print(repr(serializer.data))

    def test_serialize_person_user8_invalid(self):
        serializer = PersonSerializer(data={'email': 'user8@a.a'})
        self.assertFalse(serializer.is_valid())
        self.assertIsNotNone(serializer.errors)
        print(repr(serializer.errors))
