from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import DateTimeField

User = get_user_model()


class Ingredients(models.Model):
    name = models.CharField('Название', max_length=150)
    measurement_unit = models.CharField(
        verbose_name="Единица измерения", max_length=200
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Название', max_length=100, unique=True)
    color = models.TextField(unique=True) # тута
    slug = models.SlugField(max_length=150, unique=True, verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт"""
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='recipe',
        verbose_name='Автор',
    )
    name = models.CharField('Название', max_length=150)
    image = models.ImageField(
        'Картинка',
        upload_to='recipe/images',
        blank=True,
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredients,
        through="RecipeIngredients",
        verbose_name='Ингредиенты',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.PositiveIntegerField()
    pub_date = DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['id']

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        null=True,
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.SET_NULL,
        null=True,
    )
    amount = models.PositiveIntegerField('Количество')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorites(models.Model):
    user = models.ForeignKey(
        User,
        related_name='elect',
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
            )
        ]


class Basket(models.Model):
    user = models.ForeignKey(
        User,
        related_name='buyer',
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
            )
        ]