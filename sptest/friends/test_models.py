from django.test import TestCase
from neomodel import db, clear_neo4j_database
from sptest.friends.models import Person

# Create your tests here.
class PersonTestCase(TestCase):
    def setUp(self):
        # Do nothing for the moment
        clear_neo4j_database(db)
        user1 = Person(email="user1@a.a").save()
        user2 = Person(email="user2@a.a").save()
        user3 = Person(email="user3@a.a").save()

        user1.friends.connect(user2)
        user2.friends.connect(user3)
        user3.blocks.connect(user1)

    def test_get_all_user2_friends(self):
        user2 = Person.nodes.filter(email="user2@a.a")

        for person in user2.friends:
            print ( repr(person) )
