from django.contrib import admin

from services.models import MainPage, Service, Doctor


@admin.register(MainPage)
class MainPageAdmin(admin.ModelAdmin):
    list_display = ('header_1', 'header_2',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price',)
    search_fields = ('title',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization',)
    list_filter = ('specialization',)
    search_fields = ('name', 'specialization',)

