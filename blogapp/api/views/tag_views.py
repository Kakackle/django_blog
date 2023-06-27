from blogapp.models import Tag
from blogapp.api.serializers import TagSerializer, TagSerializerSlug
from rest_framework import generics

class TagListAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializerSlug

class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializerSlug
    lookup_field='slug'