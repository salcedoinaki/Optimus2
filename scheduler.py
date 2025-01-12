from geopy.distance import great_circle

def greedy_schedule(satellite_path, targets):
    scheduled_targets = []
    covered_targets = set()

    for path_point in satellite_path:
        path_lat, path_lon = path_point

        for target in targets:
            if target not in covered_targets:
                distance = great_circle((path_lat, path_lon), target).km
                if distance <= 75:
                    scheduled_targets.append(target)
                    covered_targets.add(target)

    print(f"Scheduled {len(scheduled_targets)} targets.")
    return scheduled_targets
