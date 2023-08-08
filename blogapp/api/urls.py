from blogapp.api.views import (CommentCreateAPIView, CommentDetailAPIView,
                               CommentDetailSlugAPIView, CommentListAPIView,
                               ImagePostDetailAPIView, ImagePostListAPIView,
                               PostCreateAPIView, PostDetailAPIView,
                               PostDetailSlugAPIView, PostListAllAPIView,
                               PostListAPIView, PostListTrendingAPIView,
                               TagDetailAPIView,
                               TagDetailSlugAPIView, TagListAPIView,
                               UserDetailAPIView, UserDetailSlugAPIView,
                               UserListAPIView, post_image_view)
from django.urls import include, path

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name="api_post_list"),
    path('posts/all/', PostListAllAPIView.as_view(), name="api_posts_list_all"),
    path('posts/trending/', PostListTrendingAPIView.as_view(), name="api_posts_list_trending"),
    # path('posts/<int:pk>', PostDetailAPIView.as_view(), name="api_post_detail"),
    path('posts/<slug:slug>', PostDetailSlugAPIView.as_view(), name="api_post_detail_slug"),
    # path('posts/<slug:slug>', PostDetailSlugAPIView.as_view(), name="api_post_detail_slug"),


    path('tags/', TagListAPIView.as_view(), name="api_tag_list"),
    path('tags/<int:pk>', TagDetailAPIView.as_view(), name="api_tag_detail"),
    path('tags/<slug:slug>', TagDetailSlugAPIView.as_view(), name="api_tag_detail_slug"),
    
    path('users/', UserListAPIView.as_view(), name="api_user_list"),
    path('users/<int:pk>', UserDetailAPIView.as_view(), name="api_user_detail"),
    path('users/<slug:slug>', UserDetailSlugAPIView.as_view(), name="api_user_detail_slug"),
    path('users/<int:user_pk>/post', PostCreateAPIView.as_view({'get': 'list'}), name="api_post_create"),
    
    path('comments/', CommentListAPIView.as_view(), name="api_comment_list"),
    path('comments/<int:pk>', CommentDetailAPIView.as_view(), name="api_comment_detail"),
    path('comments/<slug:slug>', CommentDetailSlugAPIView.as_view(), name="api_comment_detail_slug"),
    path('create_comment', CommentCreateAPIView.as_view({'get': 'list'}),
          name="api_comment_create"),

    path('image/<slug:slug>', post_image_view, name='post_image_view'),
    path('posts/<slug:slug>/images', ImagePostListAPIView.as_view(), name="api_post_images"),
    path('posts/<slug:slug>/images/<str:name>', ImagePostDetailAPIView.as_view(), name="api_post_image_name"),
]

