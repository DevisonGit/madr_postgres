class MadrError(Exception): ...


class AlreadyExists(MadrError):
    pass


class NotFound(MadrError):
    pass
