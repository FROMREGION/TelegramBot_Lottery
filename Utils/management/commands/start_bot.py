from django.core.management.base import BaseCommand
from Modules.LotteryBot import run
from TeleShop.settings import TOKEN
from os import system

from aiogram.utils import executor


class Command(BaseCommand):
    help = 'Starting Telegram bot'

    def handle(self, *args, **options):
        system("./wait-for-postgres.sh")
        print('Bot starting... ', end='')
        run()
