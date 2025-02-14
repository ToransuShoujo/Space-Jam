from direct.showbase.ShowBase import ShowBase
from panda3d.core import *


class Model(ShowBase):
    # tex_path is optional here because sometimes, like in the event of using a .egg file, you do not need to provide one.
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, pos_vec: Vec3,
                 scale_vec: float, tex_path: str = None):
        self.model_node = loader.loadModel(model_path)
        self.model_node.reparentTo(parent_node)
        self.model_node.setPos(pos_vec)
        self.model_node.setScale(scale_vec)
        self.model_node.setName(node_name)

        if tex_path:
            texture = loader.loadTexture(tex_path)
            self.model_node.setTexture(texture, 1)


class Planet(Model):
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, pos_vec: Vec3,
                 scale_vec: float, tex_path: str = None):
        super().__init__(loader, model_path, parent_node, node_name, pos_vec, scale_vec, tex_path)


class Universe(Model):
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, pos_vec: Vec3,
                 scale_vec: float, tex_path: str = None):
        super().__init__(loader, model_path, parent_node, node_name, pos_vec, scale_vec, tex_path)


class SpaceStation(Model):
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, pos_vec: Vec3,
                 scale_vec: float, tex_path: str = None):
        super().__init__(loader, model_path, parent_node, node_name, pos_vec, scale_vec, tex_path)


class Spaceship(Model):
    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, pos_vec: Vec3,
                 scale_vec: float, tex_path: str = None):
        super().__init__(loader, model_path, parent_node, node_name, pos_vec, scale_vec, tex_path)


class Drone(Model):
    # How many drones have been spawned
    drone_count = 0

    def __init__(self, loader: Loader, model_path: str, parent_node: NodePath, node_name: str, pos_vec: Vec3,
                 scale_vec: float, tex_path: str = None):
        super().__init__(loader, model_path, parent_node, node_name, pos_vec, scale_vec, tex_path)