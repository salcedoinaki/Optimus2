from geopy.distance import great_circle

# Greedy scheduling algorithm
def greedy_schedule(satellite_path, targets):
    scheduled_targets = []
    covered_targets = set()

    for path_lat, path_lon in satellite_path:
        for target in targets:
            if target not in covered_targets:
                distance = great_circle((path_lat, path_lon), target).km
                if distance <= 150:  # 150 km swath width
                    scheduled_targets.append(target)
                    covered_targets.add(target)

    return scheduled_targets
