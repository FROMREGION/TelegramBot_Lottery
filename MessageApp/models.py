from django.db import models
#
# class TelegramAdminUser(models.Model):
#     id = models.Cha


class TelegramMessagePattern(models.Model):
    role = models.CharField(verbose_name="Message role", max_length=64, unique=True)
    text = models.TextField(verbose_name="Message text")

    class Meta:
        verbose_name = "Message Pattern"
        verbose_name_plural = "Message Patterns"


class TelegramUser(models.Model):
    id = models.BigIntegerField(verbose_name="Telegram ID", unique=True, primary_key=True)
    username = models.CharField(verbose_name="Telegram username", max_length=32, default=None, blank=True)
    first_name = models.CharField(verbose_name="Telegram first_name", max_length=64, default=None, blank=True)
    is_subscribe = models.BooleanField(verbose_name="Is subscribe", blank=False, default=False)
    is_admin = models.BooleanField(verbose_name="Is admin", blank=False, default=False)

    class Meta:
        verbose_name = "Telegram User"
        verbose_name_plural = "Telegram Users"
