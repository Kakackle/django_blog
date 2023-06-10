from django.urls import path, include
from blogapp.api.views import PostListAPIView, PostDetailAPIView, TagListAPIView, TagDetailAPIView, \
UserListAPIView, UserDetailAPIView, CommentListAPIView, CommentDetailAPIView, PostCreateAPIView, \
TagDetailSlugAPIView

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name="api_post_list"),
    path('posts/<int:pk>', PostDetailAPIView.as_view(), name="api_post_detail"),
    path('tags/', TagListAPIView.as_view(), name="api_tag_list"),
    path('tags/<int:pk>', TagDetailAPIView.as_view(), name="api_tag_detail"),
    path('tags/<slug:slug>', TagDetailSlugAPIView.as_view(), name="api_tag_detail_slug"),
    path('users/', UserListAPIView.as_view(), name="api_user_list"),
    path('users/<int:pk>', UserDetailAPIView.as_view(), name="api_user_detail"),
    path('users/<int:user_pk>/post', PostCreateAPIView.as_view({'get': 'list'}), name="api_post_create"),
    path('comments/', CommentListAPIView.as_view(), name="api_comment_list"),
    path('comments/<int:pk>', CommentDetailAPIView.as_view(), name="api_comment_detail"),
]

