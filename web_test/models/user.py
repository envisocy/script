from models import Model

class User(Model):
    def __init__(self, form):
        self.id = None
        self.username = form.get("username", "")
        self.password = form.get("password", "")

    def validate_login(self):
        # user_all = User.all()
        # for u in user_all:
        #     if u.username == self.username and u.password == self.password:
        #         return True
        #     return False
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2
