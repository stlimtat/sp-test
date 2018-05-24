from django.contrib.auth.models import AnonymousUser
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sptest.friends.models import Person
from sptest.friends.serializers import RequestorTargetRequestSerializer
from sptest.friends.views import ViewUtilities


class SubscribeView(APIView):
    """
      Issue #04 - As a user, I need an API to subscribe to updates from an email address
    """

    @swagger_auto_schema(
        operation_description="Issue #04 - As a user, I need an API to subscribe to updates from an email address",
        request_body=RequestorTargetRequestSerializer,
        responses={
            200: "Depends on input, either returns a list of friends with count",
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
            result, result_status = ViewUtilities.validate_req_tgt_req_serializer(request.data)
            if result_status == status.HTTP_200_OK:
                requestor = Person.nodes.get_or_none(email=result.get('requestor'))
                target = Person.nodes.get_or_none(email=result.get('target'))
                if not requestor:
                    result = {
                        'success': False,
                        'errors': {'requestor': [u'requestor not found in db']}
                    }
                    result_status = status.HTTP_406_NOT_ACCEPTABLE
                elif not target:
                    result = {
                        'success': False,
                        'errors': {'target': [u'target not found in db']}
                    }
                    result_status = status.HTTP_406_NOT_ACCEPTABLE
                elif requestor.email == target.email:
                    result = {
                        'success': False,
                        'errors': {'duplicate': [u'requestor cannot be the same as target']}
                    }
                    result_status = status.HTTP_406_NOT_ACCEPTABLE
                else:
                    requestor.subscribes.connect(target)
        return Response(result, status=result_status)
