from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Favorite

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "created_at")
    search_fields = ("user__email", "product__name")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
