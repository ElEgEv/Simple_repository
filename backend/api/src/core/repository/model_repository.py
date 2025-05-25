from src.core.database.database import db
from src.core.models.models import Model
from src.core.repository import brand_repository


def get_all_models():
    query = "SELECT * FROM model;"
    models = db.fetch_all(query)
    return models


def get_models_by_brand_id(brand_id: int):
    query = "SELECT * FROM model WHERE brand_id = ?;"
    models = db.fetch_all(query, (brand_id,))
    return models


def get_model_by_id(model_id: int):
    query = "SELECT * FROM model WHERE id = ?;"
    model = db.fetch_one(query, (model_id,))
    return model


def create_model(model: Model):
    result_check = brand_repository.get_brand_by_id(model.brand_id)
    if not result_check:
        return False

    query = "INSERT INTO model (name, brand_id) VALUES (?, ?);"
    params = (model.name, model.brand_id)
    db.execute_query(query, params)

    all_models = get_all_models()
    return all_models[-1] if all_models else None


def update_model(id: int, model: Model):
    try:
        check_model_exist = get_model_by_id(id)
        if not check_model_exist:
            return False

        result_check = brand_repository.get_brand_by_id(model.brand_id)
        if not result_check:
            return False

        query = "UPDATE model SET name = ?, brand_id = ? WHERE id = ?;"
        params = (model.name, model.brand_id, id)
        db.execute_query(query, params)

        return get_model_by_id(id)
    except Exception as e:
        # В реальной разработке логируй ошибку
        return False


def delete_model_by_id(id: int):
    check_model_exist = get_model_by_id(id)
    if not check_model_exist:
        return False

    query = "DELETE FROM model WHERE id = ?;"
    db.execute_query(query, (id,))
    return True
