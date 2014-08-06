import unittest
import time

from model import utils


class UtilsTests(unittest.TestCase):

    def test_ignore_ignores_error(self):
        try:
            with utils.ignore(ZeroDivisionError):
                undef = 1 / 0.
                success = False
            success = True
        except Exception:
            success = False

        self.assertTrue(success)

    def test_ignore_ignores_multiple(self):
        success = True

        try:
            with utils.ignore(ZeroDivisionError, KeyError):
                x = {}['key']
                success = False
            success = True
        except Exception:
            success = False

        self.assertTrue(success)

    def test_cached_decreases_computation_time(self):
        def uncached(x):
            time.sleep(0.01)
            return x

        @utils.cached
        def cached(x):
            time.sleep(0.01)
            return x

        uncached_init_time = time.time()
        for __ in xrange(10):
            uncached(1)
        uncached_final_time = time.time()

        cached_init_time = time.time()
        for __ in xrange(10):
            cached(1)
        cached_final_time = time.time()

        uncached_total_time = uncached_final_time - uncached_init_time
        cached_total_time = cached_final_time - cached_init_time

        self.assertLess(cached_total_time, uncached_total_time)

    def test_first_argument(self):
        pass  # TODO

    def test_second_argument(self):
        pass  # TODO

    def test_scale_float(self):
        self.assertEqual(utils.scale_float(0.5, 0, 10), 5)
        self.assertEqual(utils.scale_float(0.5, 1, 11), 6)
        self.assertEqual(utils.scale_float(0.5, 0, 1.), 0.5)


if __name__ == '__main__':
    unittest.main()