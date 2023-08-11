from blogapp.api.pagination import CustomPagination
from blogapp.api.serializers import CommentSerializer, CommentSerializerSlug
from blogapp.models import Comment, Post, User
from rest_framework import generics, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

class CommentListAPIView(generics.ListCreateAPIView):
    """
    Returns a list of all posts on a particular post supplied in request

    Post chosen by post_slug
    """
    # queryset = Comment.objects.all()
    
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    # @extend_schema(
    #     request=CommentSerializer,
    #     responses={200: CommentSerializer},
    #     methods=['GET']
    # )


    # @extend_schema(
    # # extra parameters added to the schema
    # parameters=[
    #     OpenApiParameter(name='artist', description='Filter by artist', required=False, type=str),
    #     OpenApiParameter(
    #         name='release',
    #         type=OpenApiTypes.DATE,
    #         location=OpenApiParameter.QUERY,
    #         description='Filter by release date',
    #         examples=[
    #             OpenApiExample(
    #                 'Example 1',
    #                 summary='short optional summary',
    #                 description='longer description',
    #                 value='1993-08-23'
    #             ),
    #             ...
    #         ],
    #     ),
    # ],
    # # override default docstring extraction
    # description='More descriptive text',
    # # provide Authentication class that deviates from the views default
    # auth=None,
    # # change the auto-generated operation name
    # operation_id=None,
    # # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
    # operation=None,
    # # attach request/response examples to the operation.
    # examples=[
    #     OpenApiExample(
    #         'Example 1',
    #         description='longer description',
    #         value=...
    #     ),
    #     ...
    # ],
    # )
    def get_queryset(self):
        queryset = Comment.objects.all().order_by("-date_posted")
        post = self.request.query_params.get("post", None)
        if post is not None:
            queryset = queryset.filter(post__slug=post)
        return queryset
    
    # @extend_schema(description='Override a specific method', methods=["GET"])
    # #@action(detail=True, methods=['post', 'get'])
    # def test_method(self, request, pk=None):
    #     # your action behaviour
    #     pass
    
    

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

        #aktualizacja zliczen
        author_object = User.objects.get(slug=self.request.data.get('author'))
        author_object.comment_count +=1
        author_object.save()

        post_object = Post.objects.get(slug=self.request.data.get('post'))
        post_object.comment_count +=1
        post_object.save()


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

    def delete(self, request, *args, **kwargs):
        #aktualizacja zliczen
        comment_object = Comment.objects.get(pk=self.kwargs.get('pk'))
        author_object = User.objects.get(slug=comment_object.author.slug)
        author_object.comment_count -=1
        author_object.save()

        post_object = Post.objects.get(slug=comment_object.post.slug)
        post_object.comment_count -=1
        post_object.save()
        return self.destroy(request, *args, **kwargs)

# wgl tu mamy napisane to wszystko a nigdy w to nie wchodzimy
# bo endpoint wchodzi w endpoint po ID
# czyli ten wyzej
# a jednak zmiana ustawiajaca na 0 i [] miala efekt mi sie wydawalo...
# wtf...

class CommentDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializerSlug
    lookup_field = 'slug'

    # def patch(self, request, *args, **kwargs):
    #     # print('update request data:', self.request.data)
    #     return self.partial_update(request, *args, **kwargs)
    
    # def perform_update(self, serializer):
    #     print('update request data:', self.request.data)
    #     # views = self.request.data.get('views')
    #     likes = self.request.data.get('likes')
    #     liked_by = self.request.data.getlist('liked_by[]')

    #     if liked_by:
    #         new_liked_by = []
    #         for user in liked_by:
    #             userN = get_object_or_404(User, slug=user)
    #             new_liked_by.append(userN)
    #             # generalnie: odbiera z frontu tablice slugow czyli str
    #             # a nastepnie na podstawie str tworzy pelne obiekty
    #             # ktore nastepnie zapisuje w modelu/obiekcie
    #             # o relacji to many przyjmujacej taka tablice obiektow
    #         serializer.save(liked_by=new_liked_by, likes=likes)
    #         return
    #     else:
    #         serializer.save(liked_by=[], likes=0)
    #         return
        
class CommentLikeAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class = CommentSerializer

    def patch(self, request, *args, **kwargs):
        # print('update request data:', self.request.data)
        return self.partial_update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        # print('update request data:', self.request.data)
        comment = Comment.objects.get(pk=self.kwargs.get('pk'))
        comment_pk = comment.pk
        # uzytkownicy, ktorzy w polubionych komentach maja comment_pk
        liked_by = list(User.objects.filter(liked_comments=comment_pk).values_list(
            'id', flat=True))
        
        new_user = int(self.request.data.get('user'))
        if new_user not in liked_by:
            liked_by.append(new_user)
            likes = len(liked_by)
            serializer.save(liked_by=liked_by, likes=likes)

            #aktualizacja zliczen ile uzytkownik ma polubien na komentarzach
            author_object = User.objects.get(slug=comment.author.slug)
            author_object.comment_likes_received += 1
            author_object.save()

            print('new liked_by: ', liked_by)
            return JsonResponse({'liked_by': liked_by, 'message': 'added'},status=200)
        else:
            liked_by.remove(new_user)
            likes = len(liked_by)
            serializer.save(liked_by=liked_by, likes=likes)
            
            author_object = User.objects.get(slug=comment.author.slug)
            author_object.comment_likes_received -= 1
            author_object.save()

            print('old liked_by: ', liked_by)
            return JsonResponse({'liked_by': liked_by, 'message': 'removed'},status=200)
        # liked_by = comment.slug
        print('users', liked_by)
        pass