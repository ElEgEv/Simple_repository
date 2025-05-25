from fastapi import APIRouter, HTTPException,Depends
from src.core.repository import model_repository
from src.core.models.models import Model
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/model",
    tags=["Model CRUD"],
)


@router.get("/")
async def get_models(secure_data: dict = Depends(role_required(Role.USER))):
    page = model_repository.get_all_models()
    return page


@router.get("/brand/{brand_id}")
async def get_models_by_brand_id(brand_id: int, secure_data: dict = Depends(role_required(Role.USER))):
    page = model_repository.get_models_by_brand_id(brand_id)
    return page


@router.get("/{id}")
async def get_model_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    model = model_repository.get_model_by_id(id)
    
    if not model:
        raise HTTPException(status_code=404, detail=f"Model with id {id} not found")
    
    return model


@router.post("/")
async def create_model(
    model: Model,
    secure_data: dict = Depends(role_required(Role.ADMIN)),
):
    create_model = model_repository.create_model(model)
    
    if not create_model:
        raise HTTPException(status_code=404, detail=f"Brand with id {model.brand_id} not found")

    return {
        "message" : "Model create success",
        "data" : create_model
    }


@router.put("/{id}")
async def update_model(
    id: int,
    model: Model, 
    secure_data: dict = Depends(role_required(Role.ADMIN)),              
):
    result = model_repository.update_model(id, model)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Model with id {id} or brand with id {model.brand_id} not found")

    return  {
        "message" : f"Model with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_model(id: int, secure_data: dict = Depends(role_required(Role.ADMIN))):
    result = model_repository.delete_model_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Model with id {id} not found")

    return {"message" : "Model delete success"}