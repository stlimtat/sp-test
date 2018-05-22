from django.contrib.auth.models import AnonymousUser
from neomodel import EITHER
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from sptest.friends.models import Person, PersonRelationship
from sptest.friends.serializers import *


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class PersonListView(APIView):
    def get(self, request, format=None):
        result = None
        result_status = status.HTTP_200_OK
        # default action - list all persons in graphdb with pagination, I think
        if not (request.query_params and 'email' in request.query_params):
            persons = Person.nodes.all()
            result_person_list = self.get_emails_for_friends_response_list(persons)
            result = FriendsResponseSerializer({
                'success': True,
                'friends': result_person_list,
                'count': len(result_person_list)
            })
        else:
            # GET friends for the person specified
            email_req_serializer = EmailRequestSerializer(data=request.query_params)
            if not email_req_serializer.is_valid():
                result = SuccessResponseSerializer({
                    'success': False,
                    'errors': email_req_serializer.errors
                })
                result_status = status.HTTP_406_NOT_ACCEPTABLE
            else:
                # Get the persons
                email = email_req_serializer.data.get('email')
                person_list = self.get_or_create_email_list(False, [email])
                # We just need the first entry
                person = person_list[0]
                friends = Person.get_all_relation_of_type(person, EITHER, PersonRelationship.FRIEND)
                result_friends_list = self.get_emails_for_friends_response_list(friends)
                result = FriendsResponseSerializer({
                    'success': True,
                    'friends': result_friends_list,
                    'count': len(result_friends_list)
                })
        return Response(result.data, status=result_status)


    """
      Issue #01 - Link users
    """
    def post(self, request, format=None):
        result = SuccessResponseSerializer({
            'success': True
        })
        result_status = status.HTTP_200_OK
        # This is just to have a valid user in session
        request_user = AnonymousUser.id
        if hasattr(request, 'user') and request.user is not None:
            request_user = request.user
        # Figure out if how the request is represented
        if not (request.data and 'friends' in request.data):
            result = ErrorResponseSerializer({
                'success': False,
                'errors': {'friends': [u'friends is not provided in body of request']}
            })
            result_status = status.HTTP_406_NOT_ACCEPTABLE
        else:
            friends_req_serializer = FriendsRequestSerializer(data=request.data)
            if not friends_req_serializer.is_valid():
                result = ErrorResponseSerializer({
                    'success': False,
                    'errors': friends_req_serializer.errors
                })
                result_status = status.HTTP_406_NOT_ACCEPTABLE
            else:
                # Running the get_or_create function
                friends_email_list = set(friends_req_serializer.validated_data.get('friends'))
                if len(friends_email_list) < 2:
                    result = ErrorResponseSerializer({
                        'success': False,
                        'errors': {'friends': [u'number of friends provided is not valid']}
                    })
                    result_status = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    person_list = self.get_or_create_email_list(True, friends_email_list)
                    # Connect every person up
                    self.connect_person_list_as_friends(person_list)
        return Response(result.data, status=result_status)

    def serialize_and_check_if_valid_person(self, email):
        result = {}
        person_serializer = PersonSerializer(data={'email': email})
        if not person_serializer.is_valid():
            result.update(person_serializer.errors)
        return result

    def get_or_create_email_list(self, is_create, email_list):
        result = []
        for email in email_list:
            # person_get_or_create is a list
            if is_create:
                persons_get_or_create = Person.get_or_create(
                    {'email': email},
                )
            else:
                persons_get_or_create = Person.nodes.filter(email=email)
            if not persons_get_or_create[0] in result:
                result += persons_get_or_create
        return result

    def connect_person_list_as_friends(self, person_list):
        for current_person in person_list:
            person_list.remove(current_person)
            for looping_person in person_list:
                if not looping_person.friends.is_connected(current_person):
                    current_person.friends.connect(looping_person)
        return

    def get_emails_for_friends_response_list(self, person_list):
        result = set()
        for person in person_list:
            result.add(person.email)
        return result
