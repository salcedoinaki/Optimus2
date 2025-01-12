import math 
from geopy.distance import great_circle

# def greedy_schedule(satellite_path, targets):
#     scheduled_targets = []
#     covered_targets = set()

#     for path_point in satellite_path:
#         path_lat, path_lon = path_point

#         for target in targets:
#             if target not in covered_targets:
#                 distance = great_circle((path_lat, path_lon), target).km
#                 if distance <= 75:
#                     scheduled_targets.append(target)
#                     covered_targets.add(target)

#     print(f"Scheduled {len(scheduled_targets)} targets.")
#     return scheduled_targets

def greedy_schedule(satellite_path, targets):
    scheduled_captures = []
    covered_targets = set()

    for path_point in satellite_path:
        lat = path_point['lat']
        lon = path_point['lon']
        vx  = path_point['vx']
        vy  = path_point['vy']
        vz  = path_point['vz']
        # time_ts = path_point['time_ts']  # if needed

        for target in targets:
            if target not in covered_targets:
                distance = great_circle((lat, lon), target).km
                if distance <= 75:
                    # We schedule the target at this path point
                    covered_targets.add(target)

                    # Compute Euler angles for this capture moment
                    yaw_deg, pitch_deg, roll_deg = compute_euler_angles(vx, vy, vz)

                    # Store everything in a list/dict
                    scheduled_captures.append({
                        'target': target,
                        'path_lat': lat,
                        'path_lon': lon,
                        'yaw_deg': yaw_deg,
                        'pitch_deg': pitch_deg,
                        'roll_deg': roll_deg
                        # 'time_ts': time_ts, if you want time
                    })

    print(f"Scheduled {len(scheduled_captures)} targets.")
    return scheduled_captures


def compute_euler_angles(vx, vy, vz):
    """
    Very simplified approach:
      - Yaw   = atan2(vy, vx)
      - Pitch = atan2(-vz, sqrt(vx^2 + vy^2))
      - Roll  = 0
    Returns angles in degrees.
    """
    yaw_rad = math.atan2(vy, vx)  # range -pi..pi
    pitch_rad = math.atan2(-vz, math.sqrt(vx*vx + vy*vy))
    roll_rad = 0.0

    yaw_deg = math.degrees(yaw_rad)
    pitch_deg = math.degrees(pitch_rad)
    roll_deg = math.degrees(roll_rad)

    return yaw_deg, pitch_deg, roll_deg
