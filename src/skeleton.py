__author__ = 'Erik S Carlsten'

from cgkit.cgtypes import mat4
from cgkit import bvhimport


class Skeleton:
    def __init__(self, bvh_importer):
        pass


class Joint:
    def __init__(self):
        self.transform_parent = mat4(1.0)
        self.transform = mat4(1.0)
        self.children = []