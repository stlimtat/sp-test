from datetime import datetime

from django.forms import ModelForm
from django_neomodel import DjangoNode
from neomodel import StructuredRel, EmailProperty, DateTimeProperty, StringProperty, RelationshipTo, \
    Relationship, Traversal


# Create your models here.
class PersonRelationship(StructuredRel):
    since = DateTimeProperty(default=datetime.utcnow())

    _FRIEND = 'FRIEND'
    _BLOCK = 'BLOCK'
    _SUBSCRIBE = 'SUBSCRIBE'

    @property
    def FRIEND(self):
        return type(self)._FRIEND

    @property
    def BLOCK(self):
        return type(self)._BLOCK

    @property
    def SUBSCRIBE(self):
        return type(self)._SUBSCRIBE


class Person(DjangoNode):
    email = EmailProperty(unique_index=True)
    friends = Relationship('Person', PersonRelationship.FRIEND, model=PersonRelationship)
    blocks = RelationshipTo('Person', PersonRelationship.BLOCK, model=PersonRelationship)
    # blocked_by = RelationshipFrom('Person', 'BLOCKED_BY')
    subscribes = RelationshipTo('Person', PersonRelationship.SUBSCRIBE, model=PersonRelationship)
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

    class Meta:
        # fields = ('email')
        app_label = 'friends'

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('email',)
