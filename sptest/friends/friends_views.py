from django.contrib.auth.models import AnonymousUser
from drf_yasg.utils import swagger_auto_schema
from neomodel import EITHER
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sptest.friends.models import Person, PersonRelationship
from sptest.friends.serializers import *
from sptest.friends.views import ViewUtilities


class FriendsView(APIView):
    """
      Issue #0 - Get all recorded friends
      Issue #2 - As a user, I need an API to retrieve the friends list for an email address
      Issue #3 - As a user, I need an API to retrieve the common friends list between two email addresses
    """
    @swagger_auto_schema(
        operation_description="Issue #0 - Get all recorded friends<br/>\
            Issue #2 - As a user, I need an API to retrieve the friends list for an email address <br/>\
            Issue #3 - As a user, I need an API to retrieve the common friends list between two email addresses",
        query_serializer=EmailOrFriendsRequestSerializer,
        responses={
            200: "Depends on input, either returns a list of friends with count",
            406: "Errors due to errors in the input parameters, either not validated as emails, or insufficient numbers of emails"
        }
    )
    def get(self, request, format=None):
        result = None
        result_status = status.HTTP_200_OK
        if request.query_params:
            email_or_friends_req_serializer = EmailOrFriendsRequestSerializer(data=request.query_params)
            if not email_or_friends_req_serializer.is_valid():
                result = {
                    'success': False,
                    'errors': email_or_friends_req_serializer.errors
                }
                result_status = status.HTTP_406_NOT_ACCEPTABLE
            else:
                # Handling Issue #02 get the friends of person
                email = email_or_friends_req_serializer.validated_data.get('email')
                friends = set(email_or_friends_req_serializer.validated_data.get('friends'))
                if email:
                    person = Person.nodes.get_or_none(email=email)
                    # We just need the first entry
                    friends = Person.get_all_relation_of_type(person, EITHER, PersonRelationship._FRIEND)
                    result_friends_list = ViewUtilities.get_emails_for_friends_response_list(friends)
                    result = {
                        'success': True,
                        'friends': result_friends_list,
                        'count': len(result_friends_list)
                    }
                # Handling Issue #03 still in GET
                elif friends:
                    if len(friends) != 2:
                        result = {
                            'success': False,
                            'errors': {'friends': [u'number of friends provided is not valid']}
                        }
                        result_status = status.HTTP_406_NOT_ACCEPTABLE
                    else:
                        person_list = ViewUtilities.get_or_create_email_list(False, friends)
                        if len(person_list) != 2:
                            result = {
                                'success': False,
                                'errors': {'friends': [u'number of friends provided is not valid']}
                            }
                            result_status = status.HTTP_406_NOT_ACCEPTABLE
                        else:
                            # Figure out the friends of the members of person_list
                            result_friends_list = Person().get_common_friends(person_list)
                            result = {
                                'success': True,
                                'friends': result_friends_list,
                                'count': len(result_friends_list)
                            }
        # default action - list all persons in graphdb with pagination, I think
        if not result:
            persons = Person.nodes.all()
            result_person_list = ViewUtilities.get_emails_for_friends_response_list(persons)
            result = {
                'success': True,
                'friends': result_person_list,
                'count': len(result_person_list)
            }
        return Response(result, status=result_status)

    """
        Issue #01 - As a user, I need an API to create a friend connection between two email addresses
    """

    @swagger_auto_schema(
        operation_description="Issue #01 - As a user, I need an API to create a friend connection between two email addresses",
        request_body=FriendsRequestSerializer,
        responses={
            200: "Email addresses created and connected as friends",
            406: "Errors due to errors in the input parameters, either not validated as emails, or insufficient numbers of emails"
        }
    )
    def post(self, request, format=None):
        result = {
            'success': True
        }
        result_status = status.HTTP_200_OK
        # This is just to have a valid user in session
        request_user = AnonymousUser.id
        if hasattr(request, 'user') and request.user is not None:
            request_user = request.user
        # Figure out if how the request is represented
        if not request.data or 'friends' not in request.data:
            result = {
                'success': False,
                'errors': {'friends': [u'friends is not provided in body of request']}
            }
            result_status = status.HTTP_406_NOT_ACCEPTABLE
        else:
            result, result_status = ViewUtilities.validate_friends_req_serializer_and_get_email_list(request.data,
                                                                                                     False)
            if result_status == status.HTTP_200_OK:
                person_list = ViewUtilities.get_or_create_email_list(True, result.get('friends'))
                # Connect every person up
                ViewUtilities.connect_person_list_as_friends(person_list)
        return Response(result, status=result_status)
