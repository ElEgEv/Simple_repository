from fastapi import APIRouter, HTTPException, Depends
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role
from src.core.repository import map_repository


router = APIRouter(
    prefix="/api/map",
    tags=["Map CRUD"],
)


@router.get("/")
async def get_cities(secure_data: dict = Depends(role_required(Role.USER))):
    data = {
        "start": [
            'Москва',
            'Санкт-Петербург',
            'Новосибирск',
            'Екатеринбург',
            'Казань',
            'Нижний Новгород',
            'Челябинск',
            'Самара',
            'Уфа',
            'Ростов-на-Дону'
        ],
        "finish": [
            'Москва',
            'Санкт-Петербург',
            'Новосибирск',
            'Екатеринбург',
            'Казань',
            'Нижний Новгород',
            'Челябинск',
            'Самара',
            'Уфа',
            'Ростов-на-Дону'
        ]
    }
    
    return data

@router.get("/start-sity")
async def get_start_cities(secure_data: dict = Depends(role_required(Role.USER))):
    data = map_repository.get_all_cities()
    
    return data


@router.get("/finish-sity")
async def get_finish_cities(start_city_id: int, secure_data: dict = Depends(role_required(Role.USER))):
    data = map_repository.get_cities_by_start_sity_id(start_city_id)
    
    return data


@router.get("/map-route")
async def get_route_for_map(
    start_city_id: int, 
    finish_city_id: int, 
    start_fuel: float,
    gas_station_operator_id: int = 0, 
    fuel_type: str = None, 
    user_car_id: int = 0, 
    secure_data: dict = Depends(role_required(Role.USER))
):
    data = map_repository.get_route_by_start_and_finish_id(start_city_id, finish_city_id, gas_station_operator_id, fuel_type, start_fuel, user_car_id)
    
    return data
