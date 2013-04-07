__author__ = 'Erik S Carlsten'


from cgkit.bvhimport import BVHReader
from unittest import TestCase

from src.skeleton import Skeleton


class TestSkeleton(TestCase):
    def test_skeleton_constructor(self):
        reader = BVHReader('test_bvh_data.bvh')
        reader.read()
        skeleton = Skeleton(reader, 2)
        assert isinstance(skeleton, Skeleton)


class TestJoint(TestCase):
    pass