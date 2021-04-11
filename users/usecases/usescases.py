

class UserFindList(object):

    class Exception(Exception):
        pass

    def __init__(self, repository, query):
        self.repository = repository
        self.query = query

    def execute(self):
        return self.repository.find_user(self.query)