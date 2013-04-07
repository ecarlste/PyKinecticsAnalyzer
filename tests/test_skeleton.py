from cgkit.cgtypes import mat4
from cgkit.bvhimport import BVHReader
from unittest import TestCase

from src.skeleton import Skeleton

__author__ = 'Erik S Carlsten'


class TestSkeleton(TestCase):

    @classmethod
    def setUpClass(cls):
        cls._reader = BVHReader('test_bvh_data.bvh')
        cls._reader.read()

    def setUp(self):
        self.skeleton = Skeleton(self._reader, 2)

    def test_root_transform(self):
        transform = mat4(
            0, 1, 0, 0,
            0, 0, -1, 0,
            -1, 0, 0, 0,
            0, 0, 0, 1
        )

        self.assertAlmostEqual_mat4(transform, self.skeleton.root.transform, 12)

    def assertAlmostEqual_mat4(self, first, second, places=7):
        difference = second - first
        difference_list = difference.toList()

        total_difference = 0
        for item in difference_list:
            total_difference += abs(item)

        total_difference = round(total_difference, places)

        self.assertEquals(total_difference, 0)


class TestJoint(TestCase):
    pass