class DatabaseError(Exception):
    pass


class UserExistsError(DatabaseError):
    pass


class UrlExistsError(DatabaseError):
    pass


class UserNotExistError(DatabaseError):
    pass



class UrlNotExistError(DatabaseError):
    pass