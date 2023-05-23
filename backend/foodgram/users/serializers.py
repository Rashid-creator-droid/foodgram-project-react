from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from users.models import User, Follow
from recipe.models import Recipe


class MeSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        )
        required_fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )


class SignUpSerializer(UserSerializer):
    is_subscribed = SerializerMethodField('get_is_subscribed')

    class Meta:
        model = User
        fields = ['id', 'email', 'username', "first_name", 'is_subscribed', "last_name"]
        read_only_fields = ['id', 'is_subscribed']

    def get_is_subscribed(self, obj):
        """Статус подписки на автора."""
        user_id = self.context.get('request').user.id
        return Follow.objects.filter(
            author=obj.id, user=user_id).exists()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SpecialRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )

class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = [
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        ]

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return Follow.objects.filter(
            author=obj.author, user=user).exists()

    def get_recipes(self, obj):
        limit = self.context.get('request').GET.get('recipes_limit')
        recipe_obj = obj.author.recipe.all()
        if limit:
            recipe_obj = recipe_obj[:int(limit)]
        serializer = SpecialRecipeSerializer(recipe_obj, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return obj.author.recipe.count()