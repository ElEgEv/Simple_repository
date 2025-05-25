from src.core.database.database import db
from src.core.models.models import Engine
from src.core.repository import generation_repository


def get_all_engines():
    query = "SELECT * FROM public.engine;"
    engines = db.fetch_all(query)

    return engines


def get_engines_by_generation_id(generation_id: int):
    query = "SELECT * FROM public.engine WHERE generation_id=%s;"
    engines = db.fetch_all(query, (generation_id,))

    return engines


def get_engine_by_id(engine_id: int):
    query = "SELECT * FROM public.engine WHERE id=%s;"
    engines = db.fetch_one(query, (engine_id,))

    return engines

def create_engine(engine: Engine):
    result_check = generation_repository.get_generation_by_id(engine.generation_id)

    if not result_check:
        return False

    query = ("INSERT INTO public.engine (name, engine_capacity, fuel_consumption, generation_id) VALUES (%s, %s, %s, %s);")

    params = (engine.name, engine.engine_capacity, engine.fuel_consumption, engine.generation_id,)

    cursor = db.execute_query(query, params)
    
    all_engines = get_all_engines()

    return all_engines[-1]


def update_engine(id: int, engine: Engine):
    try:
        result_check = get_engine_by_id(id)

        if not result_check:
            return False
        
        result_check = generation_repository.get_generation_by_id(engine.generation_id)

        if not result_check:
            return False

        query = "UPDATE public.engine SET name=%s, engine_capacity=%s, fuel_consumption=%s, generation_id=%s WHERE id=%s;"
        params = (engine.name, engine.engine_capacity, engine.fuel_consumption, engine.generation_id, id,)

        db.execute_query(query, params)

        return get_engine_by_id(id)
    except:
        return False


def delete_engine_by_id(id: int):
    check_engines_exist = get_engine_by_id(id)

    if not check_engines_exist:
        return False

    query = "DELETE FROM public.engine WHERE id=%s;"
    db.execute_query(query, (id,))

    return True
