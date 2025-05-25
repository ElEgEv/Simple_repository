from fastapi import APIRouter, HTTPException,Depends
from src.core.repository import user_auto_repository
from src.core.models.models import Auto
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/user/auto",
    tags=["Auto CRUD"],
)


@router.get("/")
async def get_cars(secure_data: dict = Depends(role_required(Role.ADMIN))):
    page = user_auto_repository.get_all_cars()
    return page


@router.get("/{id}")
async def get_auto_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    auto = user_auto_repository.get_auto_by_id(id)
    
    if not auto:
        raise HTTPException(status_code=404, detail=f"Auto with id {id} not found")
    
    return auto


@router.get("/user/{user_id}")
async def get_all_cars_by_user_id(user_id: int, secure_data: dict = Depends(role_required(Role.USER))):
    auto = user_auto_repository.get_all_cars_by_user_id(user_id)
    
    if not auto:
        raise HTTPException(status_code=404, detail=f"Auto with user id {user_id} not found")
    
    return auto


@router.post("/")
async def create_auto(
    auto: Auto,
    secure_data: dict = Depends(role_required(Role.USER)),
):
    create_auto = user_auto_repository.create_auto(auto)

    if not create_auto:
        raise HTTPException(status_code=500, detail=f"User with this user id {auto.user_id} not exists")

    return {
        "message" : "Auto create success",
        "data" : create_auto
    }


@router.put("/{id}")
async def update_auto(
    id: int,
    auto: Auto, 
    secure_data: dict = Depends(role_required(Role.USER)),              
):
    result = user_auto_repository.update_auto(id, auto)

    if not result:
        raise HTTPException(status_code=404, detail=f"Auto with id {id} or user with id {auto.user_id} not found")

    return  {
        "message" : f"Auto with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_auto(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    result = user_auto_repository.delete_auto_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Auto with id {id} not found")

    return {"message" : "Auto delete success"}