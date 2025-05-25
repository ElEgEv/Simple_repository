from src.core.database.database import db
from src.core.models.models import Brand


def get_all_brands():
    query = "SELECT * FROM public.brand;"
    brands = db.fetch_all(query)

    return brands

def get_brand_by_id(brand_id: int):
    query = "SELECT * FROM public.brand WHERE id=%s;"
    brand = db.fetch_one(query, (brand_id,))

    return brand


def create_brand(brand: Brand):
    query = ("INSERT INTO public.brand (name) VALUES (%s);")

    params = (brand.name,)

    cursor = db.execute_query(query, params)
    
    all_brands = get_all_brands()

    return all_brands[-1]


def update_brand(id: int, brand: Brand):
    try:
        check_brand_exist = get_brand_by_id(id)

        if not check_brand_exist:
            return False

        query = "UPDATE public.brand SET name=%s WHERE id=%s;"
        params = (brand.name, id,)

        db.execute_query(query, params)

        return get_brand_by_id(id)
    except:
        return False


def delete_brand_by_id(id: int):
    check_brand_exist = get_brand_by_id(id)

    if not check_brand_exist:
        return False

    query = "DELETE FROM public.brand WHERE id=%s;"
    db.execute_query(query, (id,))

    return True
