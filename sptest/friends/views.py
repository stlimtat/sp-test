from django.contrib.auth.models import User
from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import viewsets, generics
from rest_framework.views import APIView

from sptest.friends.models import Person
from sptest.friends.serializers import UserSerializer, PersonSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PersonDetailView(APIView):

    # GET Person by unique identifier (pk)
    def get_object(self, pk):
        try:
            return Person.nodes.filter(uid=pk)
        except Person.DoesNotExist:
            print(_("Person with uuid '%(pk)' does not exists.") % {'pk': pk})

    def get(self, request, pk, format=None):
        person = self.get_object(self, pk)
        serializer = PersonSerializer(person)
        return JsonResponse(serializer.data)


class PersonListView(generics.ListCreateAPIView):
    queryset = Person.nodes.all()
    serializer_class = PersonSerializer


"""
class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.nodes.all()
    lookup_field = "email"
    serializer_class = PersonSerializer

    # GET Person by unique identifier (pk)
    def get_object(self, pk):
        try:
            return Person.nodes.filter(uid=pk)
        except Person.DoesNotExist:
            print ( _("Person with uuid '%(pk)' does not exists.") % { 'pk': pk } )
"""
