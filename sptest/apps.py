from django.apps import AppConfig
from django.conf import settings
from neomodel import db, clear_neo4j_database

from sptest.friends.models import Person


class SptestConfig(AppConfig):
    name = 'sptest'
    verbose_name = "Friends Application"

    def ready(self):
        while not settings.NEOMODEL_NEO4J_BOLT_URL and not db:
            pass
        SptestConfig.setup_models()

    @staticmethod
    def setup_models():
        # Initialize the basic database for the application
        print(repr(db))
        print(repr(settings))
        clear_neo4j_database(db)
        user1 = Person.get_or_create(({'email': 'user1@a.com'}))
        user2 = Person.get_or_create(({'email': 'user2@a.com'}))
        user3 = Person.get_or_create(({'email': 'user3@a.com'}))
        user4 = Person.get_or_create(({'email': 'user4@a.com'}))
        user5 = Person.get_or_create(({'email': 'user5@a.com'}))
        user6 = Person.get_or_create(({'email': 'user6@a.com'}))

        user1.friends.connect(user2)
        user1.friends.connect(user3)
        user3.blocks.connect(user1)
        user3.blocks.connect(user2)
