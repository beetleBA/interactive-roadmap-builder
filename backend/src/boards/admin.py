from django.contrib import admin
from .models import Board, Access


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    pass


@admin.register(Access)
class AccessAdmin(admin.ModelAdmin):
    pass
