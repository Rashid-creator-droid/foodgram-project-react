from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import SignUp, SubscribeViewSet
from .views import TagViewSet, RecipeViewSet, IngredientsViewSet

app_name = 'api'
router = DefaultRouter()


router.register('users', SignUp, basename='users'),
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register(
    r'users/(?P<user_id>\d+)/subscribe', SubscribeViewSet,
    basename='subscribe')
router.register('download_shopping_cart', TagViewSet, basename='basket')
router.register('subscriptions', TagViewSet, basename='subscriptions')
router.register('ingredients', IngredientsViewSet, basename='ingredients')




urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]