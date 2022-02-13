from django.contrib import admin
from MessageApp.models import TelegramMessagePattern


@admin.register(TelegramMessagePattern)
class TelegramMessagePatternAdmin(admin.ModelAdmin):
    list_display = ('role', 'text')
    list_filter = ('role',)
    search_fields = ('role', 'text')
    save_on_top = True
    ordering = ('role', 'text')
