from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import *
from direct.task import Task


class Planet(ShowBase):
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


class Universe(ShowBase):
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


class SpaceStation(ShowBase):
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


class Spaceship(ShowBase):
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

        self.set_key_bindings()

    def thrust(self, key_down):
        if key_down:
            taskMgr.add(self.apply_thrust, 'forward-thrust')
        else:
            taskMgr.remove('forward-thrust')

    def apply_thrust(self, task):
        rate = 5

        trajectory = render.getRelativeVector(self.model_node, Vec3.forward())
        trajectory.normalize()
        self.model_node.setFluidPos(self.model_node.getPos() + trajectory * rate)
        return Task.cont

    def left_turn(self, key_down):
        if key_down:
            taskMgr.add(self.apply_left_turn, 'left-turn')
        else:
            taskMgr.remove('left-turn')

    def apply_left_turn(self, task):
        rate = 0.5

        self.model_node.setH(self.model_node.getH() + rate)
        return Task.cont

    def right_turn(self, key_down):
        if key_down:
            taskMgr.add(self.apply_right_turn, 'right-turn')
        else:
            taskMgr.remove('right-turn')

    def apply_right_turn(self, task):
        rate = 0.5

        self.model_node.setH(self.model_node.getH() - rate)
        return Task.cont

    def look_up(self, key_down):
        if key_down:
            taskMgr.add(self.apply_look_up, 'look-up')
        else:
            taskMgr.remove('look-up')

    def apply_look_up(self, task):
        rate = 0.4

        self.model_node.setP(self.model_node.getP() + rate)
        return task.cont

    def look_down(self, key_down):
        if key_down:
            taskMgr.add(self.apply_look_down, 'look-down')
        else:
            taskMgr.remove('look-down')

    def apply_look_down(self, task):
        rate = 0.4

        self.model_node.setP(self.model_node.getP() - rate)
        return task.cont

    def roll_left(self, key_down):
        if key_down:
            taskMgr.add(self.apply_roll_left, 'roll-left')
        else:
            taskMgr.remove('roll-left')

    def apply_roll_left(self, task):
        rate = 0.25

        self.model_node.setR(self.model_node.getR() - rate)
        return Task.cont

    def roll_right(self, key_down):
        if key_down:
            taskMgr.add(self.apply_roll_right, 'roll-right')
        else:
            taskMgr.remove('roll-right')

    def apply_roll_right(self, task):
        rate = 0.25

        self.model_node.setR(self.model_node.getR() + rate)
        return Task.cont

    def set_key_bindings(self):
        self.accept('space', self.thrust, [1])
        self.accept('space-up', self.thrust, [0])
        self.accept('a', self.left_turn, [1])
        self.accept('a-up', self.left_turn, [0])
        self.accept('d', self.right_turn, [1])
        self.accept('d-up', self.right_turn, [0])
        self.accept('w', self.look_up, [1])
        self.accept('w-up', self.look_up, [0])
        self.accept('s', self.look_down, [1])
        self.accept('s-up', self.look_down, [0])
        self.accept('q', self.roll_left, [1])
        self.accept('q-up', self.roll_left, [0])
        self.accept('e', self.roll_right, [1])
        self.accept('e-up', self.roll_right, [0])


class Drone(ShowBase):
    # How many drones have been spawned
    drone_count = 0

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
