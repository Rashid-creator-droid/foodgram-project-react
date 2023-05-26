from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import DateTimeField

from foodgram.settings import MAX_AMOUNT, MIN_AMOUNT

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
        unique=True,
    )
    color = ColorField(default='#000000')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Ссылка',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='recipe',
        verbose_name='Автор',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='Картинка',
        upload_to='recipe/images',
    )
    text = models.TextField(verbose_name='Описание', max_length=1000)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredients',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MaxValueValidator(
                MAX_AMOUNT,
                message='Время приготовления не может быть таким большим'
            ),
            MinValueValidator(
                MIN_AMOUNT,
                message='Время приготовления не может быть меньше 1 минуты',
            )
        ],
    )
    pub_date = DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.SET_NULL,
        null=True,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MaxValueValidator(
                MAX_AMOUNT,
                message='Количество ингредиентов слишком большое'
            ),
            MinValueValidator(
                MIN_AMOUNT,
                message='Количество ингредиентов не может быть меньше 1',
            )
        ],
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        related_name='favorite',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorite',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='uniquefavorit'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('recipe')),
                name='author_user'
            )
        ]


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        related_name='basket',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='basket',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='uniquebasket'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('recipe')),
                name='author_user'
            )
        ]
