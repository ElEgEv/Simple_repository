from src.core.database.database import db
from src.core.models.models import GasStation
from src.core.repository import gas_station_operator_repository


def get_all_gas_stations():
    query = "SELECT * FROM public.gas_station;"
    gas_stations = db.fetch_all(query)

    return gas_stations


def get_gas_station_by_id(gas_station_id: int):
    query = "SELECT * FROM public.gas_station WHERE id=%s;"
    gas_station = db.fetch_one(query, (gas_station_id,))

    return gas_station


def get_gas_station_by_operator_id(operator_gas_station_id: int):
    query = "SELECT * FROM public.gas_station WHERE operator_gas_station_id=%s LIMIT 1;"
    gas_station = db.fetch_all(query, (operator_gas_station_id,))

    return gas_station


def get_cost_fuel_gas_station_by_id_and_fuel_type(gas_station_id: int, fuel_type: str):
    query = "SELECT " + fuel_type + " AS fuel_cost FROM public.gas_station WHERE id=%s;"
    gas_station = db.fetch_one(query, (gas_station_id,))

    return gas_station


def create_gas_station(gas_station: GasStation):
    check_gas_station_operator_exist = gas_station_operator_repository.get_gas_station_operator_by_id(gas_station.operator_gas_station_id)

    if not check_gas_station_operator_exist:
        return False
        
    query = ("INSERT INTO public.gas_station (coords, ai92, ai95, ai98, ai100, diesel, gas_propane, gas_methane, operator_gas_station_id)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")

    params = (gas_station.coords, gas_station.ai92, gas_station.ai95, gas_station.ai98, 
              gas_station.ai100, gas_station.diesel, gas_station.gas_propane, 
              gas_station.gas_methane, gas_station.operator_gas_station_id,)

    cursor = db.execute_query(query, params)
    
    all_gas_stations = get_all_gas_stations()

    return all_gas_stations[-1]


def update_gas_station(id: int, gas_station: GasStation):
    try:
        check_gas_station_exist = get_gas_station_by_id(id)

        if not check_gas_station_exist:
            return False
        
        check_gas_station_operator_exist = gas_station_operator_repository.get_gas_station_operator_by_id(gas_station.operator_gas_station_id)

        if not check_gas_station_operator_exist:
            return False

        query = ("UPDATE public.gas_station SET coords=%s, ai92=%s, ai95=%s, ai98=%s, ai100=%s,"
                 " diesel=%s, gas_propane=%s, gas_methane=%s, operator_gas_station_id=%s WHERE id=%s;")
        
        params = (gas_station.coords, gas_station.ai92, gas_station.ai95, gas_station.ai98, 
              gas_station.ai100, gas_station.diesel, gas_station.gas_propane, 
              gas_station.gas_methane, gas_station.operator_gas_station_id, id,)

        db.execute_query(query, params)

        return get_gas_station_by_id(id)
    except:
        return False


def delete_gas_station_by_id(id: int):
    check_gas_station_exist = get_gas_station_by_id(id)

    if not check_gas_station_exist:
        return False

    query = "DELETE FROM public.gas_station WHERE id=%s;"
    db.execute_query(query, (id,))

    return True
