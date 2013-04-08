from cgkit.cgtypes import mat4
from cgkit.bvhimport import BVHReader
from unittest import TestCase

from src.skeleton import Skeleton, Joint
from testUtility import TestUtility

__author__ = 'Erik S Carlsten'


class TestSkeleton(TestCase):

    @classmethod
    def setUpClass(cls):
        cls._reader = BVHReader('test_bvh_data.bvh')
        cls._reader.read()

    def setUp(self):
        self._skeleton = Skeleton(self._reader, 2)

    def test_root_name(self):

        name = 'Hips'
        self.assertEqual(self._skeleton.root.name, name)

    def test_root_transform_parent(self):
        transform_parent = mat4().identity()
        self.assertEqual(self._skeleton.root.transform_parent, transform_parent)

    def test_root_children_size(self):
        self.assertEqual(len(self._skeleton.root.children), 3)

    def test_root_children_names(self):
        names = ['Spine1', 'LeftUpLeg', 'RightUpLeg']
        children_names = [
            self._skeleton.root.children[0].name,
            self._skeleton.root.children[1].name,
            self._skeleton.root.children[2].name,
        ]
        self.assertEqual(children_names, names)

    def test_root_transform(self):
        transform = mat4(
            0, 1, 0, 0,
            0, 0, -1, 0,
            -1, 0, 0, 0,
            0, 0, 0, 1
        )

        TestUtility().assertAlmostEqual_mat4(transform, self._skeleton.root.transform, 12)


class TestJoint(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._reader = BVHReader('test_bvh_data.bvh')
        cls._reader.read()

    def test_constructor_name(self):
        joint = Joint('joint name')
        self.assertEqual(joint.name, 'joint name')

    def test_constructor_no_name(self):
        joint = Joint()
        self.assertEqual(joint.name, '')

    def test_constructor_transform_parent(self):
        joint = Joint()
        mat = mat4()
        self.assertEqual(joint.transform_parent, mat)

    def test_constructor_transform(self):
        joint = Joint()
        mat = mat4()
        self.assertEqual(joint.transform, mat)

    def test_constructor_children_is_empty(self):
        joint = Joint()
        self.assertEqual(len(joint.children), 0)

    