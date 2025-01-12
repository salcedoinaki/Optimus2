from skyfield.api import load
from datetime import datetime, timezone, timedelta
from math import sin, cos, radians, degrees, atan2

def get_satellite_path(satellite, num_orbits=1):
    ts = load.timescale()

    # Calculate orbital period
    no_kozai = satellite.model.no_kozai
    orbital_period = 1440 / ((no_kozai * 1440) / (2 * 3.141592653589793))
    print(f"Orbital Period (minutes): {orbital_period:.2f}")

    # Time setup
    now = datetime.now(timezone.utc)
    end_time = now + timedelta(minutes=orbital_period * num_orbits)
    time_list = []
    current_time = now
    while current_time <= end_time:
        time_list.append(ts.utc(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second))
        current_time += timedelta(seconds=10)

    # Swath width setup (75 km on each side)
    swath_half_width_km = 75

    # Path and Swath Edges
    satellite_path = []
    left_swath = []
    right_swath = []

    for t in time_list:
        geocentric = satellite.at(t)
        subpoint = geocentric.subpoint()
        satellite_path.append((subpoint.latitude.degrees, subpoint.longitude.degrees))

        # Satellite altitude
        position = geocentric.position.km
        earth_radius_km = 6371
        altitude_km = (position[0]**2 + position[1]**2 + position[2]**2)**0.5 - earth_radius_km

        # Swath offset in radians
        swath_offset_rad = swath_half_width_km / earth_radius_km

        # Calculate heading
        velocity = geocentric.velocity.km_per_s
        heading = atan2(velocity[1], velocity[0])

        # Left swath edge
        left_lat = subpoint.latitude.radians + swath_offset_rad * cos(heading)
        left_lon = subpoint.longitude.radians + swath_offset_rad * sin(heading)
        left_swath.append((degrees(left_lat), degrees(left_lon)))

        # Right swath edge
        right_lat = subpoint.latitude.radians - swath_offset_rad * cos(heading)
        right_lon = subpoint.longitude.radians - swath_offset_rad * sin(heading)
        right_swath.append((degrees(right_lat), degrees(right_lon)))

    return satellite_path, left_swath, right_swath
