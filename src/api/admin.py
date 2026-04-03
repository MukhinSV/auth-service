from fastapi import APIRouter, Depends

from src.dependencies import DBDep, check_admin
from src.services.admin import AdminService

router = APIRouter(prefix="/admin", tags=["Администрирование"], dependencies=[Depends(check_admin)])

@router.get("/users", summary="Получить пользователей")
async def get_users(db: DBDep):
    return {"status": "WWW"}
    # return await AdminService(db).get_users()
