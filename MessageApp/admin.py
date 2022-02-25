from django.contrib import admin
from MessageApp.models import TelegramMessagePattern, TelegramUser


@admin.register(TelegramMessagePattern)
class TelegramMessagePatternAdmin(admin.ModelAdmin):
    list_display = ('role', 'text')
    list_filter = ('role',)
    search_fields = ('role', 'text')
    save_on_top = True
    ordering = ('role', 'text')

@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'is_subscribe', 'is_admin')
    list_filter = ('id', 'username', 'first_name', 'is_subscribe', 'is_admin')
    search_fields = ('id', 'username', 'first_name')
    save_on_top = True
    ordering = ('id', 'username')
