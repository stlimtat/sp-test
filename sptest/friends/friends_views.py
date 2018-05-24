from django.contrib.auth.models import AnonymousUser
from neomodel import EITHER
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sptest.friends.models import Person, PersonRelationship
from sptest.friends.serializers import *
from sptest.friends.views import ViewUtilities


class FriendsView(APIView):
    '''
      Issue #0 - Get all recorded friends
      Issue #2 - As a user, I need an API to retrieve the friends list for an email address
      Issue #3 - As a user, I need an API to retrieve the common friends list between two email addresses
    '''
    def get(self, request, format=None):
        result = None
        result_status = status.HTTP_200_OK
        if request.query_params and 'email' in request.query_params:
            # Handling Issue #02 still in GET
            # GET friends for the email specified
            email_req_serializer = EmailRequestSerializer(data=request.query_params)
            if not email_req_serializer.is_valid():
                result = {
                    'success': False,
                    'errors': email_req_serializer.errors
                }
                result_status = status.HTTP_406_NOT_ACCEPTABLE
            else:
                # Get the persons
                email = email_req_serializer.data.get('email')
                person_list = ViewUtilities.get_or_create_email_list(False, [email])
                # We just need the first entry
                person = person_list[0]
                friends = Person.get_all_relation_of_type(person, EITHER, PersonRelationship._FRIEND)
                result_friends_list = ViewUtilities.get_emails_for_friends_response_list(friends)
                result = {
                    'success': True,
                    'friends': result_friends_list,
                    'count': len(result_friends_list)
                }
        # Handling Issue #03 still in GET
        elif request.query_params and 'friends' in request.query_params:
            result, result_status = ViewUtilities.validate_friends_req_serializer_and_get_email_list(
                request.query_params, True)
            if result_status == status.HTTP_200_OK:
                person_list = ViewUtilities.get_or_create_email_list(False, result.get('friends'))
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
        else:
            persons = Person.nodes.all()
            result_person_list = ViewUtilities.get_emails_for_friends_response_list(persons)
            result = {
                'success': True,
                'friends': result_person_list,
                'count': len(result_person_list)
            }
        return Response(result, status=result_status)


    """
      Issue #1 - As a user, I need an API to create a friend connection between two email addresses
    """
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
