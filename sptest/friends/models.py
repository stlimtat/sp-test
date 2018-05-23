from datetime import datetime

from django.forms import ModelForm
from django_neomodel import DjangoNode
from neomodel import StructuredRel, EmailProperty, DateTimeProperty, StringProperty, RelationshipTo, \
    Relationship, Traversal
from neomodel import db


# Create your models here.
class PersonRelationship(StructuredRel):
    since = DateTimeProperty(default=datetime.utcnow())

    _FRIEND = 'FRIEND'
    _BLOCK = 'BLOCK'
    _SUBSCRIBE = 'SUBSCRIBE'

class Person(DjangoNode):
    email = EmailProperty(unique_index=True)
    friends = Relationship('Person', PersonRelationship._FRIEND, model=PersonRelationship)
    blocks = RelationshipTo('Person', PersonRelationship._BLOCK, model=PersonRelationship)
    # blocked_by = RelationshipFrom('Person', 'BLOCKED_BY')
    subscribes = RelationshipTo('Person', PersonRelationship._SUBSCRIBE, model=PersonRelationship)
    # subscribed_by = RelationshipFrom('Person', 'SUBSCRIBED_BY')

    created_by = StringProperty()
    created = DateTimeProperty(default=datetime.utcnow())
    modified_by = StringProperty()
    modified = DateTimeProperty(default=datetime.utcnow())

    # Get all the Person of relation_type of relation_direction
    @staticmethod
    def get_all_relation_of_type(person, relation_direction, relation_type):
        result = []
        traversal_definition = dict(
            node_class=Person,
            direction=relation_direction,
            relation_type=relation_type,
            model=None
        )
        relations_traversal = Traversal(
            person,
            Person.__label__,
            traversal_definition
        )
        result = relations_traversal.all()
        return result

    # Get all the friends for a list of person nodes
    @staticmethod
    def get_common_friends(person_list):
        result = []
        # We don't really know how to handle more than 2 persons at the moment
        query = "MATCH (n:Person)-[:FRIEND]-(friend:Person)-[:FRIEND]-(m:Person) \
                WHERE n.email='%s' \
                AND m.email='%s' \
                RETURN DISTINCT friend.email \
                ORDER BY friend.email ASC" % (person_list[0].email, person_list[1].email)
        result, meta = db.cypher_query(query)
        # We do not need to run the inflate method
        return result

    class Meta:
        # fields = ('email')
        app_label = 'friends'

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('email',)
