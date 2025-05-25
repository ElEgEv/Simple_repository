from fastapi import APIRouter, HTTPException,Depends
from src.core.repository import engine_repository
from src.core.models.models import Engine
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/engine",
    tags=["Engine CRUD"],
)


@router.get("/")
async def get_engines(secure_data: dict = Depends(role_required(Role.USER))):
    page = engine_repository.get_all_engines()
    return page


@router.get("/generation/{generation_id}")
async def get_engines_by_generation_id(generation_id: int, secure_data: dict = Depends(role_required(Role.USER))):
    page = engine_repository.get_engines_by_generation_id(generation_id)
    return page


@router.get("/{id}")
async def get_engine_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    engine = engine_repository.get_engine_by_id(id)
    
    if not engine:
        raise HTTPException(status_code=404, detail=f"Engine with id {id} not found")
    
    return engine


@router.post("/")
async def create_engine(
    engine: Engine,
    secure_data: dict = Depends(role_required(Role.ADMIN)),
):
    create_engine = engine_repository.create_engine(engine)
    
    if not create_engine:
        raise HTTPException(status_code=404, detail=f"Generation with id {engine.generation_id} not found")

    return {
        "message" : "Engine create success",
        "data" : create_engine
    }


@router.put("/{id}")
async def update_engine(
    id: int,
    engine: Engine, 
    secure_data: dict = Depends(role_required(Role.ADMIN)),              
):
    result = engine_repository.update_engine(id, engine)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Engine with id {id} or generation with id {engine.generation_id} not found")

    return  {
        "message" : f"Engine with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_engine(id: int, secure_data: dict = Depends(role_required(Role.ADMIN))):
    result = engine_repository.delete_engine_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Engine with id {id} not found")

    return {"message" : "Engine delete success"}