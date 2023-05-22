from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

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
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user,
            author=obj,
        ).exists()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class SubscribeRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        source='author.email',
        read_only=True)
    id = serializers.IntegerField(
        source='author.id',
        read_only=True)
    username = serializers.CharField(
        source='author.username',
        read_only=True)
    first_name = serializers.CharField(
        source='author.first_name',
        read_only=True)
    last_name = serializers.CharField(
        source='author.last_name',
        read_only=True)
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField(
        source='author.recipe.count'
    )

    class Meta:
        model = Follow
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

    def validate(self, data):
        FIRST = 0
        user = self.context['request'].user
        author = User.objects.filter(id=self.context['author_id'])
        if user.id == author[FIRST].id:
            raise serializers.ValidationError('Подписка на себя не возможна.')
        if self.context['request'].method == 'POST':
            if Follow.objects.filter(
                    user=user,
                    author=author[FIRST].id,
            ).exists():
                raise serializers.ValidationError(
                    f'Вы уже подписаны на пользователя {author[FIRST].username}'
                )
        return data

    def get_recipes(self, obj):
        recipes = obj.author.recipe.all()
        return SubscribeRecipeSerializer(
            recipes,
            many=True,
        ).data

    def get_is_subscribed(self, obj):
        subscribe = Follow.objects.filter(
            user=self.context.get('request').user,
            author=obj.author,
        )
        if subscribe:
            return True
        return False