from django.contrib import admin

from services.models import MainPage, Service


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ('header_1', 'header_2',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'category', 'price',)
#     list_filter = ('category',)
#     search_fields = ('name', 'description',)
