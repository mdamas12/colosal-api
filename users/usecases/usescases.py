

class UserFindList(object):

    class Exception(Exception):
        pass

    def __init__(self, repository, query):
        self.repository = repository
        self.query = query

    def execute(self):
        return self.repository.find_user(self.query)


class UserRegister(object):

    class Exception(Exception):
        pass

    def __init__(self, repository, data):
        self.repository = repository
        self.data = data

    def execute(self):
        return self.repository.create_user(self.data)


class UserRecoverPassword(object):

    class Exception(Exception):
        pass

    def __init__(self, repository, email):
        self.repository = repository
        self.email = email

    def execute(self):
        return self.repository.reset_password(self.email)