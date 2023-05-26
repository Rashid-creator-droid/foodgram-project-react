from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from users.models import Follow

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = UserCreationForm.Meta.model
        fields = '__all__'
        field_classes = UserCreationForm.Meta.field_classes


class UserAdminChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    form = UserAdminChangeForm
    model = User
    search_fields = (
        'username',
        'email',
    )
    list_filter = (
        'username',
        'email',
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )
    search_fields = (
        'user__username',
        'author__username',
    )