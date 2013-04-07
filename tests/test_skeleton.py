from cgkit.cgtypes import mat4
from cgkit.bvhimport import BVHReader
from unittest import TestCase

from src.skeleton import Skeleton
from testUtility import TestUtility

__author__ = 'Erik S Carlsten'


class TestSkeleton(TestCase):

    @classmethod
    def setUpClass(cls):
        cls._reader = BVHReader('test_bvh_data.bvh')
        cls._reader.read()

    def setUp(self):
        self.skeleton = Skeleton(self._reader, 2)

    def test_root_name(self):
        name = 'Hips'
        self.assertEqual(self.skeleton.root.name, name)

    def test_root_transform(self):
        transform = mat4(
            0, 1, 0, 0,
            0, 0, -1, 0,
            -1, 0, 0, 0,
            0, 0, 0, 1
        )

        TestUtility().assertAlmostEqual_mat4(transform, self.skeleton.root.transform, 12)


class TestJoint(TestCase):
    pass