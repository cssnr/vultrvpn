from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'is_staff', 'is_superuser',)
    list_filter = ('is_staff', 'is_superuser',)
    fieldsets = UserAdmin.fieldsets + (('OAuth', {'fields': ('avatar_hash',)}),)
    readonly_fields = ('username', 'avatar_hash',)
    search_fields = ('username', 'first_name', 'last_name',)
    ordering = ('username',)
