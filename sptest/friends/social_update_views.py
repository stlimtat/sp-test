import re

from django.contrib.auth.models import AnonymousUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sptest.friends.models import Person
from sptest.friends.serializers import SocialUpdateRequestSerializer
from sptest.friends.views import ViewUtilities


class SocialUpdateView(APIView):
    """
      Issue #04 - As a user, I need an API to subscribe to updates from an email address
    """

    @swagger_auto_schema(
        operation_description="Issue #06 - As a user I need an API to retrieve all email address that can receive updates from an email address",
        request_body=SocialUpdateRequestSerializer,
        responses={
            200: "Returns a JSON message with success: True and the list of receipients",
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
        if not request.data:
            result = {
                'success': False,
                'errors': {'friends': [u'friends is not provided in body of request']}
            }
            result_status = status.HTTP_406_NOT_ACCEPTABLE
        else:
            social_update_req_serializer = SocialUpdateRequestSerializer(data=request.data)
            if not social_update_req_serializer.is_valid():
                result = {
                    'success': False,
                    'errors': {'requestor': [u'requestor not found in db']}
                }
                result_status = status.HTTP_406_NOT_ACCEPTABLE
            else:
                sender_req = social_update_req_serializer.validated_data.get('sender')
                text_req = social_update_req_serializer.validated_data.get('text')
                if not sender_req:
                    result = {
                        'success': False,
                        'errors': {'sender': [u'sender not found in request']}
                    }
                    result_status = status.HTTP_406_NOT_ACCEPTABLE
                elif not text_req:
                    result = {
                        'success': False,
                        'errors': {'text': [u'text not found in request']}
                    }
                    result_status = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    sender_person = Person.nodes.get_or_none(sender_req)
                    if not sender_person:
                        result = {
                            'success': False,
                            'errors': {'duplicate': [u'requestor cannot be the same as target']}
                        }
                        result_status = status.HTTP_406_NOT_ACCEPTABLE
                    else:
                        # Issue #6b-03 - has been @mentioned in the update
                        email_re_match = re.findall(r'[\w\.-]+@[\w\.-]+', text_req)
                        mentioned_person_list = ViewUtilities.get_or_create_email_list(False, email_re_match)

                        # cypher query to search for all friends, merge with all subscribed who are not blocked
                        query = "MATCH (n:Person)-[:FRIEND|SUBSCRIBE]-(friend:Person) \
                                WHERE NOT (friend)-[:BLOCK]->(n) \
                                n.email='%s' \
                                RETURN DISTINCT friend.email \
                                ORDER BY friend.email ASC" % (sender_person.email)
                        query_result, meta = db.cypher_query(query)
                        result = {
                            'success': True,
                            'friends': query_result + mentioned_person_list
                        }

        return Response(result, status=result_status)
