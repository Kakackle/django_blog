from blogapp.models import Comment, User, Post
from blogapp.api.serializers import CommentSerializer, CommentSerializerSlug
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from blogapp.api.pagination import CustomPagination

class CommentListAPIView(generics.ListCreateAPIView):
    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        queryset = Comment.objects.all().order_by("-date_posted")
        post = self.request.query_params.get("post", None)
        if post is not None:
            queryset = queryset.filter(post__slug=post)
        return queryset

# class CommentListByPostSlugAPIView(generics.ListCreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer

class CommentCreateAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        print('self.request.data: ', self.request.data)
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
        author = self.request.data.get("author")
        post = self.request.data.get("post")
        parent = self.request.data.get("parent")
        # print('author: ', author)
        author = get_object_or_404(User, slug=author)
        # print('author got')
        post = get_object_or_404(Post, slug=post)
        # print('post got')
        if parent != 'no_parent':
            parent = get_object_or_404(Comment, pk=parent)
            # print('parent got')
            serializer.save(author=author, post=post, parent=parent)
        else:
            serializer.save(author=author, post=post)

        
        # return super().perform_create(serializer)

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializerSlug
    lookup_field = 'slug'