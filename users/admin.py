from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username')
    list_filter = ('email', 'username')

    fieldsets = (
        (None, {
            'fields': ('email', 'username')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
    )

    search_fields = ('email', 'username')
    ordering = ('email', 'username')


admin.site.register(User, CustomUserAdmin)
