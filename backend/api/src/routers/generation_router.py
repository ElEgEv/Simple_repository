from fastapi import APIRouter, HTTPException,Depends
from src.core.repository import generation_repository
from src.core.models.models import Generation
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/generation",
    tags=["Generation CRUD"],
)


@router.get("/")
async def get_generations(secure_data: dict = Depends(role_required(Role.USER))):
    page = generation_repository.get_all_generations()
    return page


@router.get("/model/{model_id}")
async def get_generations_by_model_id(model_id: int, secure_data: dict = Depends(role_required(Role.USER))):
    page = generation_repository.get_generations_by_model_id(model_id)
    return page


@router.get("/{id}")
async def get_generation_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    generation = generation_repository.get_generation_by_id(id)
    
    if not generation:
        raise HTTPException(status_code=404, detail=f"Generation with id {id} not found")
    
    return generation


@router.post("/")
async def create_generation(
    generation: Generation,
    secure_data: dict = Depends(role_required(Role.ADMIN)),
):
    create_generation = generation_repository.create_generation(generation)
    
    if not create_generation:
        raise HTTPException(status_code=404, detail=f"Model with id {generation.model_id} not found")

    return {
        "message" : "Generation create success",
        "data" : create_generation
    }


@router.put("/{id}")
async def update_generation(
    id: int,
    generation: Generation, 
    secure_data: dict = Depends(role_required(Role.ADMIN)),              
):
    result = generation_repository.update_generation(id, generation)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Generation with id {id} or model with id {generation.model_id} not found")

    return  {
        "message" : f"Generation with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_generation(id: int, secure_data: dict = Depends(role_required(Role.ADMIN))):
    result = generation_repository.delete_generation_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Generation with id {id} not found")

    return {"message" : "Generation delete success"}