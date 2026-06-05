from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'price', 'stock', 'is_available', 'created', 'updated']
    list_filter = ['is_available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'is_available']
    prepopulated_fields = {'slug': ('title',)}