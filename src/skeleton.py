from math import pi, sin, cos

from cgkit.cgtypes import mat4


__author__ = 'Erik S Carlsten'


class Skeleton:
    def __init__(self, bvh_reader, frame_number):
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

        Skeleton.add_children(self.root, bvh_reader.root.children, frame_number)

    @staticmethod
    def add_children(parent, children, frame_number):
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
                    'x': child.vtx.values[frame_number].v * pi / 180,
                    'y': child.vty.values[frame_number].v * pi / 180,
                    'z': child.vtz.values[frame_number].v * pi / 180,
                }

            new_child.build_transform_matrix(translation, rotation)
            parent.children.append(new_child)
            Skeleton.add_children(new_child, child.children, frame_number)


class Joint:
    def __init__(self, name=''):
        self.name = name
        self.transform_parent = mat4()
        self.transform = mat4()
        self.children = []

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