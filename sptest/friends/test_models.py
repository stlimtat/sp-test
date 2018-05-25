from django.test import TestCase
from neomodel import db, clear_neo4j_database

from sptest.friends.models import Person


# Create your tests here.
# By extending TestCase, this should run first
class PersonTestCase(TestCase):
    @staticmethod
    def setup_models():
        # Initialize the basic database for the application
        clear_neo4j_database(db)
        users = Person.get_or_create(
            ({'email': 'user1@a.com'}),
            ({'email': 'user2@a.com'}),
            ({'email': 'user3@a.com'}),
            ({'email': 'user4@a.com'}),
            ({'email': 'user5@a.com'}),
            ({'email': 'user6@a.com'}),
            ({'email': 'user7@a.com'}),
            ({'email': 'user8@a.com'}),
            ({'email': 'user9@a.com'}),
            ({'email': 'user0@a.com'})
        )

        users[0].friends.connect(users[1])
        users[0].friends.connect(users[2])
        users[0].friends.connect(users[3])
        users[0].friends.connect(users[4])
        users[4].blocks.connect(users[0])
        users[4].blocks.connect(users[5])
        users[6].subscribes.connect(users[0])
        users[6].subscribes.connect(users[7])


    @staticmethod
    def teardown_models():
        clear_neo4j_database(db)

    def setUp(self):
        PersonTestCase.setup_models()

    def tearDown(self):
        PersonTestCase.teardown_models()

    def test_get_all_user1_friends(self):
        user1 = Person.nodes.filter(email="user1@a.a")
        print ( repr(user1) )

        for person in user1.friends:
            print ( repr(person) )
