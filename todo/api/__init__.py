from fastapi import APIRouter, Depends

from api.auth.auth import auth_router
from api.internal.dependencies import get_token_header
from api.todo.todo import todo_router
from api.user.user import user_router
from api.address.address import address_router
from api.internal.internal import internal_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(todo_router, prefix="/todo", tags=["Todo"])
router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(address_router, prefix="/address", tags=["Address"])
router.include_router(internal_router,
                      prefix="/internal",
                      tags=["Internal"],
                      responses={418: {
                          "description": "Internal User Only"
                      }},
                      dependencies=[Depends(get_token_header)])

__all__ = ["router"]
