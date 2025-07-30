import inspect

from .types import TelegramObject
from .states import StateManager


class Router:
    def __init__(self, bot):
        self.bot = bot
        self.handlers = {}
        self.error_handlers = {}
        self.state_handlers = {}

    def __call__(self, event_type, condition=None, state=None, exception=None):
        def decorator(handler):
            conditions = condition if isinstance(condition, list) else [condition]
            if event_type == 'error':
                name = exception.__name__
                self.error_handlers[name] = (exception, handler)
                return handler
            elif state:
                if event_type not in self.handlers:
                    self.handlers[event_type] = []
                self.handlers[event_type].append({"conditions": conditions, "handler": handler, "state": state})
            else:
                if event_type not in self.handlers:
                    self.handlers[event_type] = []
                self.handlers[event_type].append({"conditions": conditions, "handler": handler})
                return handler
        return decorator

    def updater(self, update):
        event_type, data = self.detect_event_type(update)
        data = TelegramObject(data)
        if event_type in self.handlers:
            state = StateManager(event_type, data)
            for handlers in self.handlers[event_type]:
                if handlers.get("state"):
                    conditions, handler, st = handlers.values()
                    if all(cond(data) for cond in conditions if cond) and st == state.current():
                        keys = inspect.signature(handler).parameters.keys()
                        if 'state' in keys:
                            handler(data, state)
                        else:
                            handler(data)
                        break
                else:
                    conditions, handler = handlers.values()
                    if all(cond(data) for cond in conditions if cond):
                        keys = inspect.signature(handler).parameters.keys()
                        if 'state' in keys:
                            handler(data, state)
                        else:
                            handler(data)
                        break


    @staticmethod
    def detect_event_type(update):
        if "message" in update:
            return "message", update["message"]
        elif "callback_query" in update:
            return "callback_query", update["callback_query"]
        elif "inline_query" in update:
            return "inline_query", update["inline_query"]
        return None, None

