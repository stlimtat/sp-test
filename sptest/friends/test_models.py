from django.test import TestCase
from neomodel import db, clear_neo4j_database

from sptest.apps import SptestConfig
from sptest.friends.models import Person


# Create your tests here.
# By extending TestCase, this should run first
class PersonTestCase(TestCase):
    @staticmethod
    def teardown_models():
        clear_neo4j_database(db)

    def setUp(self):
        SptestConfig.setup_models()

    def tearDown(self):
        PersonTestCase.teardown_models()

    def test_get_all_user1_friends(self):
        user1 = Person.nodes.filter(email="user1@a.a")
        print ( repr(user1) )

        for person in user1.friends:
            print ( repr(person) )
