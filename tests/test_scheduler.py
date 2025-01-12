import unittest
from scheduler import greedy_schedule, compute_euler_angles

class TestScheduler(unittest.TestCase):
    def test_compute_euler_angles_basic(self):
        """
        Check if compute_euler_angles produces the expected yaw/pitch/roll
        when we have a simple velocity vector along +x.
        """
        vx, vy, vz = 7.5, 0, 0  # e.g. purely along +X
        yaw_deg, pitch_deg, roll_deg = compute_euler_angles(vx, vy, vz)
        # Expect yaw near 0°, pitch near 0°, roll 0° (using the simple velocity-based logic).
        self.assertAlmostEqual(yaw_deg, 0, delta=0.01)
        self.assertAlmostEqual(pitch_deg, 0, delta=0.01)
        self.assertAlmostEqual(roll_deg, 0, delta=0.01)

    def test_greedy_schedule_basic(self):
        """
        Test if greedy_schedule returns a capture for a target that is
        definitely within 75 km of the path.
        """
        # Minimal path: one point near lat=0, lon=0
        satellite_path = [{
            'lat': 0.0,
            'lon': 0.0,
            'vx': 7.5,
            'vy': 0,
            'vz': 0
        }]
        # Target is the same spot
        targets = [(0.0, 0.0)]
        scheduled_captures = greedy_schedule(satellite_path, targets)
        
        self.assertEqual(len(scheduled_captures), 1)
        self.assertEqual(scheduled_captures[0]['target'], (0.0, 0.0))

if __name__ == '__main__':
    unittest.main()
