class User:

    def __init__(self, _id, username, password, name, **kwargs):
        self._id = _id
        self.username = username
        self.password = password
        self.name = name

    def __repr__(self):
        template = 'User id={s._id}: <{s.email}> , <{s.password}> .'
        return template.format(s=self)

    def __str__(self):
        return self.__repr__()

    def match_password(self, password):
        if password != self.password:
            raise User.PasswordDoesNotMatch

    class DoesNotExist(BaseException):
        pass

    class PasswordDoesNotMatch(BaseException):
        pass

    class objects:
        _storage = []
        _max_id = 0

        @classmethod
        def create(cls, email, password, is_admin=False):
            cls._max_id += 1
            cls._storage.append(User(cls._max_id, email, password, is_admin))

        @classmethod
        def all(cls):
            return cls._storage

        @classmethod
        def filter(cls, **kwargs):
            users = cls._storage
            for k, v in kwargs.items():
                if v:
                    users = [u for u in users if getattr(u, k, None) == v]
            return users

        @classmethod
        def get(cls, id=None, email=None):
            users = cls.filter(id=id, email=email)
            if len(users) > 1:
                raise User.TooManyObjects
            if len(users) == 0:
                raise User.DoesNotExist
            return users[0]
