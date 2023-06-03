from django.urls import path, include
from blogapp.api.views import PostListAPIView, PostDetailAPIView, TagListAPIView, TagDetailAPIView, \
UserListAPIView, UserDetailAPIView, CommentListAPIView, CommentDetailAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name="api_post_list"),
    path('posts/<int:pk>', PostDetailAPIView.as_view(), name="api_post_detail"),
    path('tags/', TagListAPIView.as_view(), name="api_tag_list"),
    path('tags/<int:pk>', TagDetailAPIView.as_view(), name="api_tag_detail"),
    path('users/', UserListAPIView.as_view(), name="api_user_list"),
    path('users/<int:pk>', UserDetailAPIView.as_view(), name="api_user_detail"),
    path('comments/', CommentListAPIView.as_view(), name="api_comment_list"),
    path('comments/<int:pk>', CommentDetailAPIView.as_view(), name="api_comment_detail"),
]

