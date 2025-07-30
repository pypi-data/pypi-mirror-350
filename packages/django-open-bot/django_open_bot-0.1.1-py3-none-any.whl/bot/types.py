from datetime import datetime, time, date
from collections.abc import Iterable

class TelegramObject:
    def __init__(self, data: dict):
        for key, value in data.items():
            if key == 'from':
                key = 'from_user'
            if isinstance(value, dict):
                value = TelegramObject(value)
            elif isinstance(value, list):
                value = [TelegramObject(item) if isinstance(item, dict) else item for item in value]
            value = self.convert_special_types(value)
            setattr(self, key, value)

    @staticmethod
    def convert_special_types(value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                pass
            try:
                return time.fromisoformat(value)
            except ValueError:
                pass
            try:
                return date.fromisoformat(value)
            except ValueError:
                pass
        if isinstance(value, tuple):
            return tuple(value)
        if isinstance(value, set):
            return set(value)
        if isinstance(value, Iterable) and not isinstance(value, str):
            return list(value)
        return value


class KeyboardBuilder:
    def __init__(self, resize_keyboard=False, one_time_keyboard=False):
        self.keyboards = []
        self.resize_keyboard = resize_keyboard
        self.one_time_keyboard = one_time_keyboard

    def add(self, **kwargs):
        self.keyboards.append([kwargs])

    def raws(self, x=2) -> None:
        raw_keyboard = []
        buttons_count = len(self.keyboards)
        for i in range(0, buttons_count, x):
            l = []
            for button in self.keyboards[i:i + x]:
                l.extend(button)
            raw_keyboard.append(l)
            print(l)
        self.keyboards = raw_keyboard

    def inline(self):
        return {'inline_keyboard': self.keyboards}

    def reply(self):
        return {"keyboard": self.keyboards, "resize_keyboard": self.resize_keyboard, "one_time_keyboard": self.one_time_keyboard}





