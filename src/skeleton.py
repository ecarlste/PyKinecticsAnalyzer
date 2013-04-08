from math import pi, sin, cos

from cgkit.cgtypes import mat4
from cgkit.bvhimport import BVHReader


__author__ = 'Erik S Carlsten'


class Skeleton:
    def __init__(self, other=None, frame_number=None):
        if isinstance(other, BVHReader) and isinstance(frame_number, int):
            self._frame_number = frame_number
            self._root = Joint(other.root.name)
            self._root.transform_parent = mat4().identity()

            translation = {
                'x': other.root.offset[0] + other.root.vtpos.values[frame_number].v.x,
                'y': other.root.offset[1] + other.root.vtpos.values[frame_number].v.y,
                'z': other.root.offset[2] + other.root.vtpos.values[frame_number].v.z,
            }

            rotation = {
                'x': other.root.vtx.values[frame_number].v * pi / 180,
                'y': other.root.vty.values[frame_number].v * pi / 180,
                'z': other.root.vtz.values[frame_number].v * pi / 180,
            }

            self._root.build_transform_matrix(translation, rotation)

            self.add_children(self._root, other.root.children)
        elif isinstance(other, Skeleton):
            self._frame_number = other._frame_number
            self._root = Joint(other._root)

    def __eq__(self, other):
        return self._root == other._root

    def add_children(self, parent, children):
        for child in children:
            new_child = Joint(child.name)
            new_child.transform_parent = mat4(parent.transform)

            translation = {
                'x': child.offset[0],
                'y': child.offset[1],
                'z': child.offset[2],
            }

            if child.name == 'End Site':
                rotation = {'x': 0, 'y': 0, 'z': 0}
            else:
                rotation = {
                    'x': child.vtx.values[self._frame_number].v * pi / 180,
                    'y': child.vty.values[self._frame_number].v * pi / 180,
                    'z': child.vtz.values[self._frame_number].v * pi / 180,
                }

            new_child.build_transform_matrix(translation, rotation)
            parent.children.append(new_child)
            self.add_children(new_child, child.children)


class Joint:
    def __init__(self, other=''):
        self.children = []

        if isinstance(other, basestring):
            self.name = other
            self.transform_parent = mat4()
            self.transform = mat4()
        elif isinstance(other, Joint):
            self.name = other.name
            self.transform_parent = mat4(other.transform_parent)
            self.transform = mat4(other.transform)

            for child in other.children:
                self.children.append(Joint(child))

    def __eq__(self, other):
        are_equal =\
            self.name == other.name and self.transform_parent == other.transform_parent and\
            self.transform == other.transform and self.children == other.children

        return are_equal

    def build_transform_matrix(self, translation, rotation):
        theta_x = rotation['x']
        rotation_matrix_x = mat4(
            1, 0, 0, 0,
            0, cos(theta_x), -sin(theta_x), 0,
            0, sin(theta_x), cos(theta_x), 0,
            0, 0, 0, 1
        )

        theta_y = rotation['y']
        rotation_matrix_y = mat4(
            cos(theta_y), 0, -sin(theta_y), 0,
            0, 1, 0, 0,
            sin(theta_y), 0, cos(theta_y), 0,
            0, 0, 0, 1
        )

        theta_z = rotation['z']
        rotation_matrix_z = mat4(
            cos(theta_z), -sin(theta_z), 0, 0,
            sin(theta_z), cos(theta_z), 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1
        )

        rotation_matrix = rotation_matrix_x * rotation_matrix_y * rotation_matrix_z

        translation_matrix = mat4().identity()
        translation_matrix[0, 3] = translation['x']
        translation_matrix[1, 3] = translation['y']
        translation_matrix[2, 3] = translation['z']

        self.transform = self.transform_parent * translation_matrix * rotation_matrix


class SkeletonMotion:
    def __init__(self, bvh_reader):
        self.frame_count = bvh_reader.frames
        self.frame_time = bvh_reader.dt

        self.frames = []
        for frame_number in range(self.frame_count):
            self.frames.append(Skeleton(bvh_reader, frame_number))