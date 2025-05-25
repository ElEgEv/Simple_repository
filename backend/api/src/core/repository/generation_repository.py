from src.core.database.database import db
from src.core.models.models import Generation
from src.core.repository import model_repository


def get_all_generations():
    query = "SELECT * FROM public.generation;"
    generations = db.fetch_all(query)

    return generations


def get_generations_by_model_id(model_id: int):
    query = "SELECT * FROM public.generation WHERE model_id=%s;"
    generations = db.fetch_all(query, (model_id,))

    return generations


def get_generation_by_id(generation_id: int):
    query = "SELECT * FROM public.generation WHERE id=%s;"
    generations = db.fetch_one(query, (generation_id,))

    return generations

def create_generation(generation: Generation):
    result_check = model_repository.get_model_by_id(generation.model_id)

    if not result_check:
        return False

    query = ("INSERT INTO public.generation (name, model_id) VALUES (%s, %s);")

    params = (generation.name, generation.model_id,)

    cursor = db.execute_query(query, params)
    
    all_generations = get_all_generations()

    return all_generations[-1]


def update_generation(id: int, generation: Generation):
    try:
        result_check = get_generation_by_id(id)

        if not result_check:
            return False
        
        result_check = model_repository.get_model_by_id(generation.model_id)

        if not result_check:
            return False

        query = "UPDATE public.generation SET name=%s, model_id=%s WHERE id=%s;"
        params = (generation.name, generation.model_id, id,)

        db.execute_query(query, params)

        return get_generation_by_id(id)
    except:
        return False


def delete_generation_by_id(id: int):
    check_generations_exist = get_generation_by_id(id)

    if not check_generations_exist:
        return False

    query = "DELETE FROM public.generation WHERE id=%s;"
    db.execute_query(query, (id,))

    return True
