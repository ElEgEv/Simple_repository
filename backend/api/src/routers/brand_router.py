from fastapi import APIRouter, HTTPException,Depends
from src.core.repository import brand_repository
from src.core.models.models import Brand
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/brand",
    tags=["Brand CRUD"],
)


@router.get("/")
async def get_brands(secure_data: dict = Depends(role_required(Role.USER))):
    page = brand_repository.get_all_brands()
    return page


@router.get("/{id}")
async def get_brand_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    brand = brand_repository.get_brand_by_id(id)
    
    if not brand:
        raise HTTPException(status_code=404, detail=f"Brand with id {id} not found")
    
    return brand


@router.post("/")
async def create_brand(
    brand: Brand,
    secure_data: dict = Depends(role_required(Role.ADMIN)),
):
    create_brand = brand_repository.create_brand(brand)

    return {
        "message" : "Brand create success",
        "data" : create_brand
    }


@router.put("/{id}")
async def update_brand(
    id: int,
    brand: Brand, 
    secure_data: dict = Depends(role_required(Role.ADMIN)),              
):
    result = brand_repository.update_brand(id, brand)

    return  {
        "message" : f"Brand with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_brand(id: int, secure_data: dict = Depends(role_required(Role.ADMIN))):
    result = brand_repository.delete_brand_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Brand with id {id} not found")

    return {"message" : "Brand delete success"}