from blogapp.models import User, Following, Post
from blogapp.api.serializers import UserSerializer, UserSerializerSlug, FollowingSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import generics
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404

class UserListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)

class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)

class UserDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'

# all following relationships
class FollowingAPIView(generics.ListCreateAPIView):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

@api_view(['GET', 'POST'])
def followed_view(request, slug):
    followed = list(Following.objects.filter(following_user=slug).values_list('user', flat=True))
    return JsonResponse({'followed': followed})

@api_view(['GET', 'POST'])
def followed_by_view(request, slug):
    followed_by = list(Following.objects.filter(user=slug).values_list('following_user', flat=True))
    return JsonResponse({'followed_by': followed_by})

# FIXME: eh... problemy bez serializatorow - brak wiedzy
@api_view(['GET', 'POST'])
def add_to_follows(request, slug):
    new_follower = request.data.get('new_follower')
    new_follower_object = User.objects.get(slug=new_follower)
    user_object = User.objects.get(slug=slug)
    user_followed_by = list(Following.objects.filter(user=slug).values_list('following_user', flat=True))
    if new_follower == slug:
        return JsonResponse({'added_to_follows': False},status=400)
    if new_follower not in user_followed_by:
        Following.objects.create(user=user_object, following_user=new_follower_object)
    # user_followed_by.append(new_follower)
        return JsonResponse({'added_to_follows': True},status=200)
    else:
        return JsonResponse({'added_to_follows': False},status=400)

@api_view(['GET', 'POST'])
def remove_from_follows(request, slug):
    follower = request.data.get('follower')
    follower_object = User.objects.get(slug=follower)
    user_object = User.objects.get(slug=slug)
    user_followed_by = list(Following.objects
                            .filter(user=slug).values_list('following_user', flat=True))
    if follower in user_followed_by:
        Following.objects.filter(user=user_object, following_user=follower_object).delete()
        return JsonResponse({'removed_from_follows': True},status=200)
    else:
        return JsonResponse({'removed_from_follows': False},status=400)
    # user_followed_by.append(new_follower)


# niewykorzystane - problem ponownie - zgodnosc querysetu i serializatora z tym
# co chce zaktualizowac, zrobic
# czyli tutaj chce na podstawie uzytkownika podanego w slug w endpoincie
# zmienic relacje w modelu Following
# i ostatecznie zrobilem to @api_view "recznie" poprzez tworzenie nowego rekordu
# following albo usuwania
class FollowAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = FollowingSerializer
    lookup_field = 'slug'

    def patch(self, request, *args, **kwargs):
        # print('update request data:', self.request.data)
        return self.partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        print('update request data:', self.request.data)
        new_follower = self.request.data.get('new_follower')
        user_slug = self.kwargs.get("slug")
        followed_by = list(Following.objects.filter(user=user_slug)
                           .values_list('following_user', flat=True))
        if new_follower not in followed_by:
            followed_by.append(new_follower)
        else:
            followed_by.remove(new_follower)
        serializer.save(followed_by=followed_by)
