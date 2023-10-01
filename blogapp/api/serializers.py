from rest_framework import serializers
from blogapp.models import Post, Tag, User, Comment, ImagePost, Following
from datetime import datetime

class TagSerializer(serializers.ModelSerializer): 
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Tag
        fields = "__all__"

class TagSerializerSlug(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')
    class Meta:
        model = Tag
        fields = "__all__"
        lookup_field = 'slug'


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(many=True, read_only=True, slug_field = 'slug')
    liked_posts = serializers.SlugRelatedField(many=True, read_only=True, slug_field = 'slug')
    
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = "__all__"
        lookup_field = 'slug'

class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Following
        fields = "__all__"

class UserSerializerSlug(serializers.ModelSerializer):
    posts = serializers.SlugRelatedField(many=True, read_only=True, slug_field = 'slug')
    liked_posts = serializers.SlugRelatedField(many=True, read_only=True, slug_field = 'slug')
    followed = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')
    followed_by = serializers.SlugRelatedField(many=True, read_only=True,
                                                slug_field='slug')
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = "__all__"
        lookup_field = 'slug'

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    post = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    liked_by = serializers.SlugRelatedField(many=True, read_only=False,
                                            slug_field = 'slug',
                                            queryset=User.objects.all(),
                                            required=False)
    class Meta:
        model = Comment
        fields = "__all__"
        lookup_field = 'slug'

    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        fields['replies'] = CommentSerializer(many=True, required=False)
        return fields

class CommentSerializerSlug(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = "__all__"
        lookup_field = 'slug'

class PostSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                               read_only=True,
                                               )
    comments = serializers.PrimaryKeyRelatedField(many=True,
                                               read_only=True,
                                               )
    author = serializers.PrimaryKeyRelatedField(read_only=True,
                                               )
    post_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')

    img = serializers.ImageField(required=False)
    class Meta:
        model = Post
        fields = "__all__"

class PostSerializerSlug(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True,
                                        read_only=True,
                                        slug_field = 'slug'
                                        )
    comments = serializers.SlugRelatedField(many=True,
                                            read_only=True,
                                            slug_field = 'slug'
                                            )
    author = serializers.SlugRelatedField(read_only=True,
                                          slug_field = 'slug'
                                            )
    liked_by = serializers.SlugRelatedField(many=True, read_only=False,
                                            slug_field = 'slug',
                                            queryset=User.objects.all(),
                                            required=False)
    img = serializers.ImageField(required=False)
    post_images = serializers.SlugRelatedField(many=True, read_only=True, slug_field='slug')

    class Meta:
        model = Post
        fields = "__all__"
        lookup_field = 'slug'

class PostSerializerCreate(serializers.ModelSerializer):
    """Serializer for create / post operations"""
    img = serializers.ImageField(required=False)
    class Meta:
        model = Post
        fields = ['title', 'tags', 'content', 'img', 'date_posted']

# ---------------------------------------------------------------------------- #
#                                    IMAGES                                    #
# ---------------------------------------------------------------------------- #
class PostImageSerializer(serializers.ModelSerializer):

    post = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    class Meta:
        model = ImagePost
        fields = "__all__"
        lookup_field = 'name'