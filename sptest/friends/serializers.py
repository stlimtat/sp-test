from django.contrib.auth.models import User, Group
from django.core.validators import EmailValidator
from rest_framework import serializers

from sptest.friends.models import PersonForm


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PersonFormSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PersonForm
        fields = ('email', 'uid')


class PersonSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[EmailValidator]
    )


class FriendsRequestSerializer(serializers.Serializer):
    friends = serializers.ListField(child=serializers.EmailField())
