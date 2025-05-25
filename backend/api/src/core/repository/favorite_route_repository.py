from src.core.database.database import db
from src.core.models.models import FavoriteRoute
from src.core.repository import user_repository, gas_station_operator_repository


def get_all_favorite_routes():
    query = "SELECT * FROM public.favorite_route;"
    favorite_routes = db.fetch_all(query)
    
    for route in favorite_routes:
        operator_gas_station = gas_station_operator_repository.get_gas_station_operator_by_id(route['operator_gas_station_id'])
        
        if operator_gas_station:
            route['operator_gas_station'] = operator_gas_station['name']

    return favorite_routes


def get_all_favorite_routes_by_user_id(user_id: int):
    check_user = user_repository.get_user_by_id(user_id)

    if not check_user:
        return False
    
    query = "SELECT * FROM public.favorite_route WHERE user_id=%s;"
    favorite_routes = db.fetch_all(query, (user_id,))
    
    for route in favorite_routes:
        operator_gas_station = gas_station_operator_repository.get_gas_station_operator_by_id(route['operator_gas_station_id'])
        
        if operator_gas_station:
            route['operator_gas_station'] = operator_gas_station['name']
    
    return favorite_routes


def get_all_favorite_routes_by_period(start: int, end: int, user_id: int, operator_gas_station_id: int):
    check_user = user_repository.get_user_by_id(user_id)

    if not check_user:
        return False
    
    query = "SELECT * FROM public.favorite_route WHERE user_id=%s AND date >= %s AND date <= %s"
    
    params = (user_id, start, end, )
    
    if operator_gas_station_id:
        query += " AND operator_gas_station_id=%s"
        
        params = (user_id, start, end, operator_gas_station_id, )
        
    query += ';'
    
    favorite_routes = db.fetch_all(query, params)
    
    for route in favorite_routes:
        operator_gas_station = gas_station_operator_repository.get_gas_station_operator_by_id(route['operator_gas_station_id'])
        
        if operator_gas_station:
            route['operator_gas_station'] = operator_gas_station['name']

    return favorite_routes


def get_favorite_route_by_id(favorite_route_id: int):
    query = "SELECT * FROM public.favorite_route WHERE id=%s;"
    favorite_route = db.fetch_one(query, (favorite_route_id,))

    operator_gas_station = gas_station_operator_repository.get_gas_station_operator_by_id(favorite_route['operator_gas_station_id'])
    
    if operator_gas_station:
        favorite_route['operator_gas_station'] = operator_gas_station['name']

    return favorite_route


def create_favorite_route(favorite_route: FavoriteRoute):
    check_exists = user_repository.get_user_by_id(favorite_route.user_id)
    
    if not check_exists:
        return False
    
    check_exists = gas_station_operator_repository.get_gas_station_operator_by_id(favorite_route.operator_gas_station_id)

    if not check_exists:
        return False
        
    query = ("INSERT INTO public.favorite_route (point_departure, point_arrival, travel_time, route_length, fuel_type, fuel_volume, fuel_cost, date, user_id, operator_gas_station_id)"
             " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")

    params = (favorite_route.point_departure, favorite_route.point_arrival, favorite_route.travel_time, favorite_route.route_length, 
              favorite_route.fuel_type, favorite_route.fuel_volume, favorite_route.fuel_cost, favorite_route.date, 
              favorite_route.user_id, favorite_route.operator_gas_station_id,)

    cursor = db.execute_query(query, params)
    
    all_favorite_routes = get_all_favorite_routes()

    return all_favorite_routes[-1]


def update_favorite_route(id: int, favorite_route: FavoriteRoute):
    try:
        check_favorite_route_exist = get_favorite_route_by_id(id)

        if not check_favorite_route_exist:
            return False
        
        check_exists = user_repository.get_user_by_id(favorite_route.user_id)
    
        if not check_exists:
            return False
        
        check_exists = gas_station_operator_repository.get_gas_station_operator_by_id(favorite_route.operator_gas_station_id)

        if not check_exists:
            return False

        query = ("UPDATE public.favorite_route SET point_departure=%s, point_arrival=%s, travel_time=%s, route_length=%s, fuel_type=%s, fuel_volume=%s,"
                 " fuel_cost=%s, date=%s, user_id=%s, operator_gas_station_id=%s WHERE id=%s;")
        
        params = (favorite_route.point_departure, favorite_route.point_arrival, favorite_route.travel_time, favorite_route.route_length, 
              favorite_route.fuel_type, favorite_route.fuel_volume, favorite_route.fuel_cost, favorite_route.date, 
              favorite_route.user_id, favorite_route.operator_gas_station_id, id)

        db.execute_query(query, params)

        return get_favorite_route_by_id(id)
    except:
        return False


def delete_favorite_route_by_id(id: int):
    check_favorite_route_exist = get_favorite_route_by_id(id)

    if not check_favorite_route_exist:
        return False

    query = "DELETE FROM public.favorite_route WHERE id=%s;"
    db.execute_query(query, (id,))

    return True
