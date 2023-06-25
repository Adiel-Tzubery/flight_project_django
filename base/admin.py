from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from .models import *


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Permissions', {'fields': ('user_role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_filter = UserAdmin.list_filter + ('user_role',)
    ordering = ('email',)
    search_fields = ('email', 'username')


    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user_role')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data['password1'])
        super().save_model(request, obj, form, change)

    # Remove first_name, last_name, and date_joined from fieldsets
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ()}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )


admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register([Country, Flight, Ticket, UserRole, Administrator, Customer, AirlineCompany])
