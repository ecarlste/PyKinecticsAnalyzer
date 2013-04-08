from math import pi, sin, cos

from cgkit.cgtypes import mat4


__author__ = 'Erik S Carlsten'


class Skeleton:
    def __init__(self, bvh_reader, frame_number):
        self._frame_number = frame_number
        self.root = Joint(bvh_reader.root.name)
        self.root.transform_parent = mat4().identity()

        translation = {
            'x': bvh_reader.root.offset[0] + bvh_reader.root.vtpos.values[frame_number].v.x,
            'y': bvh_reader.root.offset[1] + bvh_reader.root.vtpos.values[frame_number].v.y,
            'z': bvh_reader.root.offset[2] + bvh_reader.root.vtpos.values[frame_number].v.z,
        }

        rotation = {
            'x': bvh_reader.root.vtx.values[frame_number].v * pi / 180,
            'y': bvh_reader.root.vty.values[frame_number].v * pi / 180,
            'z': bvh_reader.root.vtz.values[frame_number].v * pi / 180,
        }

        self.root.build_transform_matrix(translation, rotation)

        self.add_children(self.root, bvh_reader.root.children)

    def __eq__(self, other):
        return self.root == other.root

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
    def __init__(self, name=''):
        self.name = name
        self.transform_parent = mat4()
        self.transform = mat4()
        self.children = []

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