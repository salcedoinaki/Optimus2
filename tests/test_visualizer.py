import unittest
from visualizer import plot_path_and_targets

class TestVisualizer(unittest.TestCase):
    def test_plot_smoke_test(self):
        """
        A smoke test to ensure that plot_path_and_targets runs without error.
        This doesn't guarantee correctness of the plot, but at least checks
        that it doesn't crash.
        """
        satellite_path = [(0, 0), (10, 10)]
        left_swath = [(0, 0)]
        right_swath = [(0, 0)]
        targets = [(5,5)]
        scheduled_targets = [(5,5)]

        try:
            plot_path_and_targets(satellite_path, left_swath, right_swath, targets, scheduled_targets)
        except Exception as e:
            self.fail(f"plot_path_and_targets raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
