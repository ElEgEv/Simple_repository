import random

from src.core.database.database import db
from src.core.models.models import Auto
from src.core.repository import user_repository


def get_all_cars():
    query = "SELECT * FROM public.auto;"
    cars = db.fetch_all(query)

    return cars


def get_all_cars_by_user_id(user_id: int = None):
    query = "SELECT * FROM public.auto WHERE user_id=%s;"
    cars = db.fetch_all(query, (user_id,))

    return cars


def get_auto_by_id(auto_id: int):
    query = "SELECT * FROM public.auto WHERE id=%s;"
    auto = db.fetch_one(query, (auto_id,))

    return auto


def create_auto(auto: Auto):
    result_check = user_repository.get_simple_user_by_id(auto.user_id)

    if not result_check:
        return False

    query = ("INSERT INTO public.auto (brand, model, generation, engine, engine_capacity, fuel_consumption, fuel_type, fuel_tank_capacity, user_id)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);")

    params = (auto.brand, auto.model, auto.generation, auto.engine, auto.engine_capacity, auto.fuel_consumption, auto.fuel_type, random.randint(44, 70), auto.user_id)

    cursor = db.execute_query(query, params)
    
    all_cars = get_all_cars_by_user_id(auto.user_id)

    return all_cars[-1]


def update_auto(id: int, auto: Auto):
    try:
        check_auto_exist = get_auto_by_id(id)

        if not check_auto_exist:
            return False

        if auto.user_id:
            check_user_exists = user_repository.get_simple_user_by_id(auto.user_id)

            if not check_user_exists:
                return False

        query = "UPDATE public.auto SET brand=%s, model=%s, generation=%s, engine=%s, engine_capacity=%s, fuel_consumption=%s, fuel_type=%s, user_id=%s WHERE id=%s;"
        params = (auto.brand, auto.model, auto.generation, auto.engine, auto.engine_capacity, auto.fuel_consumption, auto.fuel_type, auto.user_id, id)

        db.execute_query(query, params)

        return get_auto_by_id(id)
    except:
        return False


def delete_auto_by_id(id: int):
    check_auto_exist = get_auto_by_id(id)

    if not check_auto_exist:
        return False

    query = "DELETE FROM public.auto WHERE id=%s;"
    db.execute_query(query, (id,))

    return True
