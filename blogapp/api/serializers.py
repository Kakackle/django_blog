from rest_framework import serializers
from blogapp.models import Post, Tag, User, Comment
from datetime import datetime

class TagSerializer(serializers.ModelSerializer):

    posts = serializers.HyperlinkedRelatedField(many=True,
                                                read_only=True,
                                                view_name="api_post_detail")
    # posts = PostSerializer(many=True, read_only=True)
    # posts = serializers.StringRelatedField(many=True,
    #                                         read_only=True,
    #                                         )
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Tag
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True,
                                                read_only=True,
                                                view_name="api_post_detail")
    
    class Meta:
        model = User
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = "__all__"

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

    class Meta:
        model = Post
        fields = "__all__"
    
    # def validate(self, data):
    #     pass

class PostSerializerCreate(serializers.ModelSerializer):
    """Serializer for create / post operations"""
    class Meta:
        model = Post
        fields = "__all__"


