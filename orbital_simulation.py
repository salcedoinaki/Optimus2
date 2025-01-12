import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from skyfield.api import load, EarthSatellite
from datetime import datetime

# Input your provided TLE
tle_name = "Your_Satellite"
tle_line1 = "1 70331U 23075AJ  24011.37034722  .00003363  00000+0  18158-3 0  9992"
tle_line2 = "2 70331  97.5031  53.7075 0012743 113.2628 246.9522 15.19071188 19047"

# Create an EarthSatellite object using your provided TLE
satellite = EarthSatellite(tle_line1, tle_line2, tle_name, load.timescale())

# Time setup
ts = load.timescale()
now = datetime.utcnow()
times = ts.utc(now.year, now.month, now.day, range(0, 1440, 10))  # Every 10 minutes for 24 hours

# Compute sub-satellite points
subsatellite_points = []
for t in times:
    geocentric = satellite.at(t)  # Get the geocentric position
    subpoint = geocentric.subpoint()  # Calculate sub-satellite point
    subsatellite_points.append((subpoint.latitude.degrees, subpoint.longitude.degrees))

# Extract latitudes and longitudes
lats, lons = zip(*subsatellite_points)

# Create a map projection using Cartopy
fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_global()

# Add features to the map
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAND, edgecolor='black')

# Plot the satellite ground track
ax.plot(lons, lats, color='red', marker='o', markersize=2, transform=ccrs.Geodetic(), label='Satellite Ground Track')

# Add day/night shading
from cartopy.feature.nightshade import Nightshade
ax.add_feature(Nightshade(datetime.utcnow(), alpha=0.2))

# Add title and legend
plt.title("Satellite Ground Track for {tle_name} (24 Hours)")
plt.legend()
plt.show()
