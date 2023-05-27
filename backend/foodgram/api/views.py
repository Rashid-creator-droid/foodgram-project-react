from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from fpdf import FPDF
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from api.filters import RecipeFilter
from core.pagination import LargeResultsSetPagination
from recipe.models import (
    Tag,
    Recipe,
    Ingredient,
    Favorites,
    Basket,
    RecipeIngredients,
)
from users.serializers import SpecialRecipeSerializer
from .permissions import ReadOnly
from .serializers import (
    TagSerializer,
    RecipeSerializer,
    IngredientsSerializer,
    RecipeEditSerializer,
)


class IngredientFilter(filters.SearchFilter):
    search_param = 'name'


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [ReadOnly]


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = [ReadOnly]
    filter_backends = [IngredientFilter]
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = RecipeFilter
    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeEditSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def __added(self, model, user, pk, name):
        recipe = get_object_or_404(Recipe, id=pk)
        if model.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'errors': f'Вы уже добавили {recipe.name} в {name}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.create(user=user, recipe=recipe)
        serializer = SpecialRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def __deleted(self, model, user, pk, name):
        recipe = get_object_or_404(Recipe, id=pk)
        removable = model.objects.filter(user=user, recipe=recipe)
        if not removable.exists():
            return Response(
                {'errors': f'Вы не добавляли {recipe.name} в {name}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        removable.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def generated_pdf(self, user):
        ingredients = RecipeIngredients.objects.filter(
            recipe__basket__user=user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            ingredient_amount=Sum('amount')
        )
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font(
            'DejaVu',
            '',
            './core/fonts/timesnewromanpsmt.ttf',
            uni=True,
        )
        pdf.set_font('DejaVu', size=14)
        pdf.cell(
            w=0,
            txt=f'Список ингредиентов пользователя {user.username}',
            align='C',
        )
        pdf.ln(10)
        for index, ingredient in enumerate(ingredients):
            name = ingredient['ingredient__name']
            unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_amount']
            pdf.cell(50, 10, f'{index + 1}) {name} {amount} {unit}')
            pdf.ln()
        return pdf.output()

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='favorite',
        filterset_class=RecipeFilter,
    )
    def favorite(self, request, pk=None):
        name = 'избранное'
        user = request.user
        if request.method == 'POST':
            return self.__added(Favorites, user, pk, name)
        if request.method == 'DELETE':
            return self.__deleted(Favorites, user, pk, name)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='shopping_cart',
    )
    def shopping_cart(self, request, pk=None):
        name = 'список покупок'
        user = request.user
        if request.method == 'POST':
            return self.__added(Basket, user, pk, name)
        if request.method == 'DELETE':
            return self.__deleted(Basket, user, pk, name)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=['get'],
        url_path='download_shopping_cart',
    )
    def download_cart(self, request):
        response = HttpResponse(
            bytes(self.generated_pdf(request.user)),
            content_type='application/pdf',
            status=status.HTTP_200_OK,
        )
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.pdf"'
        )
        return response
