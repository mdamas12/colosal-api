

class UserRegisterUsecase(object):

    class Exception(Exception):
        pass

    def __init__(self, repository, username, email, password, is_superuser):
        self.repository = repository
        self.username = username
        self.email = email
        self.password = password
        self.is_superuser = is_superuser

    def execute(self):
        return self.repository.create_user(self.username, self.email, self.password, self.is_superuser)