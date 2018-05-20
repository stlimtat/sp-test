from datetime import datetime

from django.forms import ModelForm
from django_neomodel import DjangoNode
from neomodel import StructuredRel, EmailProperty, DateTimeProperty, StringProperty, UniqueIdProperty, RelationshipTo, \
    Relationship


# Create your models here.
class PersonRelationship(StructuredRel):
    since = DateTimeProperty(default=datetime.utcnow())

class Person(DjangoNode):
    uid = UniqueIdProperty()
    email = EmailProperty(unique_index=True)
    friends = Relationship('Person', 'FRIEND', model=PersonRelationship)
    blocks = RelationshipTo('Person', 'BLOCK', model=PersonRelationship)
    # blocked_by = RelationshipFrom('Person', 'BLOCKED_BY')
    subscribes = RelationshipTo('Person', 'SUBSCRIBE', model=PersonRelationship)
    # subscribed_by = RelationshipFrom('Person', 'SUBSCRIBED_BY')

    created_by = StringProperty()
    created = DateTimeProperty(default=datetime.utcnow())
    modified_by = StringProperty()
    modified = DateTimeProperty(default=datetime.utcnow())

    class Meta:
        # fields = ('email', 'uid')
        app_label = 'friends'

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ('email', 'uid')
