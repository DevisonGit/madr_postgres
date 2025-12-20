from madr_postgres.exceptions.base import MadrError


class UserNotFound(MadrError):
    pass


class UserAlreadyExists(MadrError):
    pass


class UserNotPermission(MadrError):
    pass
