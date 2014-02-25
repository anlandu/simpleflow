# -*- coding:utf-8 -*-
import unittest
import logging
import itertools

from cdf.log import logger
from cdf.streams.masks import follow_mask, NOFOLLOW_MASKS

logger.setLevel(logging.DEBUG)


class TestMasks(unittest.TestCase):

    def setUp(self):
        pass

    def test_follow(self):
        # 0 and 8 means follow
        self.assertEquals(follow_mask("0"), ["follow"])
        self.assertEquals(follow_mask("8"), ["follow"])

    def test_nofollow(self):
        # Bitmask test
        for L in range(1, len(NOFOLLOW_MASKS) + 1):
            for subset in itertools.combinations(NOFOLLOW_MASKS, L):
                counter = sum(k[0] for k in subset)
                self.assertEquals(follow_mask(str(counter)), [k[1] for k in subset])