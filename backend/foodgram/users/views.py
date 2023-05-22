from django.shortcuts import get_object_or_404
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.pagination import LargeResultsSetPagination
from .serializers import MeSerializer, \
    SignUpSerializer, SubscribeSerializer
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
        url_path='me',
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer_class = MeSerializer
        if request.method == 'GET':
            serializer = serializer_class(request.user, many=False)
            return Response(serializer.data)

    @action(
        url_path='subscriptions',
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializer(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)


class SubscribeViewSet(CreateDestroyViewSet):
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        return self.request.user.follower.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['author_id'] = self.kwargs.get('user_id')
        return context

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            author=get_object_or_404(
                User,
                id=self.kwargs.get('user_id')
            )
        )

    @action(
        methods=['delete'],
        detail=True
    )
    def delete(self, request, user_id):
        get_object_or_404(User, id=user_id)
        author = get_object_or_404(
            User,
            id=self.kwargs.get('user_id')
        )
        if not Follow.objects.filter(
                user=request.user, author_id=user_id).exists():
            return Response(
                {'errors': f'Вы не были подписаны на {author.username}'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        get_object_or_404(
            Follow,
            user=request.user,
            author_id=user_id
        ).delete()
        return Response(
            {'errors': f'Вы отписались от пользователя {author.username}'},
            status=status.HTTP_204_NO_CONTENT,
        )
