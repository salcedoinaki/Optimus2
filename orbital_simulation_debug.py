import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from skyfield.api import load, EarthSatellite
from datetime import datetime, timezone, timedelta
from math import pi, radians, degrees, atan2, cos, sin

# Input your provided TLE
tle_name = "Your_Satellite"
tle_line1 = "1 70331U 23075AJ  24011.37034722  .00003363  00000+0  18158-3 0  9992"
tle_line2 = "2 70331  97.5031  53.7075 0012743 113.2628 246.9522 15.19071188 19047"

# Create an EarthSatellite object using your provided TLE
satellite = EarthSatellite(tle_line1, tle_line2, tle_name, load.timescale())

# Calculate the orbital period in minutes
no_kozai = satellite.model.no_kozai  # Mean motion in radians per minute
mean_motion_revolutions_per_day = (no_kozai * 1440) / (2 * pi)  # Convert to revolutions per day
orbital_period = 1440 / mean_motion_revolutions_per_day  # Orbital period in minutes
print(f"Orbital Period: {orbital_period:.2f} minutes")

# Time setup: Start from now and calculate until the end of one orbit
ts = load.timescale()
now = datetime.now(timezone.utc)
end_time = now + timedelta(minutes=orbital_period)

# Generate time intervals manually (every 10 seconds)
time_list = []
current_time = now
while current_time <= end_time:
    time_list.append(ts.utc(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second))
    current_time += timedelta(seconds=10)  # Step size of 10 seconds

# Swath width setup (150 km total width, 75 km on each side)
swath_half_width_km = 75  # Half of the swath width

# Compute sub-satellite points and swath coverage
subsatellite_points = []
left_swath = []
right_swath = []

for t in time_list:
    geocentric = satellite.at(t)  # Get the geocentric position
    subpoint = geocentric.subpoint()  # Calculate sub-satellite point
    subsatellite_points.append((subpoint.latitude.degrees, subpoint.longitude.degrees))

    # Calculate the satellite's altitude
    position = satellite.at(t).position.km
    earth_radius_km = 6371  # Earth's average radius in km
    alt_km = (position[0]**2 + position[1]**2 + position[2]**2)**0.5 - earth_radius_km

    # Correct swath offset calculation
    swath_offset_rad = swath_half_width_km / earth_radius_km

    # Calculate the satellite's heading (azimuth)
    velocity = geocentric.velocity.km_per_s
    heading = atan2(velocity[1], velocity[0])  # Calculate azimuth in radians

    # Left swath edge
    left_lat = subpoint.latitude.radians + swath_offset_rad * cos(heading)
    left_lon = subpoint.longitude.radians + swath_offset_rad * sin(heading)
    left_swath.append((degrees(left_lat), degrees(left_lon)))

    # Right swath edge
    right_lat = subpoint.latitude.radians - swath_offset_rad * cos(heading)
    right_lon = subpoint.longitude.radians - swath_offset_rad * sin(heading)
    right_swath.append((degrees(right_lat), degrees(right_lon)))

# 🔍 Debugging Output: Print the first 10 sub-satellite points and swath edges
print("\nFirst 10 Sub-Satellite Points and Swath Edges:")
for i in range(10):
    print(f"{i+1}. Sub-Satellite Point: ({subsatellite_points[i][0]:.2f}, {subsatellite_points[i][1]:.2f}) | "
          f"Left Swath Edge: ({left_swath[i][0]:.2f}, {left_swath[i][1]:.2f}) | "
          f"Right Swath Edge: ({right_swath[i][0]:.2f}, {right_swath[i][1]:.2f})")

# Extract latitudes and longitudes
lats, lons = zip(*subsatellite_points)
left_lats, left_lons = zip(*left_swath)
right_lats, right_lons = zip(*right_swath)

# Create a map projection using Cartopy
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_global()

# Add features to the map
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, edgecolor='black')

# Plot the satellite ground track
ax.plot(lons, lats, color='red', linewidth=1, transform=ccrs.Geodetic(), label='Satellite Ground Track')

# Plot left and right swath edges
ax.plot(left_lons, left_lats, color='blue', linewidth=0.5, transform=ccrs.Geodetic(), label='Left Swath Edge')
ax.plot(right_lons, right_lats, color='green', linewidth=0.5, transform=ccrs.Geodetic(), label='Right Swath Edge')

# Add day/night shading
from cartopy.feature.nightshade import Nightshade
ax.add_feature(Nightshade(datetime.now(timezone.utc), alpha=0.2))

# Add title and legend
plt.title("Satellite Ground Track and Swath Coverage for {tle_name} (One Complete Orbit)")
plt.legend()
plt.show()
