from datetime import datetime, timezone, timedelta
from math import pi
from skyfield.api import load

def get_satellite_path(satellite, num_orbits=1):
    ts = load.timescale()  # Proper initialization

    # Debug: Print the mean motion
    mean_motion = satellite.model.no_kozai * (1440 / (2 * pi))  # Convert to revolutions per day
    print(f"Mean Motion (revolutions per day): {mean_motion:.6f}")

    if mean_motion <= 0 or mean_motion > 18:
        print("⚠️ Warning: Mean motion is outside the expected range. Using default value for testing.")
        orbital_period = 92  # Typical LEO period in minutes
    else:
        orbital_period = 1440 / mean_motion

    print(f"Orbital Period (minutes): {orbital_period}")

    # Calculate the total simulation duration
    total_duration = orbital_period * num_orbits
    print(f"Total Simulation Duration (minutes): {total_duration}")

    # Generate time intervals
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(minutes=total_duration)
    print(f"Start Time: {start_time}")
    print(f"End Time: {end_time}")

    time_list = []
    current_time = start_time
    while current_time <= end_time:
        time_list.append(ts.utc(current_time.year, current_time.month, current_time.day,
                                current_time.hour, current_time.minute, current_time.second))
        current_time += timedelta(seconds=10)  # Step size of 10 seconds

    # Return time points as the satellite path
    return [(satellite.at(t).subpoint().latitude.degrees, satellite.at(t).subpoint().longitude.degrees)
            for t in time_list]
