from fastapi import APIRouter, HTTPException,Depends
from src.core.repository import gas_station_operator_repository
from src.core.models.models import GasStationOperator
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/gas-station-operator",
    tags=["Gas station operator CRUD"],
)


@router.get("/")
async def get_gas_station_operators(secure_data: dict = Depends(role_required(Role.USER))):
    page = gas_station_operator_repository.get_all_gas_station_operators()
    return page


@router.get("/{id}")
async def get_gas_station_operator_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    gas_station_operator = gas_station_operator_repository.get_gas_station_operator_by_id(id)
    
    if not gas_station_operator:
        raise HTTPException(status_code=404, detail=f"Gas station operator with id {id} not found")
    
    return gas_station_operator


@router.post("/")
async def create_gas_station_operator(
    gas_station_operator: GasStationOperator,
    secure_data: dict = Depends(role_required(Role.ADMIN)),
):
    create_gas_station_operator = gas_station_operator_repository.create_gas_station_operator(gas_station_operator)

    return {
        "message" : "Gas station operator create success",
        "data" : create_gas_station_operator
    }


@router.put("/{id}")
async def update_gas_station_operator(
    id: int,
    gas_station_operator: GasStationOperator, 
    secure_data: dict = Depends(role_required(Role.ADMIN)),              
):
    result = gas_station_operator_repository.update_gas_station_operator(id, gas_station_operator)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Gas station operator with id {id} not found")

    return  {
        "message" : f"Gas station operator with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_gas_station_operator(id: int, secure_data: dict = Depends(role_required(Role.ADMIN))):
    result = gas_station_operator_repository.delete_gas_station_operator_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Gas station operator with id {id} not found")

    return {"message" : "Gas station operator delete success"}