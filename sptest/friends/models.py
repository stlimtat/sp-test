from datetime import datetime
from django_neomodel import DjangoNode
from neomodel import StructuredNode, EmailProperty, DateTimeProperty, StringProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom, Relationship

# Create your models here.
class Person(DjangoNode):
    uid = UniqueIdProperty()
    email = EmailProperty(unique_index=True)
    friends = Relationship('Person', 'FRIEND')
    blocks = RelationshipTo('Person', 'BLOCK')
    # blocked_by = RelationshipFrom('Person', 'BLOCKED_BY')
    subscribes = RelationshipTo('Person', 'SUBSCRIBE')
    # subscribed_by = RelationshipFrom('Person', 'SUBSCRIBED_BY')

    created_by = StringProperty()
    created = DateTimeProperty(default=datetime.utcnow())
    modified_by = StringProperty()
    modified = DateTimeProperty(default=datetime.utcnow())

    class Meta:
        app_label = 'friends'