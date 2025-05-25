from enum import Enum
from pydantic import BaseModel, StrictStr

from src.secure.secure_entity import Role


class User(BaseModel):
    id: int = 0
    login: str | None
    password: str | None
    role: str = Role.USER
    avatar: str | None = None
    

class Auto(BaseModel):
    id: int
    brand: str
    model: str
    generation: str
    engine: str
    engine_capacity: float
    fuel_consumption: float
    fuel_type: str
    user_id: int


class Image(BaseModel):
    id: int
    type: str
    level: str
    position: int	
    object_id: int
    path: str


class Brand(BaseModel):
    id: int
    name: str


class Model(BaseModel):
    id: int
    name: str
    brand_id: int
    

class Generation(BaseModel):
    id: int
    name: str
    model_id: int
    

class Engine(BaseModel):
    id: int
    name: str
    engine_capacity: float
    fuel_consumption: float
    generation_id: int


class GasStationOperator(BaseModel):
    id: int
    name: str
    

class GasStation(BaseModel):
    id: int
    coords: str
    ai92: float | None = 0.0
    ai95: float | None = 0.0
    ai98: float | None = 0.0
    ai100: float | None = 0.0
    diesel: float | None = 0.0
    gas_propane: float | None = 0.0
    gas_methane: float | None = 0.0
    operator_gas_station_id: int
    

class FavoriteRoute(BaseModel):
    id: int
    point_departure: str
    point_arrival: str
    travel_time: str
    route_length: int
    fuel_type: str = "-" # fuel not set
    fuel_volume: float = 0.0
    fuel_cost: float = 0.0
    date: int
    user_id: int
    operator_gas_station_id: int = 6 # DEFAULT
