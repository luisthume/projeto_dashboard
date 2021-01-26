from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (User, XMLFile, NFe)

# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal_info'), {'fields': ('name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_superuser','groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'last_name', 'is_staff')
    search_fields = ('email', 'name', 'last_name')
    ordering = ('email',)