from django.shortcuts import render
from .models import Post, Comment, Tag, User

# ---------------------------------------------------------------------------- #
#                              using generic views                             #
# ---------------------------------------------------------------------------- #

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

class PostDetailView(DetailView):
    model = Post
    template_name = "blogapp/post_detail.html"

class PostListView(ListView):
    model = Post
    template_name = "blogapp/post_list.html"


# ---------------------------------------------------------------------------- #
#                                 JSON response                                #
# ---------------------------------------------------------------------------- #

from django.http import JsonResponse

def post_list_response(request):
    posts = Post.objects.all()
    data = {"posts": list(posts.values())}
    response = JsonResponse(data)
    return response