from typing import Annotated

from fastapi import Depends

from madr_postgres.deps.service import (
    get_auth_service,
    get_author_service,
    get_book_service,
    get_user_service,
)
from madr_postgres.services import auth, users

from ..models import User
from ..services.authors import AuthorService
from ..services.books import BookService
from .users import get_current_user

UserServiceDep = Annotated[users.UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[auth.AuthService, Depends(get_auth_service)]
AuthorServiceDep = Annotated[AuthorService, Depends(get_author_service)]
BookServiceDep = Annotated[BookService, Depends(get_book_service)]

CurrentUser = Annotated[User, Depends(get_current_user)]
