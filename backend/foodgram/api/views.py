from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated, IsAuthenticatedOrReadOnly

from core.filters import RecipeFilter
from core.pagination import LargeResultsSetPagination
from users.serializers import SpecialRecipeSerializer
from .permissions import ReadOnly
from .serializers import TagSerializer, RecipeSerializer, IngredientsSerializer, RecipeEditSerializer, \
    FavoriteSerializer, ShoppingCartSerializer
from rest_framework import filters, viewsets, status
from recipe.models import Tag, Recipe, Ingredients, Favorites, Basket


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (ReadOnly,)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (ReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name']



class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filterset_class = RecipeFilter
    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeEditSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorites = Favorites.objects.filter(
            recipe=recipe,
            user=user,
        )
        if request.method == 'POST':
            if favorites.exists():
                return Response(
                    {'errors': f'Вы уже добавили {recipe.name} в список избранного'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Favorites.objects.create(
                recipe=recipe,
                user=user,
            )
            serializer = SpecialRecipeSerializer(
                recipe,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not favorites.exists():
                return Response(
                    {'errors': f'Вы не добавляли {recipe.name} в список избранного'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            favorites.delete()
            return Response(
                {f'Вы удалили {recipe.name} из списка избранного'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='shopping_cart',
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        basket = Basket.objects.filter(
            recipe=recipe,
            user=user,
        )
        if request.method == 'POST':
            if basket.exists():
                return Response(
                    {'errors': f'Вы уже добавили {recipe.name} в корзину'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Basket.objects.create(
                recipe=recipe,
                user=user,
            )
            serializer = SpecialRecipeSerializer(
                recipe,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not basket.exists():
                return Response(
                    {'errors': f'Вы не добавляли {recipe.name} в корзину'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            basket.delete()
            return Response(
                {f'Вы удалили {recipe.name} из корзины'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)