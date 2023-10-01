niewykorzystane - problem ponownie - zgodnosc querysetu i serializatora z tym
co chce zaktualizowac, zrobic
czyli tutaj chce na podstawie uzytkownika podanego w slug w endpoincie
zmienic relacje w modelu Following
i ostatecznie zrobilem to @api_view "recznie" poprzez tworzenie nowego rekordu
following albo usuwania

```
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
```