import unittest
from skyfield.api import load, EarthSatellite
from satellite import get_satellite_path

class TestSatellite(unittest.TestCase):
    def test_get_satellite_path(self):
        """
        Use a dummy TLE to ensure get_satellite_path returns a non-empty list
        of path points. Also check that each path entry has the expected keys.
        """
        ts = load.timescale()
        tle_name = "Test_Satellite"
        tle_line1 = "1 70000U 20001A   20001.00000000 -.00000023  00000-0  00000+0 0  9991"
        tle_line2 = "2 70000  98.7000  30.3000 0001000  80.0000 280.0000 14.50000000    02"
        satellite = EarthSatellite(tle_line1, tle_line2, tle_name, ts)

        satellite_path, left_swath, right_swath = get_satellite_path(satellite, num_orbits=1)

        # Check that we have some path points
        self.assertTrue(len(satellite_path) > 0, "satellite_path is empty!")
        
        # Check that each path point has the keys we expect
        for point in satellite_path:
            self.assertIn('lat', point)
            self.assertIn('lon', point)
            self.assertIn('vx', point)
            self.assertIn('vy', point)
            self.assertIn('vz', point)

if __name__ == '__main__':
    unittest.main()
