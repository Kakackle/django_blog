from blogapp.models import User
from blogapp.api.serializers import UserSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics

class UserListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)

class UserDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'