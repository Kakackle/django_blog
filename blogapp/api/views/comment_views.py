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
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    @extend_schema(
            parameters=[
                OpenApiParameter(name='post', description='filter by post',
                                required=False, type=str)
            ],
            description='custom get_queryset?'
    )

    def get_queryset(self):
        queryset = Comment.objects.all().order_by("-date_posted")
        post = self.request.query_params.get("post", None)
        if post is not None:
            queryset = queryset.filter(post__slug=post)
        return queryset

class CommentCreateAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @extend_schema(
        request=CommentSerializer
    )
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
        author = get_object_or_404(User, slug=author)
        post = get_object_or_404(Post, slug=post)

        #aktualizacja zliczen
        author_object = User.objects.get(slug=self.request.data.get('author'))
        author_object.comment_count +=1
        author_object.save()

        post_object = Post.objects.get(slug=self.request.data.get('post'))
        post_object.comment_count +=1
        post_object.save()

        if parent != 'no_parent':
            parent = get_object_or_404(Comment, pk=parent)
            serializer.save(author=author, post=post, parent=parent)
        else:
            serializer.save(author=author, post=post)

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
        
class CommentLikeAPIView(generics.UpdateAPIView):
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