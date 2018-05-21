from django.apps import AppConfig
from neomodel import db, clear_neo4j_database

from sptest.friends.models import Person


class SptestConfig(AppConfig):
    name = 'sptest'
    verbose_name = "Friends Application"

    def ready(self):
        SptestConfig.setup_models()

    @staticmethod
    def setup_models():
        # Initialize the basic database for the application
        clear_neo4j_database(db)
        user1 = Person(email="user1@a.com").save()
        user2 = Person(email="user2@a.com").save()
        user3 = Person(email="user3@a.com").save()
        user4 = Person(email="user4@a.com").save()
        user5 = Person(email="user5@a.com").save()
        user6 = Person(email="user6@a.com").save()

        user1.friends.connect(user2)
        user1.friends.connect(user3)
        user3.blocks.connect(user1)
        user3.blocks.connect(user2)
