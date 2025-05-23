from django.contrib import admin
from .models import NewsUpdate


class NewsUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_created')
    ordering = ('-date_created',)

admin.site.register(NewsUpdate)