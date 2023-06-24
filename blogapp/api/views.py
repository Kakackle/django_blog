from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework.decorators import api_view
from django.http import HttpResponse

from django.template.defaultfilters import slugify

from blogapp.models import Post, Tag, Comment, User
from blogapp.api.serializers import PostSerializer, PostSerializerCreate, TagSerializer, CommentSerializer, UserSerializer
from blogapp.api.serializers import TagSerializerSlug, UserSerializerSlug, PostSerializerSlug, CommentSerializerSlug
from blogapp.api.pagination import CustomPagination


# ---------------------------------------------------------------------------- #
#                                 generic views                                #
# ---------------------------------------------------------------------------- #

class PostListAPIView(generics.ListCreateAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostSerializerSlug
    pagination_class = CustomPagination
    parser_classes = (MultiPartParser, FormParser)
    # filter_backends = [SearchFilter]
    # search_fields = ["title"]
    def get_queryset(self):
        queryset = Post.objects.all().order_by("-id")
        author = self.request.query_params.get("author", None)
        # tag = self.request.query_params.get("tag", None)
        tags = self.request.query_params.getlist("tag", None)
        # print("tags:",tags)
        title = self.request.query_params.get("title", None)
        if author is not None:
            # queryset = queryset.filter(author__name__icontains=author)
            queryset = queryset.filter(author__username=author)
        if len(tags) is not 0:
            # queryset = queryset.filter(tags__name__in=tags)
            queryset = queryset.filter(tags__in=tags).distinct()
            print('len: ', queryset.__len__())
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        # Ordering?
        ordering = self.request.query_params.get("ordering", None)
        if ordering:
            if ordering == "title":
                queryset = queryset.order_by("title")
            if ordering == "date":
                queryset = queryset.order_by("-date_posted")
            if ordering == "views":
                queryset = queryset.order_by("-views")
            if ordering == "likes":
                queryset = queryset.order_by("-likes")    
        return queryset
        # TODO: sprobuj tak jak autora zobaczy te tagi po slugach?
        # moze powinno dzialac, bo to __name, __in itd to jakies sprytne jest, nie wiem


class PostListAllAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerSlug
    parser_classes = (MultiPartParser, FormParser)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_update(self, serializer):
        title = self.request.data.get("title")
        slug = slugify(title)
        serializer.save(slug=slug)

class PostDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerSlug
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'

# generics.CreateAPIView
class PostCreateAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_classes = {
        'create': PostSerializerCreate,
    }
    default_serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

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
        # print('self.request.data: ', self.request.data)
        # WAZNE: tutaj kwargs jest to czesc argumentow wbudowanych w path
        # prawdziwe dane z requestu sa oczywiscie w requescie
        user_pk = self.kwargs.get("user_pk")
        tags = self.request.data.getlist('tags[]')
        img = self.request.data.get('img')
        print('img: ', img)
        # print('tags: ', tags)
        tagsList = []
        existingTags = Tag.objects.values_list('name', flat=True).distinct()
        # print('existingTags: ', existingTags)
        for tag in tags:
            # print('tag: ', tag)
            if tag not in existingTags:
                # print('not in')
                tagL = Tag.objects.create(
                name = tag,
                description = tag
                )
            else:
                tagL = get_object_or_404(Tag, name=tag)
            tagsList.append(tagL)
        author = get_object_or_404(User, pk=user_pk)
        date_posted = self.request.data.get('date_posted')
        serializer.save(author=author, tags=tagsList, date_posted=date_posted, img=img)
        # return super().perform_create(serializer)

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
        # if serializer.is_valid():
        if serializer.is_valid(raise_exception=True):
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

@api_view(['GET', 'POST'])
def post_image_view(request, slug):
    image = Post.objects.get(slug=slug).img
    return HttpResponse(image, content_type="image/jpg")