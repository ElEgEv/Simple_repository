import json

from src.core.database.database import db
from src.core.repository import gas_station_repository, user_auto_repository, gas_station_operator_repository


def get_all_cities():
    query = "SELECT * FROM public.city;"
    cities = db.fetch_all(query)

    return cities


def get_city_by_id(city_id: int):
    query = "SELECT * FROM public.city WHERE id=%s;"
    cities = db.fetch_one(query, (city_id,))

    return cities


def get_cities_by_start_sity_id(start_sity_id: int):
    query = "SELECT c.* FROM public.city AS c RIGHT JOIN public.map_route AS mr ON c.id = mr.finish_sity_id WHERE mr.start_city_id=%s;"
    cities = db.fetch_all(query, (start_sity_id,))

    return cities


def get_route_by_start_and_finish_id(
    start_city_id: int, 
    finish_city_id: int,
    gas_station_operator_id: int, 
    fuel_type: str, 
    start_fuel: float,
    user_car_id: int, 
):
    query = "SELECT * FROM public.map_route WHERE start_city_id=%s AND finish_sity_id=%s;"
    route = db.fetch_one(query, (start_city_id, finish_city_id,))
    
    # decode main info about route
    route['route_data'] = json.loads(route['route_data'])
    
    # add info about start city
    route['city_start'] = get_city_by_id(start_city_id)
    route['city_start']['coords'] = route['city_start']['coords'].split(',')
    
    # add info about finish city
    route['city_finish'] = get_city_by_id(finish_city_id)
    route['city_finish']['coords'] = route['city_finish']['coords'].split(',')
    
    support_list = route['city_start']['coords']
    support_list.append(0) 
    full_coords = [support_list]
    total_full_coords = [support_list]
       
    del route['start_city_id']
    del route['finish_sity_id']
     
    # add info about gas station
    if gas_station_operator_id:
        route['route_data'] = {f"{gas_station_operator_id}" : route['route_data'][f"{gas_station_operator_id}"]}
        
    full_rout_data = {}
    
    operator_name = []

    for operator in route['route_data']:
        full_data_by_operator = []
        
        operator_data = gas_station_operator_repository.get_gas_station_operator_by_id(int(operator))
        
        operator_name.append({operator_data['id'] : operator_data['name']})
        
        for gas_station in route['route_data'][operator]:
            support_obj = {}
        
            support_obj['info'] = gas_station_repository.get_gas_station_by_id(gas_station[0])
            
            if fuel_type and fuel_type not in support_obj['info']:
                continue
            
            if fuel_type and support_obj['info'][fuel_type] <= 0.0:
                continue
                
            support_obj['position'] = gas_station[1]
            support_obj['operator_name'] = operator_data['name']
            full_data_by_operator.append(support_obj)
            
        full_rout_data[operator] = full_data_by_operator
        
    route['operator_name'] = operator_name
    route['route_data'] = full_rout_data
    
    total_fuel_price = 0.0
    total_fuel_volume = 0.0
    need_gas_station_ids = []
    
    # find needed gas station
    if user_car_id and gas_station_operator_id:
        user_car = user_auto_repository.get_auto_by_id(user_car_id)
        
        kilometers_traveled = 0.0
  
        can_be_flooded = user_car['fuel_tank_capacity'] - start_fuel
        
        count_gas_station = len(route['route_data'][f"{gas_station_operator_id}"])

        for index, gas_station in enumerate(route['route_data'][f"{gas_station_operator_id}"]):
            drive_km = gas_station['position'] - kilometers_traveled
            kilometers_traveled += drive_km
            
            fuel_to_station = drive_km / 100 * user_car['fuel_consumption']
            can_be_flooded += fuel_to_station
            
            # print(f"Пройденно: {kilometers_traveled}")
            # print(f"Можно дозаправить: {can_be_flooded}")
            # print(f"Осталось топлива: {user_car['fuel_tank_capacity'] - can_be_flooded}")
            
            # на первую и последнюю заправки точно заезжем
            if index != 0 and index < count_gas_station - 1:
                remaining_fuel = user_car['fuel_tank_capacity'] - can_be_flooded
                
                # если на остатках можем дотянуть до следующей заправки - то едем
                if (remaining_fuel / user_car['fuel_consumption'] * 100) >= route['route_data'][f"{gas_station_operator_id}"][index + 1]['position'] - kilometers_traveled:
                    # print("---------")
                    continue
            
            total_fuel_price += gas_station['info'][fuel_type] * can_be_flooded
            total_fuel_volume += can_be_flooded
            
            # print(f"ЗАЛИЛИ {can_be_flooded}")
            # print("---------")
            
            can_be_flooded = 0
            need_gas_station_ids.append(gas_station['info']['id'])
            
    route['total_fuel_price'] = total_fuel_price
    route['total_fuel_volume'] = total_fuel_volume
    route['need_gas_station_ids'] = need_gas_station_ids
    
    if not len(need_gas_station_ids):
        for elem in route['route_data']:
            for station in route['route_data'][elem]:
                support_list_data = station['info']['coords'].split(',')
                support_list_data.append(station['position'])
                support_list_data.append(station['operator_name'])
                full_coords.append(support_list_data)
    else:
        for elem in route['route_data'][f"{gas_station_operator_id}"]:
            support_list_data = elem['info']['coords'].split(',')
            support_list_data.append(elem['position'])
            support_list_data.append(elem['operator_name'])
            
            if elem['info']['id'] in need_gas_station_ids:
                full_coords.append(support_list_data)
                
            total_full_coords.append(support_list_data)
    
    support_list = route['city_finish']['coords']
    support_list.append(route['route_length'])
    
    full_coords.append(support_list)
    total_full_coords.append(support_list)
    
    full_coords.sort(key=lambda x: x[2])
    
    route['full_coords'] = full_coords
    route['total_full_coords'] = total_full_coords

    return route
