from fastapi import APIRouter

from api.auth.auth import auth_router
from api.todo.todo import todo_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(todo_router, prefix="/todo", tags=["Todo"])

__all__ = ["router"]
