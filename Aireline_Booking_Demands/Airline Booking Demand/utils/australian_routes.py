# utils/australian_routes.py

def get_australian_domestic_routes():
    """
    Return a comprehensive list of major Australian domestic air routes.
    Each route includes origin, destination, and typical frequency.
    """
    
    routes = [
        # Major Capital City Routes (High Frequency)
        {"origin": "SYD", "destination": "MEL", "name": "Sydney - Melbourne", "frequency": "Very High", "distance": "713 km"},
        {"origin": "SYD", "destination": "BNE", "name": "Sydney - Brisbane", "frequency": "Very High", "distance": "732 km"},
        {"origin": "SYD", "destination": "PER", "name": "Sydney - Perth", "frequency": "High", "distance": "3290 km"},
        {"origin": "MEL", "destination": "BNE", "name": "Melbourne - Brisbane", "frequency": "High", "distance": "1370 km"},
        {"origin": "MEL", "destination": "PER", "name": "Melbourne - Perth", "frequency": "High", "distance": "2707 km"},
        {"origin": "BNE", "destination": "PER", "name": "Brisbane - Perth", "frequency": "Medium", "distance": "3605 km"},
        {"origin": "SYD", "destination": "ADL", "name": "Sydney - Adelaide", "frequency": "High", "distance": "1165 km"},
        {"origin": "MEL", "destination": "ADL", "name": "Melbourne - Adelaide", "frequency": "High", "distance": "654 km"},
        {"origin": "BNE", "destination": "ADL", "name": "Brisbane - Adelaide", "frequency": "Medium", "distance": "1630 km"},
        {"origin": "SYD", "destination": "CBR", "name": "Sydney - Canberra", "frequency": "Very High", "distance": "248 km"},
        {"origin": "MEL", "destination": "CBR", "name": "Melbourne - Canberra", "frequency": "High", "distance": "470 km"},
        {"origin": "SYD", "destination": "HBA", "name": "Sydney - Hobart", "frequency": "High", "distance": "1047 km"},
        {"origin": "MEL", "destination": "HBA", "name": "Melbourne - Hobart", "frequency": "High", "distance": "559 km"},
        {"origin": "SYD", "destination": "DRW", "name": "Sydney - Darwin", "frequency": "Medium", "distance": "3147 km"},
        {"origin": "MEL", "destination": "DRW", "name": "Melbourne - Darwin", "frequency": "Medium", "distance": "3156 km"},
        
        # Queensland Routes
        {"origin": "BNE", "destination": "CNS", "name": "Brisbane - Cairns", "frequency": "High", "distance": "1389 km"},
        {"origin": "SYD", "destination": "CNS", "name": "Sydney - Cairns", "frequency": "High", "distance": "1961 km"},
        {"origin": "MEL", "destination": "CNS", "name": "Melbourne - Cairns", "frequency": "Medium", "distance": "2043 km"},
        {"origin": "BNE", "destination": "TSV", "name": "Brisbane - Townsville", "frequency": "Medium", "distance": "1108 km"},
        {"origin": "CNS", "destination": "TSV", "name": "Cairns - Townsville", "frequency": "Medium", "distance": "285 km"},
        {"origin": "BNE", "destination": "OOL", "name": "Brisbane - Gold Coast", "frequency": "Very High", "distance": "78 km"},
        {"origin": "SYD", "destination": "OOL", "name": "Sydney - Gold Coast", "frequency": "High", "distance": "750 km"},
        {"origin": "MEL", "destination": "OOL", "name": "Melbourne - Gold Coast", "frequency": "High", "distance": "1388 km"},
        {"origin": "BNE", "destination": "MCY", "name": "Brisbane - Sunshine Coast", "frequency": "Medium", "distance": "95 km"},
        {"origin": "SYD", "destination": "MCY", "name": "Sydney - Sunshine Coast", "frequency": "Medium", "distance": "767 km"},
        {"origin": "BNE", "destination": "MKY", "name": "Brisbane - Mackay", "frequency": "Medium", "distance": "825 km"},
        {"origin": "BNE", "destination": "ROK", "name": "Brisbane - Rockhampton", "frequency": "Medium", "distance": "486 km"},
        {"origin": "BNE", "destination": "BDB", "name": "Brisbane - Bundaberg", "frequency": "Medium", "distance": "320 km"},
        {"origin": "BNE", "destination": "GLT", "name": "Brisbane - Gladstone", "frequency": "Medium", "distance": "400 km"},
        {"origin": "BNE", "destination": "HTI", "name": "Brisbane - Hamilton Island", "frequency": "Medium", "distance": "887 km"},
        {"origin": "CNS", "destination": "HTI", "name": "Cairns - Hamilton Island", "frequency": "Medium", "distance": "602 km"},
        
        # New South Wales Routes
        {"origin": "SYD", "destination": "NTL", "name": "Sydney - Newcastle", "frequency": "High", "distance": "123 km"},
        {"origin": "SYD", "destination": "CBR", "name": "Sydney - Canberra", "frequency": "Very High", "distance": "248 km"},
        {"origin": "SYD", "destination": "PQQ", "name": "Sydney - Port Macquarie", "frequency": "Medium", "distance": "308 km"},
        {"origin": "SYD", "destination": "CFS", "name": "Sydney - Coffs Harbour", "frequency": "Medium", "distance": "423 km"},
        {"origin": "SYD", "destination": "BNK", "name": "Sydney - Ballina", "frequency": "Medium", "distance": "572 km"},
        {"origin": "SYD", "destination": "TMW", "name": "Sydney - Tamworth", "frequency": "Medium", "distance": "320 km"},
        {"origin": "SYD", "destination": "WGA", "name": "Sydney - Wagga Wagga", "frequency": "Medium", "distance": "439 km"},
        {"origin": "SYD", "destination": "DBO", "name": "Sydney - Dubbo", "frequency": "Medium", "distance": "307 km"},
        {"origin": "SYD", "destination": "WOL", "name": "Sydney - Wollongong", "frequency": "Medium", "distance": "82 km"},
        
        # Victoria Routes
        {"origin": "MEL", "destination": "LST", "name": "Melbourne - Launceston", "frequency": "High", "distance": "451 km"},
        {"origin": "MEL", "destination": "HBA", "name": "Melbourne - Hobart", "frequency": "High", "distance": "559 km"},
        {"origin": "MEL", "destination": "BWT", "name": "Melbourne - Burnie", "frequency": "Medium", "distance": "481 km"},
        
        # South Australia Routes
        {"origin": "ADL", "destination": "DRW", "name": "Adelaide - Darwin", "frequency": "Medium", "distance": "2612 km"},
        {"origin": "ADL", "destination": "PER", "name": "Adelaide - Perth", "frequency": "Medium", "distance": "2125 km"},
        {"origin": "ADL", "destination": "CNS", "name": "Adelaide - Cairns", "frequency": "Medium", "distance": "2043 km"},
        
        # Western Australia Routes
        {"origin": "PER", "destination": "DRW", "name": "Perth - Darwin", "frequency": "Medium", "distance": "2649 km"},
        {"origin": "PER", "destination": "BME", "name": "Perth - Broome", "frequency": "Medium", "distance": "2203 km"},
        {"origin": "PER", "destination": "KGI", "name": "Perth - Kalgoorlie", "frequency": "Medium", "distance": "595 km"},
        {"origin": "PER", "destination": "ZNE", "name": "Perth - Newman", "frequency": "Medium", "distance": "1146 km"},
        
        # Northern Territory Routes
        {"origin": "DRW", "destination": "CNS", "name": "Darwin - Cairns", "frequency": "Medium", "distance": "1642 km"},
        {"origin": "DRW", "destination": "ASP", "name": "Darwin - Alice Springs", "frequency": "Medium", "distance": "1498 km"},
        {"origin": "DRW", "destination": "AYQ", "name": "Darwin - Ayers Rock", "frequency": "Low", "distance": "1960 km"},
        
        # Regional Routes
        {"origin": "CNS", "destination": "ASP", "name": "Cairns - Alice Springs", "frequency": "Low", "distance": "1920 km"},
        {"origin": "ASP", "destination": "AYQ", "name": "Alice Springs - Ayers Rock", "frequency": "Medium", "distance": "462 km"},
        {"origin": "ADL", "destination": "ASP", "name": "Adelaide - Alice Springs", "frequency": "Medium", "distance": "1532 km"},
        {"origin": "ADL", "destination": "AYQ", "name": "Adelaide - Ayers Rock", "frequency": "Low", "distance": "1994 km"},
        {"origin": "BNE", "destination": "ASP", "name": "Brisbane - Alice Springs", "frequency": "Low", "distance": "2040 km"},
        {"origin": "SYD", "destination": "ASP", "name": "Sydney - Alice Springs", "frequency": "Low", "distance": "1960 km"},
        {"origin": "MEL", "destination": "ASP", "name": "Melbourne - Alice Springs", "frequency": "Low", "distance": "2250 km"},
        
        # Island Routes
        {"origin": "BNE", "destination": "AYQ", "name": "Brisbane - Ayers Rock", "frequency": "Low", "distance": "2000 km"},
        {"origin": "SYD", "destination": "AYQ", "name": "Sydney - Ayers Rock", "frequency": "Low", "distance": "2100 km"},
        
        # Additional Regional Routes
        {"origin": "BNE", "destination": "EMD", "name": "Brisbane - Emerald", "frequency": "Low", "distance": "650 km"},
        {"origin": "BNE", "destination": "LRE", "name": "Brisbane - Longreach", "frequency": "Low", "distance": "1200 km"},
        {"origin": "BNE", "destination": "ISA", "name": "Brisbane - Mount Isa", "frequency": "Low", "distance": "1500 km"},
        {"origin": "BNE", "destination": "MRZ", "name": "Brisbane - Moree", "frequency": "Low", "distance": "450 km"},
        {"origin": "BNE", "destination": "GFF", "name": "Brisbane - Griffith", "frequency": "Low", "distance": "1000 km"},
        {"origin": "SYD", "destination": "MRZ", "name": "Sydney - Moree", "frequency": "Low", "distance": "520 km"},
        {"origin": "SYD", "destination": "GFF", "name": "Sydney - Griffith", "frequency": "Low", "distance": "570 km"},
        {"origin": "MEL", "destination": "GFF", "name": "Melbourne - Griffith", "frequency": "Low", "distance": "430 km"},
    ]
    
    return routes

def get_route_by_airports(origin, destination):
    """
    Get specific route information between two airports.
    """
    routes = get_australian_domestic_routes()
    
    for route in routes:
        if (route["origin"] == origin.upper() and route["destination"] == destination.upper()) or \
           (route["origin"] == destination.upper() and route["destination"] == origin.upper()):
            return route
    
    return None

def get_routes_from_airport(airport_code):
    """
    Get all routes departing from a specific airport.
    """
    routes = get_australian_domestic_routes()
    airport_routes = []
    
    for route in routes:
        if route["origin"] == airport_code.upper():
            airport_routes.append(route)
    
    return airport_routes

def get_routes_to_airport(airport_code):
    """
    Get all routes arriving at a specific airport.
    """
    routes = get_australian_domestic_routes()
    airport_routes = []
    
    for route in routes:
        if route["destination"] == airport_code.upper():
            airport_routes.append(route)
    
    return airport_routes 