from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework import mixins
from rest_framework.filters import SearchFilter
from rest_framework import viewsets

from blogapp.models import Post, Tag, Comment, User
from blogapp.api.serializers import PostSerializer, PostSerializerCreate, TagSerializer, CommentSerializer, UserSerializer
from blogapp.api.serializers import TagSerializerSlug, UserSerializerSlug, PostSerializerSlug, CommentSerializerSlug
from blogapp.api.pagination import CustomPagination


# ---------------------------------------------------------------------------- #
#                                 generic views                                #
# ---------------------------------------------------------------------------- #

class PostListAPIView(generics.ListCreateAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination
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
            queryset = queryset.filter(author=author)
        if len(tags) is not 0:
            # queryset = queryset.filter(tags__name__in=tags)
            queryset = queryset.filter(tags__in=tags)
        if title is not None:
            queryset = queryset.filter(title__icontains=title)
        return queryset
        #FIXME: z jakiegos powodu niezrozumialego nie moge filtrowac tak przez tagi w slugach
        # nawet jesli jako serializator postow dam ten ze slugami
        # bo mowi ze "pole id musi byc numerem a dostalo tekst"
        # jakie kurwa id mnie tu nie obchodzi zadne id o chuj ci chodzi
        # ale ze takie uzycie query uzywamy tylko w wewnetrznych callach to poki co moze zostac
        # ale przydaloby sie to kiedys naprawic    

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializerSlug
    lookup_field = 'slug'

# generics.CreateAPIView
class PostCreateAPIView(viewsets.ModelViewSet):
    # queryset = Post.objects.all()
    serializer_classes = {
        'create': PostSerializerCreate,
    }
    default_serializer_class = PostSerializer

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def post(self, request, *args, **kwargs):
        # print('self.request.data: ', self.request.data.get('tags'))
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # print('self.request.data: ', self.request.data)
        user_pk = self.kwargs.get("user_pk")
        tags = self.request.data.get('tags')
        tagsList = []
        existingTags = Tag.objects.values_list('name', flat=True).distinct()
        print('existing:', existingTags)
        for tag in tags[0]:
            # TODO: przesylamy jednak tagi nazwami i po nazwach dodajemy i sprawdzamy
            if tag not in existingTags:
                tagL = Tag.objects.create(
                name = tag,
                description = tag
                )
                # print('created object:', tagL)
            else:
                tagL = get_object_or_404(Tag, name=tag)
            # tagL = get_object_or_404(Tag, pk=tag.get('id'))
            
            tagsList.append(tagL)
        author = get_object_or_404(User, pk=user_pk)
        serializer.save(author=author, tags=tagsList)
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

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'slug'

class CommentListAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class CommentDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'slug'