from django.core.management.base import BaseCommand
from Modules.LotteryBot import Bot
from TeleShop.settings import TOKEN
from os import system


class Command(BaseCommand):
    help = 'Starting Telegram bot'

    def handle(self, *args, **options):
        system("./wait-for-postgres.sh")
        print('Bot starting... ', end='')
        bot = Bot(token=TOKEN)
        bot.run()
