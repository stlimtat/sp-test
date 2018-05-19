from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User, Group
from sptest.friends.serializers import UserSerializer, GroupSerializer, PersonSerializer

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
