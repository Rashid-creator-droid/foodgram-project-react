from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.pagination import LargeResultsSetPagination
from .serializers import MeSerializer, \
    SignUpSerializer, SubscriptionSerializer
from rest_framework import mixins, status, viewsets
from users.models import User, Follow


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass

class SignUp(UserViewSet):
    queryset = User.objects.all()
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'create':
            return MeSerializer
        return SignUpSerializer

    @action(
        detail=False,
        url_path='me',
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer_class = MeSerializer
        if request.method == 'GET':
            serializer = serializer_class(request.user, many=False)
            return Response(serializer.data)

    @action(
        detail=False,
        url_path='subscriptions',
        methods=['get'],
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        """Список авторов, на которых подписан пользователь."""
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_path='subscribe',
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response(
                {'errors': 'Попытка подписки/отписки на/от себя.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        subscription = Follow.objects.filter(
            author=author,
            user=user,
        )

        if request.method == 'POST':
            if subscription.exists():
                return Response(
                    {'errors': f'Вы уже подписаны на пользователя {author.username}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queryset = Follow.objects.create(
                author=author,
                user=user,
            )
            serializer = SubscriptionSerializer(
                queryset,
                context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not subscription.exists():
                return Response(
                    {'errors': f'Вы не были подписаны на пользователя {author.username}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            subscription.delete()
            return Response(
                {f'Вы отписаны от пользователя {author.username}'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
