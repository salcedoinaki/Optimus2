import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

def plot_path_and_targets(satellite_path, left_swath, right_swath, targets, scheduled_targets):
    fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_global()
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Plot satellite path
    lats, lons = zip(*satellite_path)
    ax.plot(lons, lats, color='red', linewidth=1, transform=ccrs.Geodetic(), label='Satellite Path')

    # Plot left and right swath edges
    left_lats, left_lons = zip(*left_swath)
    right_lats, right_lons = zip(*right_swath)
    ax.plot(left_lons, left_lats, color='blue', linewidth=0.5, transform=ccrs.Geodetic(), label='Left Swath Edge')
    ax.plot(right_lons, right_lats, color='green', linewidth=0.5, transform=ccrs.Geodetic(), label='Right Swath Edge')

    # Plot targets
    target_lats, target_lons = zip(*targets)
    ax.scatter(target_lons, target_lats, color='blue', marker='o', label='Targets', transform=ccrs.PlateCarree())

    # Plot scheduled targets with a larger star marker
    if scheduled_targets:
        scheduled_lats, scheduled_lons = zip(*scheduled_targets)
        ax.scatter(scheduled_lons, scheduled_lats, color='#FFD700', marker='*', s=100, label='Scheduled Targets', transform=ccrs.PlateCarree())

    # Add title and legend
    plt.title("Satellite Path and Target Locations")
    plt.legend()
    plt.show()
