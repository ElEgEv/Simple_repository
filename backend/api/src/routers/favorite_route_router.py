from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Optional, Annotated
from src.core.repository import favorite_route_repository, common_tools
from src.core.models.models import FavoriteRoute
from src.secure.main_secure import role_required
from src.secure.secure_entity import Role


router = APIRouter(
    prefix="/api/favorite-route",
    tags=["Favorite route CRUD"],
)


@router.get("/")
async def get_favorite_routes(secure_data: dict = Depends(role_required(Role.USER))):
    page = favorite_route_repository.get_all_favorite_routes()
    return page


@router.get("/user/{user_id}")
async def get_favorite_routes_by_user_id(user_id: int, secure_data: dict = Depends(role_required(Role.USER))):
    page = favorite_route_repository.get_all_favorite_routes_by_user_id(user_id)
    
    if not page and page != []:
        raise HTTPException(status_code=404, detail=f"Favorite routes with user id {user_id} not found")
    
    return page


@router.get("/{id}")
async def get_favorite_route_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    gas_station = favorite_route_repository.get_favorite_route_by_id(id)
    
    if not gas_station:
        raise HTTPException(status_code=404, detail=f"Favorite route with id {id} not found")
    
    return gas_station


@router.get("/full-statisctics/{user_id}")
async def get_full_statisctic_by_user_id(
    user_id: int, 
    secure_data: dict = Depends(role_required(Role.USER))
):
    page = common_tools.get_full_statistic_for_user(user_id)

    if not page and page != []:
        raise HTTPException(status_code=404, detail=f"Can't creatre report for user with id {user_id}")
    
    return page


@router.post("/statistics-by-period/")
async def get_statistics_by_period(
    user_id: Annotated[int, Form()] = None,
    start: Annotated[int, Form()] = None, 
    end: Annotated[int, Form()] = None, 
    operator_gas_station_id: Annotated[int, Form()] = None,
    secure_data: dict = Depends(role_required(Role.USER))
):
    data = common_tools.get_statistic_for_user_by_period(start, end, user_id, operator_gas_station_id)
    
    if not data:
        raise HTTPException(status_code=404, detail=f"Can't creatre report for user with id {user_id}")

    return data


@router.post("/")
async def create_favorite_route(
    gas_station: FavoriteRoute,
    secure_data: dict = Depends(role_required(Role.USER)),
):
    create_favorite_route = favorite_route_repository.create_favorite_route(gas_station)
    
    if not create_favorite_route:
        raise HTTPException(status_code=404, detail=f"Operator gas station with id {gas_station.operator_gas_station_id} or user with id {gas_station.user_id} not found")

    return {
        "message" : "Favorite route create success",
        "data" : create_favorite_route
    }


@router.put("/{id}")
async def update_favorite_route(
    id: int,
    gas_station: FavoriteRoute, 
    secure_data: dict = Depends(role_required(Role.USER)),              
):
    result = favorite_route_repository.update_favorite_route(id, gas_station)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Favorite route with id {id} or operator gas station with id {gas_station.operator_gas_station_id} or user with id {gas_station.user_id} not found")

    return  {
        "message" : f"Favorite route with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_favorite_route(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    result = favorite_route_repository.delete_favorite_route_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"Favorite route with id {id} not found")

    return {"message" : "Favorite route delete success"}
