__author__ = 'Erik S Carlsten'

from cgkit.cgtypes import mat4


class Skeleton:
    def __init__(self, bvh_reader, frame_number):
        self.root = Joint(bvh_reader.root.name)
        self.root.add_children(bvh_reader.root.children)


class Joint:
    def __init__(self, name):
        self.name = name
        self.transform_parent = mat4()
        self.transform = mat4()
        self.children = []

    def set_transform_parent(self, transform_matrix):
        assert isinstance(transform_matrix, mat4)
        self.transform_parent = transform_matrix

    def set_transform(self, transform_matrix):
        assert isinstance(transform_matrix, mat4)
        self.transform = transform_matrix

    def add_children(self, children):
        for child in children:
            new_child = Joint(child.name)
            self.add_child(new_child)
            new_child.add_children(child.children)

    def add_child(self, child):
        assert isinstance(child, Joint)
        self.children.append(child)