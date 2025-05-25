from src.core.database.database import db
from src.core.models.models import GasStationOperator


def get_all_gas_station_operators():
    query = "SELECT * FROM public.operator_gas_station;"
    gas_station_operators = db.fetch_all(query)

    return gas_station_operators


def get_gas_station_operator_by_id(gas_station_operator_id: int):
    query = "SELECT * FROM public.operator_gas_station WHERE id=%s;"
    gas_station_operator = db.fetch_one(query, (gas_station_operator_id,))

    return gas_station_operator


def create_gas_station_operator(gas_station_operator: GasStationOperator):
    query = ("INSERT INTO public.operator_gas_station (name) VALUES (%s);")

    params = (gas_station_operator.name,)

    cursor = db.execute_query(query, params)
    
    all_gas_station_operators = get_all_gas_station_operators()

    return all_gas_station_operators[-1]


def update_gas_station_operator(id: int, gas_station_operator: GasStationOperator):
    try:
        check_gas_station_operator_exist = get_gas_station_operator_by_id(id)

        if not check_gas_station_operator_exist:
            return False

        query = "UPDATE public.operator_gas_station SET name=%s WHERE id=%s;"
        params = (gas_station_operator.name, id,)

        db.execute_query(query, params)

        return get_gas_station_operator_by_id(id)
    except:
        return False


def delete_gas_station_operator_by_id(id: int):
    check_gas_station_operator_exist = get_gas_station_operator_by_id(id)

    if not check_gas_station_operator_exist:
        return False

    query = "DELETE FROM public.operator_gas_station WHERE id=%s;"
    db.execute_query(query, (id,))

    return True
