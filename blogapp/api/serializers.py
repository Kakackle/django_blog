from rest_framework import serializers
from blogapp.models import Post, Tag, User, Comment
from datetime import datetime

class TagSerializer(serializers.ModelSerializer):

    # posts = serializers.HyperlinkedRelatedField(many=True,
    #                                             read_only=True,
    #                                             view_name="api_post_detail")
    
    # posts = PostSerializer(many=True, read_only=True)
    
    # posts = serializers.StringRelatedField(many=True,
    #                                         read_only=True,
    #                                         )
    
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
    # posts = serializers.HyperlinkedRelatedField(many=True,
    #                                             read_only=True,
    #                                             view_name="api_post_detail")
    
    # posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posts = serializers.SlugRelatedField(many=True, read_only=True, slug_field = 'slug')
    liked_posts = serializers.SlugRelatedField(many=True, read_only=True, slug_field = 'slug')
    
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = "__all__"

class UserSerializerSlug(serializers.ModelSerializer):
    # posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    posts = serializers.SlugRelatedField(many=True, read_only=True, slug_field = 'slug')
    liked_posts = serializers.SlugRelatedField(many=True, read_only=True, slug_field = 'slug')
    
    avatar = serializers.ImageField(required=False)
    class Meta:
        model = User
        fields = "__all__"
        lookup_field = 'slug'

# class subCommentSerializer(serializers.ModelSerializer):
#     author = serializers.PrimaryKeyRelatedField(read_only=True,
#                                                )
#     parent = serializers.PrimaryKeyRelatedField(read_only=True)
#     class Meta:
#         model = Comment
#         # fields = "__all__"
#         fields = ("id", "content", "date_posted", "parent", "author")

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    # children = subCommentSerializer()
    # children = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    post = serializers.SlugRelatedField(read_only=True, slug_field='slug')
    liked_by = serializers.SlugRelatedField(many=True, read_only=False,
                                            slug_field = 'slug',
                                            queryset=User.objects.all())
    class Meta:
        model = Comment
        fields = "__all__"

    def get_fields(self):
        fields = super(CommentSerializer, self).get_fields()
        fields['replies'] = CommentSerializer(many=True, required=False)
        return fields

class CommentSerializerSlug(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True,)
    parent = serializers.PrimaryKeyRelatedField(read_only=True)
    # children = subCommentSerializer(many=True)
    class Meta:
        model = Comment
        fields = "__all__"
        lookup_field = 'slug'

class PostSerializer(serializers.ModelSerializer):
    # tags = serializers.HyperlinkedRelatedField(many=True,
    #                                            read_only=True,
    #                                            view_name="api_tag_detail")
    # comments = serializers.HyperlinkedRelatedField(many=True,
    #                                            read_only=True,
    #                                            view_name="api_comment_detail")
    # author = serializers.HyperlinkedRelatedField(read_only=True,
    #                                            view_name="api_user_detail")
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                               read_only=True,
                                               )
    comments = serializers.PrimaryKeyRelatedField(many=True,
                                               read_only=True,
                                               )
    author = serializers.PrimaryKeyRelatedField(read_only=True,
                                               )
    # tags = TagSerializer(many=True, read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    # author = UserSerializer(read_only=True)

    img = serializers.ImageField(required=False)
    class Meta:
        model = Post
        fields = "__all__"
    
    # def validate(self, data):
    #     pass

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
                                            queryset=User.objects.all())
    img = serializers.ImageField(required=False)
    class Meta:
        model = Post
        fields = "__all__"
        lookup_field = 'slug'

    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('liked_by')
    #     instance = super(PostSerializerSlug, self).update(instance, validated_data)

    

class PostSerializerCreate(serializers.ModelSerializer):
    """Serializer for create / post operations"""
    img = serializers.ImageField(required=False)
    class Meta:
        model = Post
        fields = "__all__"


