__author__ = 'Erik S Carlsten'

from cgkit.cgtypes import mat4
from cgkit import bvhimport


class Skeleton:
    def __init__(self, bvh_importer):
        pass


class Joint:
    def __init__(self):
        self._transform_parent = mat4()
        self._transform = mat4()
        self._children = []

    def set_transform_parent(self, transform_matrix):
        assert isinstance(transform_matrix, mat4)
        self._transform_parent = transform_matrix

    def set_transform(self, transform_matrix):
        assert isinstance(transform_matrix, mat4)
        self._transform = transform_matrix

    def add_child(self, child):
        assert isinstance(child, Joint)
        self._children.append(child)