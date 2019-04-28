from django.contrib import admin

from .models import Ad


class AdAdmin(admin.ModelAdmin):
    fields = ['author', 'title', 'ad_text', 'deleted']
    list_display = ('title', 'short_text', 'created_at', 'deleted')
    list_filter = ['created_at']
    search_fields = ['title', 'ad_text']


admin.site.register(Ad, AdAdmin)
