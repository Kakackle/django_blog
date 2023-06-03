from django.urls import path
from .views import PostDetailView, PostListView, post_list_response

urlpatterns = [
    # --- using generic views
    path("posts/", PostListView.as_view(), name="post_list"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post_detail"),
    path("posts/response", post_list_response, name="post_list_response"),
]