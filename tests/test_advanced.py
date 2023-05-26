# -*- coding: utf-8 -*-

from .context import reqpy

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(reqpy.hmm()) # type: ignore


if __name__ == '__main__':
    unittest.main()
