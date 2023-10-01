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

class UserDetailSlugAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'

# all following relationships
class FollowingAPIView(generics.ListCreateAPIView):
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

@api_view(['GET'])
def followed_view(request, slug):
    followed = list(Following.objects.filter(following_user=slug).values_list('user', flat=True))
    return JsonResponse({'followed': followed})

@api_view(['GET'])
def followed_by_view(request, slug):
    followed_by = list(Following.objects.filter(user=slug).values_list('following_user', flat=True))
    return JsonResponse({'followed_by': followed_by})

@api_view(['POST'])
def add_to_follows(request, slug):
    # nowy uzytkownik ktory ma byc dodany - czyli ktorego strone widzimy
    new_follower = request.data.get('new_follower')
    new_follower_object = User.objects.get(slug=new_follower)
    # uzytkownik ktory ma zaczac sledzic - czyli zalogowany
    user_object = User.objects.get(slug=slug)
    user_followed_by = list(Following.objects.filter(user=slug).values_list('following_user', flat=True))
    # jesli uzytkownik chcialby sledzic siebie
    if new_follower == slug:
        return JsonResponse({'added_to_follows': False},status=400)
    # jesli jeszcze nie ma podanego uzytkownika w sledzonych przez aktualnego
    if new_follower not in user_followed_by:
        # uzytkownik wskazany otrzymuje nowego sledzacego
        new_follower_object.followed_by_count += 1
        new_follower_object.save()
        # uzytkownik zalogowany otrzymuje nowego ktorego sledzi
        user_object.followed_count += 1
        user_object.save()
        Following.objects.create(user=user_object, following_user=new_follower_object)
        return JsonResponse({'added_to_follows': True},status=200)
    else:
        return JsonResponse({'added_to_follows': False},status=400)

@api_view(['POST'])
def remove_from_follows(request, slug):
    follower = request.data.get('follower')
    follower_object = User.objects.get(slug=follower)
    user_object = User.objects.get(slug=slug)
    user_followed_by = list(Following.objects
                            .filter(user=slug).values_list('following_user', flat=True))
    if follower in user_followed_by:
        # uzytkownik wskazany otrzymuje nowego sledzacego
        follower_object.followed_by_count -= 1
        follower_object.save()
        # uzytkownik zalogowany otrzymuje nowego ktorego sledzi
        user_object.followed_count -= 1
        user_object.save()
        Following.objects.filter(user=user_object, following_user=follower_object).delete()
        return JsonResponse({'removed_from_follows': True},status=200)
    else:
        return JsonResponse({'removed_from_follows': False},status=400)

