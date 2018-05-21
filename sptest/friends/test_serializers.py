from django.test import SimpleTestCase

from sptest.friends.models import Person
from sptest.friends.serializers import PersonSerializer


class PersonSerializerTestCase(SimpleTestCase):
    def setUp(self):
        self.persons = Person.nodes.all()

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
