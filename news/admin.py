from django.contrib import admin
from .models import NewsUpdate

@admin.register(NewsUpdate)
class NewsUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created')
    list_filter = ('status', 'date_created')
    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = "Mark selected news as published"