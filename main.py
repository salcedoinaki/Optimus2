from satellite import get_satellite_path
from target_list import targets
from scheduler import greedy_schedule
from visualizer import plot_path_and_targets
from skyfield.api import load, EarthSatellite

# def main():
#     print("Starting the Satellite Mission Planner...")

#     # TLE Data
#     tle_name = "Your_Satellite"
#     tle_line1 = "1 70331U 23075AJ  24011.37034722  .00003363  00000+0  18158-3 0  9992"
#     tle_line2 = "2 70331  97.5031  53.7075 0012743 113.2628 246.9522 15.19071188 19047"

#     # Satellite Object
#     ts = load.timescale()
#     satellite = EarthSatellite(tle_line1, tle_line2, tle_name, ts)

#     # Number of orbits to simulate
#     num_orbits = 3

#     # Get Satellite Path and Swath Edges
#     satellite_path, left_swath, right_swath = get_satellite_path(satellite, num_orbits)

#     # Greedy Scheduling Algorithm
#     scheduled_targets = greedy_schedule(satellite_path, targets)

#     # Plot Results
#     print("Plotting results...")
#     plot_path_and_targets(satellite_path, left_swath, right_swath, targets, scheduled_targets)

def main():
    print("Starting the Satellite Mission Planner...")

    # TLE Data
    tle_name = "Your_Satellite"
    tle_line1 = "1 70331U 23075AJ  24011.37034722  .00003363  00000+0  18158-3 0  9992"
    tle_line2 = "2 70331  97.5031  53.7075 0012743 113.2628 246.9522 15.19071188 19047"

    ts = load.timescale()
    satellite = EarthSatellite(tle_line1, tle_line2, tle_name, ts)

    num_orbits = 20
    satellite_path, left_swath, right_swath = get_satellite_path(satellite, num_orbits)

    # Now the scheduler returns a list of captures with Euler angles
    scheduled_captures = greedy_schedule(satellite_path, targets)

    # Print out each scheduled capture with Euler angles
    for capture in scheduled_captures:
        target_lat, target_lon = capture['target']
        yaw_deg = capture['yaw_deg']
        pitch_deg = capture['pitch_deg']
        roll_deg = capture['roll_deg']
        print(f"Target {target_lat:.2f},{target_lon:.2f} -> "
              f"Yaw={yaw_deg:.2f}°, Pitch={pitch_deg:.2f}°")

    print("Plotting results...")
    # If you only need the target lat/lons for plotting:
    plotted_targets = [cap['target'] for cap in scheduled_captures]
    plot_path_and_targets(
        [(p['lat'], p['lon']) for p in satellite_path],
        left_swath,
        right_swath,
        targets,
        plotted_targets
    )

if __name__ == "__main__":
    main()
