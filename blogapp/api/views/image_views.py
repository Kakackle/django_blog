from blogapp.models import Post, ImagePost
from blogapp.api.serializers import PostImageSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404

@api_view(['GET', 'POST'])
def post_image_view(request, slug):
    image = Post.objects.get(slug=slug).img
    return HttpResponse(image, content_type="image/jpg")

class ImagePostListAPIView(generics.ListCreateAPIView):
    # queryset = ImagePost.objects.all(post)
    # queryset = Post.objects.all().images
    serializer_class=PostImageSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        queryset = ImagePost.objects.filter(post__slug = post_slug)
        return queryset
    
    def post(self, request, *args, **kwargs):
        print('self.request.data: ', self.request.data)
        # user_pk = self.kwargs.get("user_pk")
        # tags = self.request.data.get('tags')
        # print('user_pk: ', user_pk, 'tags: ', tags)
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
        # if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        print('serializer.errors:', serializer.errors)

    def perform_create(self, serializer):
        print('perform create')
        post = self.request.data.get("post")
        post = get_object_or_404(Post, slug=post)
        # print('post got')
        serializer.save(post=post)


class ImagePostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=PostImageSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = "name"
    def get_queryset(self):
        post_slug = self.kwargs.get("slug")
        queryset = ImagePost.objects.filter(post__slug = post_slug)
        return queryset