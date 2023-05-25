from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from core.pagination import LargeResultsSetPagination
from users.models import User, Follow
from .serializers import MeSerializer, \
    SignUpSerializer, FollowSerializer


class SignUp(UserViewSet):
    queryset = User.objects.all()
    pagination_class = LargeResultsSetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'set_password':
            return SetPasswordSerializer
        if self.action == 'create':
            return MeSerializer
        return SignUpSerializer

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer_class = MeSerializer
        if request.method == 'GET':
            serializer = serializer_class(request.user, many=False)
            return Response(serializer.data)

    @action(
        detail=False,
        methods=['get'],
        url_path='subscriptions',
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request},
        )
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
        follow = Follow.objects.filter(
            author=author,
            user=user,
        )

        if request.method == 'POST':
            if follow.exists():
                return Response(
                    {'errors': f'Вы уже подписаны на {author.username}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            queryset = Follow.objects.create(
                author=author,
                user=user,
            )
            serializer = FollowSerializer(
                queryset,
                context={'request': request},
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            if not follow.exists():
                return Response(
                    {'errors': f'Нет подписки на {author.username}'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            follow.delete()
            return Response(
                {f'Вы отписаны от пользователя {author.username}'},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
