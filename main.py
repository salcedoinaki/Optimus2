from satellite import get_satellite_path
from target_list import targets
from scheduler import greedy_schedule
from visualizer import plot_path_and_targets
from skyfield.api import load, EarthSatellite

def main():
    # Debugging start point
    print("Starting the Satellite Mission Planner...")

    # Satellite TLE data
    tle_name = "Your_Satellite"
    tle_line1 = "1 25544U 98067A   24011.54791667  .00016717  00000-0  10270-3 0  9007"
    tle_line2 = "2 25544  51.6423 217.5805 0007411 281.3912 148.7028 15.49786621298750"

    # Load satellite data
    ts = load.timescale()
    satellite = EarthSatellite(tle_line1, tle_line2, tle_name, ts)

    # Get satellite path for 3 orbits
    num_orbits = 5
    satellite_path = get_satellite_path(satellite, num_orbits)

    # Debug output
    print(f"Satellite path calculated. Path contains {len(satellite_path)} points.")
    print(f"Targets: {targets}")

    # Run greedy scheduling algorithm
    scheduled_targets = greedy_schedule(satellite_path, targets)

    # Debug output
    print(f"Scheduled {len(scheduled_targets)} targets.")

    # Plot the satellite path and targets
    plot_path_and_targets(satellite_path, targets, scheduled_targets)

# Ensure the script runs when executed directly
if __name__ == "__main__":
    main()
