from django.contrib.auth.models import User, AnonymousUser
from neomodel import EITHER
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from sptest.friends.models import Person, PersonRelationship
from sptest.friends.serializers import UserSerializer, PersonSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class PersonListView(APIView):
    def get(self, request, format=None):
        # default action - list all persons in graphdb with pagination, I think
        if not (request.query_params and 'email' in request.query_params):
            persons = Person.nodes.all()
            person_serializer = PersonSerializer(persons, many=True)
            return Response(person_serializer.data)
        else:
            email = request.query_params.get('email', None)
            if email is not None:
                # Running the validator on all the items in friends
                validation_result = self.validate_input_emails([email])
                if validation_result is not None:
                    return validation_result
                # Get the persons
                person_list = self.get_or_create_email_list([email])
                # We just need the first entry
                person = person_list[0]
                result = Person.get_all_relation_of_type(person, EITHER, PersonRelationship.FRIEND)
        return Response({"success": True})


    """
      Issue #01 - Link users
    """
    def post(self, request, format=None):
        # print(repr(request))
        # This is just to have a valid user in session
        request_user = AnonymousUser.id
        if hasattr(request, 'user') and request.user is not None:
            request_user = request.user
        # Figure out if how the request is represented
        if not (request.data and 'friends' in request.data):
            return Response(
                {'friends': [u'friends is not provided in body of request']},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        else:
            friends_email_list = set(request.data.get('friends', []))
            if len(friends_email_list) < 2:
                return Response(
                    {'friends': [u'number of friends not acceptable']},
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            # Running the validator on all the items in friends
            validation_result = self.validate_input_emails(friends_email_list)
            if validation_result is not None:
                return validation_result
            # Running the get_or_create function
            person_list = self.get_or_create_email_list(friends_email_list)
            # Connect every person up
            self.connect_person_list_as_friends(person_list)
        return Response({"success": True})

    def validate_input_emails(self, email_list):
        result = None
        errors = {}
        for email in email_list:
            errors.update(self.serialize_and_check_if_valid_person(email))
        if len(errors) > 0:
            result = Response(
                errors,
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        return result

    def serialize_and_check_if_valid_person(self, email):
        result = {}
        person_serializer = PersonSerializer(data={'email': email})
        if not person_serializer.is_valid():
            result.update(person_serializer.errors)
        return result

    def get_or_create_email_list(self, email_list):
        result = []
        for email in email_list:
            # person_get_or_create is a list
            persons_get_or_create = Person.get_or_create(
                {'email': email},
            )
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
