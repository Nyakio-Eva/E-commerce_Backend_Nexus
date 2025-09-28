from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "is_active")
    search_fields = ("name", "description")
    list_filter = ("category", "is_active")
    ordering = ("id",)
