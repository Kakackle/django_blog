from blogapp.api.pagination import CustomPagination
from blogapp.api.serializers import (PostSerializer, PostSerializerCreate,
                                     PostSerializerSlug)
from blogapp.models import Post, Tag, User
from django.template.defaultfilters import slugify
from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response


class PostListAPIView(generics.ListCreateAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostSerializerSlug
    pagination_class = CustomPagination
    parser_classes = (MultiPartParser, FormParser)
    # filter_backends = [SearchFilter]
    # search_fields = ["title"]
    def get_queryset(self):
        queryset = Post.objects.all().order_by("-id")

        
        # dodatkowe filtracje
        liked_by = self.request.query_params.get("liked_by", None)
        own = self.request.query_params.get("own", None)
        commented = self.request.query_params.get("commented", None)
        followed = self.request.query_params.get("followed", None)
        if liked_by:
            # wymaga przeslania slugu zalogowanego uzytkownika
            print('liked_by:', liked_by)
            user = User.objects.get(slug=liked_by)
            print('user:', user)
            print('liked_posts:', user.liked_posts.all())
            queryset = user.liked_posts.all()
            print('qs:', queryset)
        if own:
            print('own:', own)
            queryset = queryset.filter(author__username=own)
        if commented:
            #TODO: tak samo - przeslania zalogowanego ale i jak zrealizowac te funkcjonalnosc?
            pass
        if followed:
            #same
            pass


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
    # content = {'message': 'you just got all posts'}
    # return Response()

class PostListTrendingAPIView(generics.ListCreateAPIView):
    # queryset = Post.objects.all()
    def get_queryset(self):
        # return super().get_queryset()
        queryset = Post.objects.all().order_by("-trending_score")[:5]
        return queryset
        
    serializer_class = PostSerializerSlug
    parser_classes = (MultiPartParser, FormParser)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    def patch(self, request, *args, **kwargs):
        # print('update request data:', self.request.data)
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        # print('update request data:', self.request.data)
        title = self.request.data.get("title")
        slug = slugify(title)
        # serializer.save(slug=slug)
        serializer.save()

class PostDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerSlug
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        # print('update request data:', self.request.data)
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        print('update request data:', self.request.data)
        views = self.request.data.get('views')
        likes = self.request.data.get('likes')
        liked_by = self.request.data.getlist('liked_by[]')

        post_slug = Post.objects.get(slug=self.kwargs.get("slug")).slug
        # if title supplied in request - post edit request
        req_title = self.request.data.get("title")
        if req_title:
            slug = slugify(req_title)
            if(post_slug != slug):
                serializer.save(slug=slug)
        # if view request
        if views:
            serializer.save(views=views)
            return
        if liked_by:
            new_liked_by = []
            for user in liked_by:
                userN = get_object_or_404(User, slug=user)
                new_liked_by.append(userN)
                # FIXME: tutaj opisz w devnotes czemu tak
            serializer.save(liked_by=new_liked_by, likes=likes)
            return
        else:
            serializer.save(liked_by=[], likes=0)
            return

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