from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


"""
class PersonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PersonForm
        fields = ('email')
"""


class PersonSerializer(serializers.Serializer):
    email = serializers.EmailField()
