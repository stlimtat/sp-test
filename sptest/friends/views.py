from django.contrib.auth.models import User
from rest_framework import viewsets, status

from sptest.friends.models import Person
from sptest.friends.serializers import UserSerializer, FriendsRequestSerializer, PersonSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


"""
Utility functions for reuse
"""
class ViewUtilities():
    @staticmethod
    def validate_friends_req_serializer_and_get_email_list(data, is_exactly_two):
        result = {}
        result_status = status.HTTP_200_OK
        friends_req_serializer = FriendsRequestSerializer(data=data)
        if not friends_req_serializer.is_valid():
            result = {
                'success': False,
                'errors': friends_req_serializer.errors
            }
            result_status = status.HTTP_406_NOT_ACCEPTABLE
        else:
            friends_email_list = set(friends_req_serializer.validated_data.get('friends'))
            if len(friends_email_list) < 2 or \
                    (is_exactly_two and len(friends_email_list) != 2):
                result = {
                    'success': False,
                    'errors': {'friends': [u'number of friends provided is not valid']}
                }
                result_status = status.HTTP_406_NOT_ACCEPTABLE
            result['friends'] = friends_email_list
        return result, result_status

    @staticmethod
    def serialize_and_check_if_valid_person(email):
        result = {}
        person_serializer = PersonSerializer(data={'email': email})
        if not person_serializer.is_valid():
            result.update(person_serializer.errors)
        return result

    @staticmethod
    def get_or_create_email_list(is_create, email_list):
        result = []
        email_set = set(email_list)
        for email in email_set:
            # person_get_or_create is a list
            if is_create:
                persons_get_or_create = Person.get_or_create(
                    {'email': email},
                )
            else:
                persons_get_or_create = Person.nodes.filter(email=email)
            if len(persons_get_or_create) > 0:
                result += persons_get_or_create
        return result

    @staticmethod
    def connect_person_list_as_friends(person_list):
        for current_person in person_list:
            person_list.remove(current_person)
            for looping_person in person_list:
                if not looping_person.friends.is_connected(current_person):
                    current_person.friends.connect(looping_person)
        return

    @staticmethod
    def get_emails_for_friends_response_list(person_list):
        result = set()
        for person in person_list:
            result.add(person.email)
        return result
