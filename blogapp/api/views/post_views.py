from blogapp.api.pagination import CustomPagination
from blogapp.api.serializers import (PostSerializer, PostSerializerCreate,
                                     PostSerializerSlug, UserSerializerSlug)
from blogapp.models import Post, Tag, User, Comment, Following
from django.template.defaultfilters import slugify
from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter

class PostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializerSlug
    pagination_class = CustomPagination
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = Post.objects.all().order_by("-id")
 
        # filtracje po specyficznych warunkach
        liked_by = self.request.query_params.get("liked_by", None)
        own = self.request.query_params.get("own", None)
        commented = self.request.query_params.get("commented", None)
        followed = self.request.query_params.get("followed", None)
        # posty polubione przez uzytkownika
        if liked_by:
            # wymaga przeslania slugu zalogowanego uzytkownika
            print('liked_by:', liked_by)
            user = User.objects.get(slug=liked_by)
            print('user:', user)
            print('liked_posts:', user.liked_posts.all())
            queryset = user.liked_posts.all()
            print('qs:', queryset)
        # tylko wlasne posty uzytkownika
        if own:
            print('own:', own)
            queryset = queryset.filter(author__username=own)
        # tylko posty na ktorych uzytkownik skomentowal
        if commented:
            queryset = queryset.filter(comments__author=commented).distinct()
            print('commented qs: ', queryset)
        # tylko posty od uzytkownikow ktorych sledzisz
        if followed:
            followed_users = Following.objects.filter(following_user=followed).values_list('user', flat=True)
            queryset = queryset.filter(author__slug__in=followed_users)
            print('followed qs:', queryset)

        author = self.request.query_params.get("author", None)
        tags = self.request.query_params.getlist("tag", None)
        title = self.request.query_params.get("title", None)
        days = self.request.query_params.get("days", None)

        if author is not None:
            queryset = queryset.filter(author__username=author)
        if len(tags) is not 0:
            queryset = queryset.filter(tags__in=tags).distinct()
            print('len: ', queryset.__len__())
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        if days is not None:
            date_limit = datetime.today() - timedelta(days=int(days))
            queryset = queryset.filter(date_posted__gte=date_limit)

        # Ordering
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
    
    @extend_schema(description="get posts with filtering",
                   parameters=[
                       OpenApiParameter(name='author', description='author slug', type=str),
                       OpenApiParameter(name='tags', description='tags array', type=list),
                       OpenApiParameter(name='title', description='by post title includes', type=str),
                       OpenApiParameter(name='days', description='how many days ago posted', type=int),
                       ])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class PostListAllAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerSlug
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(description="get all posts without filtering and pagination")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class PostListTrendingAPIView(generics.ListAPIView):
    def get_queryset(self):
        queryset = Post.objects.all().order_by("-trending_score")[:5]
        return queryset
        
    serializer_class = PostSerializerSlug
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(description="get all 'trending' posts only")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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

        # aktualizacja zliczen na tagach - moga sie zmienic w update
        post_object = Post.objects.get(slug=self.kwargs.get("slug"))
        tags = list(post_object.tags.all())
        for tag in tags:
            print('tag:', tag)
            tag.post_count +=1
            tag.save()

        post_slug = post_object.slug
        # if title supplied in request - post edit request
        req_title = self.request.data.get("title")
        if req_title:
            slug = slugify(req_title)
            if(post_slug != slug):
                serializer.save(slug=slug)
    
    # aktualizacja zliczania postow
    def delete(self, request, *args, **kwargs):
        post_object = Post.objects.get(slug=self.kwargs.get("slug"))
        # aktualizacja ilosci postow utworzonych przez uzytkownika
        author = post_object.author.slug
        author_object = User.objects.get(slug=author)
        author_object.post_count -= 1
        author_object.save()
        # aktualizacja ilosci postow z tagami
        tags = list(post_object.tags.all())
        for tag in tags:
            tag.post_count -=1
            tag.save()
        return self.destroy(request, *args, **kwargs)

class PostLikeAPIView(generics.UpdateAPIView):
    queryset=Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        # print('update request data:', self.request.data)
        return self.partial_update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        # print('update request data:', self.request.data)
        # post wybrany przez endpoint
        post = Post.objects.get(slug=self.kwargs.get('slug'))
        post_pk = post.pk
        # uzytkownicy, ktorzy w polubionych postach posiadaja post_pk
        liked_by = list(User.objects.filter(liked_posts=post_pk).values_list(
            'id', flat=True))
        
        new_user = int(self.request.data.get('user'))
        if new_user not in liked_by:
            liked_by.append(new_user)
            likes = len(liked_by)
            serializer.save(liked_by=liked_by, likes=likes)

            author_object = User.objects.get(slug=post.author.slug)
            author_object.post_likes_received += 1
            author_object.save()

            print('new liked_by: ', liked_by)
            return JsonResponse({'liked_by': liked_by, 'message': 'added'},status=200)
        else:
            liked_by.remove(new_user)
            likes = len(liked_by)
            serializer.save(liked_by=liked_by, likes=likes)

            author_object = User.objects.get(slug=post.author.slug)
            author_object.post_likes_received -= 1
            author_object.save()

            print('old liked_by: ', liked_by)
            return JsonResponse({'liked_by': liked_by, 'message': 'removed'},status=200)

# proby rozbijania views na wiecej mniejszych single-purpose endpointow
# dodawanie wyswietlen do postow prostym endpointem
class PostViewAPIView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerSlug
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        # print('update request data:', self.request.data)
        return self.partial_update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        print('update request data:', self.request.data)
        views = Post.objects.get(slug=self.kwargs.get("slug")).views
        views += 1
        serializer.save(views=views)

class PostCreateAPIView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_classes = {
        'create': PostSerializerCreate,
    }
    default_serializer_class = PostSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
    
    @extend_schema(tags=["posts",],
                   description="create post authored by specified user")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
        # if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            print('serializer.errors:', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        user_slug = self.kwargs.get("slug")

        #aktualizacja zliczania stworzonych przez uzytkownika postow
        user_object = User.objects.get(slug=user_slug)
        user_object.post_count +=1
        user_object.save()
        
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
        # aktualizacja zliczen ilosci postow z tagami
        for tag in tagsList:
            tag.post_count +=1
            tag.save()
        author = get_object_or_404(User, slug=user_slug)
        date_posted = self.request.data.get('date_posted')
        serializer.save(author=author, tags=tagsList, date_posted=date_posted, img=img)
        # return super().perform_create(serializer)
        return Response(data={"message": "post created"},
                        status=status.HTTP_201_CREATED)
    