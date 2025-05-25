from fastapi import APIRouter, HTTPException,Depends
from src.core.repository import gas_station_repository
from src.core.models.models import GasStation
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/gas-station",
    tags=["Gas station CRUD"],
)


@router.get("/")
async def get_gas_stations(secure_data: dict = Depends(role_required(Role.USER))):
    page = gas_station_repository.get_all_gas_stations()
    return page


@router.get("/type-fuel")
async def gat_type_fuel(secure_data: dict = Depends(role_required(Role.USER))):
    data = {
        "ai92": "АИ92",
        "ai95": "АИ95",
        "ai98": "АИ98",
        "ai100": "АИ100",
        "diesel": "Дизель",
        "gas_propane": "Газ пропан",
        "gas_methane": "Газ метан"
    }
    
    return [data]


@router.get("/{id}")
async def get_gas_station_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    gas_station = gas_station_repository.get_gas_station_by_id(id)
    
    if not gas_station:
        raise HTTPException(status_code=404, detail=f"Gas station with id {id} not found")
    
    return gas_station


@router.get("/operator/{operator_gas_station_id}")
async def get_gas_station_by_operator_id(operator_gas_station_id: int, secure_data: dict = Depends(role_required(Role.USER))):
    gas_station = gas_station_repository.get_gas_station_by_operator_id(operator_gas_station_id)
    
    if not gas_station:
        raise HTTPException(status_code=404, detail=f"Gas station with operator id {id} not found")
    
    return gas_station


@router.post("/")
async def create_gas_station(
    gas_station: GasStation,
    secure_data: dict = Depends(role_required(Role.ADMIN)),
):
    create_gas_station = gas_station_repository.create_gas_station(gas_station)
    
    if not create_gas_station:
        raise HTTPException(status_code=404, detail=f"Operator gas station with id {gas_station.operator_gas_station_id} not found")

    return {
        "message" : "Gas station create success",
        "data" : create_gas_station
    }


@router.put("/{id}")
async def update_gas_station(
    id: int,
    gas_station: GasStation, 
    secure_data: dict = Depends(role_required(Role.ADMIN)),              
):
    result = gas_station_repository.update_gas_station(id, gas_station)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Gas station with id {id} not found")

    return  {
        "message" : f"Gas station with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_gas_station(id: int, secure_data: dict = Depends(role_required(Role.ADMIN))):
    result = gas_station_repository.delete_gas_station_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Gas station with id {id} not found")

    return {"message" : "Gas station delete success"}
