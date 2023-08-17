# -*- coding: utf-8 -*-

from .context import reqpy # type:ignore # noqa

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(None)


if __name__ == '__main__':
    unittest.main()
