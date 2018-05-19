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
        user4 = Person(email="user4@a.a").save()
        user5 = Person(email="user5@a.a").save()
        user6 = Person(email="user6@a.a").save()

        user1.friends.connect(user2)
        user1.friends.connect(user3)
        user3.blocks.connect(user1)
        user3.blocks.connect(user2)

    def test_get_all_user1_friends(self):
        user1 = Person.nodes.filter(email="user1@a.a")
        print ( repr(user1) )

        for person in user1.friends:
            print ( repr(person) )
