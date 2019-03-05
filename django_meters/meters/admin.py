from django.contrib import admin
from .models import ResourceType, Meters, Records


class RecordsInline(admin.TabularInline):
    model = Records
    extra = 0
    ordering = ["-date"]


@admin.register(ResourceType)
class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ResourceType._meta.fields]
    list_display_links = ['id', 'name']

    class Meta:
        model = ResourceType


@admin.register(Meters)
class MetersAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Meters._meta.fields]
    list_display_links = ['id', 'name']
    inlines = [RecordsInline]

    class Meta:
        model = Meters