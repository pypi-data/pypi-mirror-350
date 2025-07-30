from django.apps import apps


class StateManager:

    def __init__(self, event_type, data):
        if event_type == 'message':
            self.chat_id = str(data.chat.id)
            self.user_id = data.from_user.id
        elif event_type == 'callback_query':
            self.chat_id = str(data.message.chat.id)
            self.user_id = data.message.from_user.id
        State = apps.get_model('bot', 'State')
        self.state_record, created = State.objects.get_or_create(chat_id=self.chat_id)

    def set(self, state_name):
        self.state_record.state = state_name
        self.state_record.save()

    def update(self, data: dict):
        self.state_record.data.update(data)
        self.state_record.save()

    def get(self):
        return self.state_record.data or {}

    def clear(self):
        self.state_record.delete()

    def current(self):
        return self.state_record.state
