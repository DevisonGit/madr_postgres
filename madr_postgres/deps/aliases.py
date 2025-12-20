from typing import Annotated

from fastapi import Depends

from madr_postgres.deps.service import get_auth_service, get_user_service
from madr_postgres.services import auth, users

from ..models import User
from .users import get_current_user

UserServiceDep = Annotated[users.UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[auth.AuthService, Depends(get_auth_service)]

CurrentUser = Annotated[User, Depends(get_current_user)]
