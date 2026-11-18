from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Stack, UserStack

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Stack)
class StackAdmin(admin.ModelAdmin):
    pass


@admin.register(UserStack)
class UserStackAdmin(admin.ModelAdmin):
    pass
