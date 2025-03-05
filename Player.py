from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task


class Spaceship(SphereCollideObject):
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str,
                 parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3,
                 scaleVec: float):
        super(Spaceship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 2)
        self.taskMgr = taskMgr
        self.accept = accept
        self.render = parentNode
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.SetKeyBindings()

    def Thrust(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, 'forward-thrust')
        else:
            self.taskMgr.remove('forward-thrust')

    def ApplyThrust(self, task):
        rate = 5

        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        trajectory.normalize()
        self.modelNode.setFluidPos(self.modelNode.getPos() + trajectory * rate)

        return Task.cont

    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn, 'left-turn')
        else:
            self.taskMgr.remove('left-turn')

    def ApplyLeftTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.modelNode.setH(self.modelNode.getH() + rate)

        return Task.cont

    def RightTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn, 'right-turn')
        else:
            self.taskMgr.remove('right-turn')

    def ApplyRightTurn(self, task):
        # Half a degree every frame.
        rate = .5
        self.modelNode.setH(self.modelNode.getH() - rate)

        return Task.cont

    def LookUp(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLookUp, 'look-up')
        else:
            self.taskMgr.remove('look-up')

    def ApplyLookUp(self, task):
        rate = .4
        self.modelNode.setP(self.modelNode.getP() + rate)

        return Task.cont

    def LookDown(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLookDown, 'look-down')
        else:
            self.taskMgr.remove('look-down')

    def ApplyLookDown(self, task):
        rate = .4
        self.modelNode.setP(self.modelNode.getP() - rate)

        return Task.cont

    def RollLeft(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRollLeft, 'roll-left')
        else:
            self.taskMgr.remove('roll-left')

    def ApplyRollLeft(self, task):
        rate = .25
        self.modelNode.setR(self.modelNode.getR() - rate)

        return Task.cont

    def RollRight(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRollRight, 'roll-right')
        else:
            self.taskMgr.remove('roll-right')

    def ApplyRollRight(self, task):
        rate = .25
        self.modelNode.setR(self.modelNode.getR() + rate)

        return Task.cont

    def SetKeyBindings(self):
        # All of our key bindings for our spaceship's movement
        self.accept('space', self.Thrust, [1])
        self.accept('space-up', self.Thrust, [0])
        self.accept('a', self.LeftTurn, [1])
        self.accept('a-up', self.LeftTurn, [0])
        self.accept('d', self.RightTurn, [1])
        self.accept('d-up', self.RightTurn, [0])
        self.accept('w', self.LookUp, [1])
        self.accept('w-up', self.LookUp, [0])
        self.accept('s', self.LookDown, [1])
        self.accept('s-up', self.LookDown, [0])
        self.accept('q', self.RollLeft, [1])
        self.accept('q-up', self.RollLeft, [0])
        self.accept('e', self.RollRight, [1])
        self.accept('e-up', self.RollRight, [0])
