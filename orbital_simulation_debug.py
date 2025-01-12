import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.patches import Polygon
from skyfield.api import load, EarthSatellite
from datetime import datetime, timezone, timedelta
from math import pi, atan2, cos, sin, radians, degrees
import numpy as np

# Input your provided TLE
tle_name = "Your_Satellite"
tle_line1 = "1 70331U 23075AJ  24011.37034722  .00003363  00000+0  18158-3 0  9992"
tle_line2 = "2 70331  97.5031  53.7075 0012743 113.2628 246.9522 15.19071188 19047"

# Create an EarthSatellite object
satellite = EarthSatellite(tle_line1, tle_line2, tle_name, load.timescale())

# Calculate the orbital period in minutes
no_kozai = satellite.model.no_kozai
mean_motion_revolutions_per_day = (no_kozai * 1440) / (2 * pi)
orbital_period = 1440 / mean_motion_revolutions_per_day
print(f"Orbital Period: {orbital_period:.2f} minutes")

# Time setup
ts = load.timescale()
now = datetime.now(timezone.utc)
end_time = now + timedelta(minutes=orbital_period)

# Generate time intervals
time_list = []
current_time = now
while current_time <= end_time:
    time_list.append(ts.utc(current_time.year, current_time.month, current_time.day, current_time.hour, current_time.minute, current_time.second))
    current_time += timedelta(seconds=10)

# Swath width setup (150 km total width, 75 km on each side)
swath_half_width_km = 75
earth_radius_km = 6371

# Compute sub-satellite points and swath edges
subsatellite_points = []
left_swath = []
right_swath = []

for t in time_list:
    geocentric = satellite.at(t)
    subpoint = geocentric.subpoint()
    subsatellite_points.append((subpoint.latitude.degrees, subpoint.longitude.degrees))

    # Calculate satellite heading
    velocity = geocentric.velocity.km_per_s
    heading = atan2(velocity[1], velocity[0])

    # Calculate swath edges
    swath_offset_rad = swath_half_width_km / earth_radius_km

    left_lat = subpoint.latitude.radians + swath_offset_rad * cos(heading)
    left_lon = subpoint.longitude.radians + swath_offset_rad * sin(heading)
    right_lat = subpoint.latitude.radians - swath_offset_rad * cos(heading)
    right_lon = subpoint.longitude.radians - swath_offset_rad * sin(heading)

    left_swath.append((degrees(left_lat), degrees(left_lon)))
    right_swath.append((degrees(right_lat), degrees(right_lon)))

# Function to normalize longitudes to the range [-180, 180]
def normalize_longitudes(longitudes):
    return [(lon + 180) % 360 - 180 for lon in longitudes]

# Normalize longitudes
left_lons = normalize_longitudes([lon for lat, lon in left_swath])
right_lons = normalize_longitudes([lon for lat, lon in right_swath])

# Create map projection
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_global()

# Add map features
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, edgecolor='black')

# Plot ground track
lats, lons = zip(*subsatellite_points)
ax.plot(lons, lats, color='red', linewidth=1, transform=ccrs.Geodetic(), label='Satellite Ground Track')

# Plot swath edges
left_lats, _ = zip(*left_swath)
right_lats, _ = zip(*right_swath)
ax.plot(left_lons, left_lats, color='blue', linewidth=0.5, transform=ccrs.Geodetic(), label='Left Swath Edge')
ax.plot(right_lons, right_lats, color='green', linewidth=0.5, transform=ccrs.Geodetic(), label='Right Swath Edge')


# Add day/night shading
from cartopy.feature.nightshade import Nightshade
ax.add_feature(Nightshade(datetime.now(timezone.utc), alpha=0.2))

# Add title and legend
plt.title(f"Satellite Ground Track and Swath Coverage for {tle_name} (One Complete Orbit)")
plt.legend()
plt.show()
