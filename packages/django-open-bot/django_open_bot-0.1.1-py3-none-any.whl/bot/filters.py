class BaseFilter:
    def __init__(self):
        self.event_type = None
        self.event = None
        self.bot = None


class IsAdminFilter(BaseFilter):
    def __init__(self, admin):
        super().__init__()
        self.admin = admin
