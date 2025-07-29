
class AuthBase:

    def __init__(self, instance, user_id):
        super().__init__()
        self.application_instance = instance
        self.user_id = user_id

    def is_verified(self): ...


