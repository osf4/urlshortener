class AuthError(Exception):
    pass


class WrongCredentialsError(AuthError):
    pass