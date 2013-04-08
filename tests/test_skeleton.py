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

    def test_frame_number(self):
        frame_number = 2
        self.assertEqual(self._skeleton._frame_number, frame_number)

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

    def test_add_children_no_children(self):
        joint = Joint()
        children = []
        self._skeleton.add_children(joint, children)
        self.assertEqual(len(joint.children), 0)

    def test_add_children_multiple_children_len(self):
        self.assertEqual(len(self._skeleton.root.children), 3)

    def test_add_children_multiple_children_parent_transforms(self):
        expected_transforms = [
            self._skeleton.root.transform,
            self._skeleton.root.transform,
            self._skeleton.root.transform
        ]
        actual_transforms = [
            self._skeleton.root.children[0].transform_parent,
            self._skeleton.root.children[1].transform_parent,
            self._skeleton.root.children[2].transform_parent
        ]
        self.assertEqual(actual_transforms, expected_transforms)

    def test_add_children_parent_transform_nested(self):
        expected_transform = self._skeleton.root.children[0].transform
        actual_transform = self._skeleton.root.children[0].children[0].transform_parent
        self.assertEqual(actual_transform, expected_transform)

    def test_add_children_name_end_site(self):
        name = 'End Site'
        joint = self._skeleton.root.children[1].children[0]
        self.assertEqual(joint.name, name)

    def test_add_children_transform_nested(self):
        expected_transform = mat4(
            0, 0, 1, 0,
            1, 0, 0, 0,
            0, 1, 0, -3,
            0, 0, 0, 1
        )
        actual_transform = self._skeleton.root.children[1].children[0].transform
        TestUtility().assertAlmostEqual_mat4(actual_transform, expected_transform)


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