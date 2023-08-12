from blogapp.api.views import (CommentCreateAPIView, CommentDetailAPIView,
                               CommentLikeAPIView, CommentListAPIView,
                               FollowAPIView, FollowedAPIView,
                               FollowingAPIView, ImagePostDetailAPIView,
                               ImagePostListAPIView, PostCreateAPIView,
                               PostDetailSlugAPIView, PostLikeAPIView,
                               PostListAllAPIView, PostListAPIView,
                               PostListTrendingAPIView, PostViewAPIView,
                               TagDetailSlugAPIView, TagListAPIView,
                               UserDetailSlugAPIView, UserListAPIView,
                               add_to_follows, followed_by_view, followed_view,
                               post_image_view, remove_from_follows)
from django.urls import include, path

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name="api_post_list"),
    path('posts/all/', PostListAllAPIView.as_view(), name="api_posts_list_all"),
    path('posts/trending/', PostListTrendingAPIView.as_view(), name="api_posts_list_trending"),
    path('posts/<slug:slug>', PostDetailSlugAPIView.as_view(), name="api_post_detail_slug"),
    path('posts/followed/', FollowedAPIView.as_view(), name='api_followed_posts'),
    path('posts/<slug:slug>/view', PostViewAPIView.as_view(), name="api_post_viewed"),
    path('posts/<slug:slug>/like', PostLikeAPIView.as_view(), name="api_post_like"),

    path('tags/', TagListAPIView.as_view(), name="api_tag_list"),
    path('tags/<slug:slug>', TagDetailSlugAPIView.as_view(), name="api_tag_detail_slug"),
    
    path('users/', UserListAPIView.as_view(), name="api_user_list"),
    path('users/<slug:slug>', UserDetailSlugAPIView.as_view(), name="api_user_detail_slug"),
    path('users/<slug:slug>/post', PostCreateAPIView.as_view({'get': 'list'}), name="api_post_create"),
    path('users/<slug:slug>/followed/', followed_view, name='followed_view'),
    path('users/<slug:slug>/followed_by/', followed_by_view, name='followed_by_view'),

    # path('users/<slug:slug>/follow', FollowAPIView.as_view(), name='add_to_follows_view'),
    path('users/<slug:slug>/follow', add_to_follows, name='add_to_follows_view'),
    path('users/<slug:slug>/unfollow', remove_from_follows, name='remove_from_follows_view'),

    path('following/', FollowingAPIView.as_view(), name='api_following_list'),

    path('comments/', CommentListAPIView.as_view(), name="api_comment_list"),
    path('comments/<int:pk>', CommentDetailAPIView.as_view(), name="api_comment_detail"),
    path('create_comment', CommentCreateAPIView.as_view({'get': 'list'}),
          name="api_comment_create"),
    path('comments/<int:pk>/like', CommentLikeAPIView.as_view(), name="api_comment_like"),

    path('image/<slug:slug>', post_image_view, name='post_image_view'),
    path('posts/<slug:slug>/images', ImagePostListAPIView.as_view(), name="api_post_images"),
    path('posts/<slug:slug>/images/<str:name>', ImagePostDetailAPIView.as_view(), name="api_post_image_name"),
]

