from django.contrib import admin
from .models import GalleryImage
from django.utils.html import format_html

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'description')
    search_fields = ('description',)
    readonly_fields = ('preview',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" style="border-radius: 5px;" />', obj.image.url)
        return "-"
    thumbnail.short_description = 'Preview'

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 300px;" />', obj.image.url)
        return "No image uploaded."
    preview.short_description = 'Image Preview'
