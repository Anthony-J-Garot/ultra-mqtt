"""
Unit test all the things!
"""
import unittest
import simulators


class MockDevice:
    is_connected = lambda x: True
    send_state = lambda state, time_like: None


class UltraMqttTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # The test runner normally sets DEBUG to False.
        # This can be set using the --debug-mode flag on manage.py.
        # It can also be set here; which overrides the test runner --debug-mode flag.
        # settings.DEBUG = True

        # Then call the super to load the fixture data (the old way) and
        # set up the tearDown class.
        super(UltraMqttTestCase, cls).setUpClass()

        print()
        print("----> START unittest output below <----")
        print()

    # Run before each test
    def setUp(self):
        # print("UT>setUp")
        print()
        print()

    def tearDown(self):
        # print("UT>tearDown")
        pass

    # ./runtests.sh test_simulators test_space_usage
    def test_space_usage(self):
        device = MockDevice()

        result = simulators.space_usage(device)
        self.assertTrue(result, "Should have sent space usage")

    # ./runtests.sh test_simulators test_random_scatter
    def test_random_scatter(self):
        device = MockDevice()

        result = simulators.space_usage(device)
        self.assertTrue(result, "Should have sent random usage")


if __name__ == '__main__':
    unittest.main()
