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

    def test_root_name(self):
        skeleton = Skeleton(self._reader, 2)
        name = 'Hips'
        self.assertEqual(skeleton.root.name, name)

    def test_root_transform_parent(self):
        skeleton = Skeleton(self._reader, 2)
        transform_parent = mat4().identity()
        self.assertEqual(skeleton.root.transform_parent, transform_parent)

    def test_root_children_size(self):
        skeleton = Skeleton(self._reader, 2)
        self.assertEqual(len(skeleton.root.children), 3)

    def test_root_children_names(self):
        skeleton = Skeleton(self._reader, 2)
        names = ['Spine1', 'LeftUpLeg', 'RightUpLeg']
        children_names = [
            skeleton.root.children[0].name,
            skeleton.root.children[1].name,
            skeleton.root.children[2].name,
        ]
        self.assertEqual(children_names, names)

    def test_root_transform(self):
        skeleton = Skeleton(self._reader, 2)
        transform = mat4(
            0, 1, 0, 0,
            0, 0, -1, 0,
            -1, 0, 0, 0,
            0, 0, 0, 1
        )

        TestUtility().assertAlmostEqual_mat4(transform, skeleton.root.transform, 12)


class TestJoint(TestCase):
    pass