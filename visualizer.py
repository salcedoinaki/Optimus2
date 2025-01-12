import matplotlib.pyplot as plt
import cartopy.crs as ccrs

# Plot satellite path and targets
def plot_path_and_targets(satellite_path, targets, scheduled_targets):
    path_lats, path_lons = zip(*satellite_path)

    fig, ax = plt.subplots(figsize=(16, 9), subplot_kw={'projection': ccrs.PlateCarree()})
    ax.set_global()

    ax.coastlines()
    ax.gridlines()

    # Plot the satellite path
    ax.plot(path_lons, path_lats, color='red', linewidth=1, transform=ccrs.Geodetic(), label='Satellite Path')

    # Plot the targets
    target_lats, target_lons = zip(*targets)
    ax.scatter(target_lons, target_lats, color='blue', s=10, label='Targets', transform=ccrs.Geodetic())

    # Plot the scheduled targets
    if scheduled_targets:
        scheduled_lats, scheduled_lons = zip(*scheduled_targets)
        ax.scatter(scheduled_lons, scheduled_lats, color='green', s=20, label='Scheduled Targets', transform=ccrs.Geodetic())

    plt.legend()
    plt.title("Satellite Path and Target Locations")
    plt.show()
