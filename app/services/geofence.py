import math

def calculate_haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance in meters between two coordinates on Earth
    using the Haversine formula.
    """
    R = 6371000.0  # Earth's radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda / 2.0) ** 2))
    
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    distance = R * c
    return distance

def is_within_geofence(
    user_lat: float,
    user_lon: float,
    zone_lat: float,
    zone_lon: float,
    radius_meters: float
) -> tuple[bool, float]:
    """
    Check if a user coordinate falls within the allowed radius of a geofence zone.
    Returns (is_inside, distance_meters).
    """
    distance = calculate_haversine_distance(user_lat, user_lon, zone_lat, zone_lon)
    return (distance <= radius_meters, distance)
