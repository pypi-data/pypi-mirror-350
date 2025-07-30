from .models import TelegramBot

from importlib import import_module
from django.conf import settings



def get_bot_model():
    if hasattr(settings, 'BOT_MODEL'):
        module_path, class_name = settings.BOT_MODEL.rsplit('.', 1)
        bot = getattr(import_module(module_path), class_name)
        if issubclass(bot, TelegramBot):
            return bot
        else:
            raise TypeError(f"{bot} is not a subclass of TelegramBot.")
    else:
        return TelegramBot