from django.apps import AppConfig
from neomodel import db, clear_neo4j_database

from sptest.friends.models import Person


class SptestConfig(AppConfig):
    name = 'sptest'
    verbose_name = "Friends Application"

    def ready(self):
        pass

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
            ({'email': 'user6@a.com'})
        )

        users[0].friends.connect(users[1])
        users[0].friends.connect(users[2])
        users[0].friends.connect(users[3])
        users[2].blocks.connect(users[0])
        users[2].blocks.connect(users[1])
