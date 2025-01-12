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
        time_list.append(ts.utc(
            current_time.year, current_time.month, current_time.day,
            current_time.hour, current_time.minute, current_time.second
        ))
        current_time += timedelta(seconds=10)

    # Swath width setup (75 km on each side)
    swath_half_width_km = 75

    satellite_path = []
    left_swath = []
    right_swath = []

    earth_radius_km = 6371

    for t in time_list:
        geocentric = satellite.at(t)
        subpoint = geocentric.subpoint()

        # --- Store position (lat/lon) ---
        lat_deg = subpoint.latitude.degrees
        lon_deg = subpoint.longitude.degrees

        # --- Store velocity (vx, vy, vz) in ECI or TEME ---
        #   geocentric.velocity.km_per_s returns (vx, vy, vz) in the inertial frame used by Skyfield
        vx, vy, vz = geocentric.velocity.km_per_s

        # Save the path with added velocity data
        satellite_path.append({
            'lat': lat_deg,
            'lon': lon_deg,
            'vx': vx,
            'vy': vy,
            'vz': vz,
            'time_ts': t  # Keep the Skyfield time if you want
        })

        # Satellite altitude
        position = geocentric.position.km
        altitude_km = (position[0]**2 + position[1]**2 + position[2]**2)**0.5 - earth_radius_km

        # Swath offset in radians
        swath_offset_rad = swath_half_width_km / earth_radius_km

        # Approximate "heading" in XY-plane for the satellite ground track
        heading = atan2(vy, vx)

        # Left swath edge
        left_lat = subpoint.latitude.radians + swath_offset_rad * cos(heading)
        left_lon = subpoint.longitude.radians + swath_offset_rad * sin(heading)
        left_swath.append((degrees(left_lat), degrees(left_lon)))

        # Right swath edge
        right_lat = subpoint.latitude.radians - swath_offset_rad * cos(heading)
        right_lon = subpoint.longitude.radians - swath_offset_rad * sin(heading)
        right_swath.append((degrees(right_lat), degrees(right_lon)))

    return satellite_path, left_swath, right_swath
