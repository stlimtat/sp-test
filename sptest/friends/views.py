from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from sptest.friends.models import Person
from sptest.friends.serializers import UserSerializer, PersonSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PersonDetailView(APIView):

    # GET Person by unique identifier (pk) - for geomodel there is no pk
    def get_object(self, pk):
        try:
            return Person.nodes.filter(uid=pk)
        except Person.DoesNotExist:
            print(_("Person with uuid '%(pk)' does not exists.") % {'pk': pk})

    def get(self, request, pk, format=None):
        person = self.get_object(self, pk)
        serializer = PersonSerializer(person)
        return JsonResponse(serializer.data)


class PersonListView(APIView):
    def get(self, request, format=None):
        persons = Person.nodes.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    """
      Issue #01 - Link users
    """
    def post(self, request, format=None):
        print(repr(request))
        # This is just to have a valid user in session
        request_user = 'unknown'
        if hasattr(request, 'user') and request.user is not None:
            request_user = request.user
        # Figure out if how the request is represented
        if not (request.data and 'friends' in request.data):
            return Response(
                {
                    'friends': [u'friends is not provided in body of request']
                },
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        else:
            friends_list = request.data.get('friends', [])
            if len(friends_list) < 2:
                return Response(
                    {
                        'friends': [u'number of friends not acceptable']
                    },
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            person_nodes = []
            errors = {}
            # The error parser for all the items in friends
            for friend_email in friends_list:
                serializer = PersonSerializer(data={'email': friend_email})
                if not serializer.is_valid():
                    errors.update(serializer.errors)
            if len(errors) > 0:
                return Response(
                    errors,
                    status=status.HTTP_406_NOT_ACCEPTABLE
                )
            for friend_email in friends_list:
                person = Person.get_or_create(
                    ({'email': friend_email})
                )
                if not person in person_nodes:
                    person_nodes += person
            for curr_person in person_nodes:
                person_nodes.remove(curr_person)
                for looping_person in person_nodes:
                    if not looping_person.friends.is_connected(curr_person):
                        curr_person.friends.connect(looping_person)
        return Response({"success": True})
