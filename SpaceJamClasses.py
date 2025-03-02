from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import *
from direct.task import Task
from CollideObjectBase import *


class Planet(SphereCollidableObject):
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, pos_vec: Vec3,
                 scale_vec: float, tex_path: str = None):
        super(Planet, self).__init__(loader, model_path, parent_node, node_name, Vec3(0, 0, 0), 1.04)
        self.model_node.setPos(pos_vec)
        self.model_node.setScale(scale_vec)
        self.model_node.setName(node_name)

        if tex_path:
            texture = loader.loadTexture(tex_path)
            self.model_node.setTexture(texture, 1)


class Universe(InverseSphereCollidableObject):
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, pos_vec: Vec3,
                 scale_vec: float, tex_path: str = None):
        super(Universe, self).__init__(loader, model_path, parent_node, node_name, Vec3(0, 0, 0), 0.9)
        self.model_node.setPos(pos_vec)
        self.model_node.setScale(scale_vec)
        self.model_node.setName(node_name)

        if tex_path:
            texture = loader.loadTexture(tex_path)
            self.model_node.setTexture(texture, 1)


class SpaceStation(CapsuleCollidableObject):
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, pos_vec: Vec3,
                 scale_vec: float, tex_path: str = None):
        super(SpaceStation, self).__init__(loader, model_path, parent_node, node_name, 1, -1, 5, 1, -1, -5, 10)
        self.model_node.setPos(pos_vec)
        self.model_node.setScale(scale_vec)
        self.model_node.setName(node_name)

        if tex_path:
            texture = loader.loadTexture(tex_path)
            self.model_node.setTexture(texture, 1)


class Drone(SphereCollidableObject):
    # How many drones have been spawned
    drone_count = 0

    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, pos_vec: Vec3,
                 scale_vec: float, tex_path: str = None):
        super(Drone, self).__init__(loader, model_path, parent_node, node_name, Vec3(0, 0, 0), 2)
        self.model_node.setPos(pos_vec)
        self.model_node.setScale(scale_vec)
        self.model_node.setName(node_name)

        if tex_path:
            texture = loader.loadTexture(tex_path)
            self.model_node.setTexture(texture, 1)
