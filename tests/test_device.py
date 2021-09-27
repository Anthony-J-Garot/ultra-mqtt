"""
Unit test all the things!
"""
import unittest
import utils
from datetime import datetime


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

    # ./runtests.sh test_utils test_log
    def test_log(self):
        msg = "Hello"
        now = datetime.now()
        expected = f"{now.strftime('%H:%M:%S')}> {msg}"
        result = utils.log(msg, now)
        self.assertEqual(expected, result, "Log should have returned consistent log message")


if __name__ == '__main__':
    unittest.main()
