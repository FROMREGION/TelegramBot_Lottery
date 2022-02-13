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
