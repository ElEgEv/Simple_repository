from src.core.repository import user_repository, favorite_route_repository, gas_station_operator_repository

def checkEntityAlreadyExists(entity_type, data):
    if entity_type == 'user':
        result = user_repository.get_user_by_email(data.login)

        if result:
            return False
        
    return True

def get_statistic_for_user_by_period(start: int, end: int, user_id: int, operator_gas_station_id: int):    
    # try:
        check_user = user_repository.get_user_by_id(user_id)
    
        if not check_user:
            return False
        
        favorite_routes = favorite_route_repository.get_all_favorite_routes_by_period(start, end, user_id, operator_gas_station_id)
        
        operator_gas_station = []
        
        if operator_gas_station_id:
            operator_gas_station.append(gas_station_operator_repository.get_gas_station_operator_by_id(operator_gas_station_id))
        else:
            operator_gas_station = gas_station_operator_repository.get_all_gas_station_operators()
        
        if not favorite_routes or not operator_gas_station:
            return []
        
        result_dict = {
            "total_len_route": 0.0,
            "total_price": 0.0
        }
        
        for operator in operator_gas_station:
            if operator["name"] == "DEFAULT":
                continue
            
            operator_dict = {
                "len_route": 0.0,
                "price": 0.0
            }
            
            routes_data = []

            for favorite_route in favorite_routes:
                if favorite_route["operator_gas_station_id"] == operator["id"]:
                    routes_data.append({
                        "date": favorite_route["date"],
                        "route_length": favorite_route["route_length"],
                        "fuel_cost": favorite_route["fuel_cost"],
                    })
                    
                    operator_dict["len_route"] += favorite_route["route_length"]
                    operator_dict["price"] += favorite_route["fuel_cost"]
                    
            operator_dict["routes_data"] = routes_data
            result_dict[operator["name"]] = operator_dict
            result_dict["total_len_route"] += operator_dict["len_route"]
            result_dict["total_price"] += operator_dict["price"]
            
        result_dict["all_routes"] = favorite_routes

        return result_dict
    # except Exception as e:
    #     return {}
    


def get_full_statistic_for_user(user_id: int):
    result_dict = {
        "len_route": 0.0,
        "price": 0.0,
        "travel_time" : 0.0
    }
            
    try:
        check_user = user_repository.get_user_by_id(user_id)
        
        if not check_user:
            return False

        favorite_routes = favorite_route_repository.get_all_favorite_routes_by_user_id(user_id)
        
        if favorite_routes:
            for favorite_route in favorite_routes:
                result_dict["len_route"] += favorite_route["route_length"]
                result_dict["price"] += favorite_route["fuel_cost"]
                
                travel_time = favorite_route["travel_time"].replace(' ч ', ';').replace(' мин', '').split(';')
                
                result_dict["travel_time"] += float(travel_time[0]) + round(float(travel_time[0]) / 60, 2)

        return [result_dict]
    except Exception as e:
        return [result_dict]