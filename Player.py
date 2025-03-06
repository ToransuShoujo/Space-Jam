from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3, TransparencyAttrib
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage


class Spaceship(SphereCollideObject):
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str,
                 parentNode: NodePath, nodeName: str, texPath: str, posVec: Vec3,
                 scaleVec: float):
        super(Spaceship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.85)
        self.taskMgr = taskMgr
        self.accept = accept
        self.render = parentNode
        self.loader = loader
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)
        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.SetKeyBindings()

        self.reloadTime = .25
        self.missileDistance = 4000  # Distance until the missile explodes.
        self.missileBay = 1  # One missile in the missile bay to be launched.

        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)

        self.EnableHUD()

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

    def Fire(self):
        if self.missileBay:
            travRate = self.missileDistance
            aim = self.render.getRelativeVector(self.modelNode,
                                                Vec3.forward())  # The direction the spaceship is facing.
            aim.normalize()
            fireSolution = aim * travRate
            inFront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()
            self.missileBay -= 1
            tag = 'Missile' + str(Missile.missileCount)
            posVec = self.modelNode.getPos() + inFront  # Spawn the missile in front of the node of the ship
            currentMissile = Missile(self.loader, './Assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0)
            Missile.intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos=posVec, fluid=1)
            Missile.intervals[tag].start()
        else:
            # If we aren't reloading, we want to start reloading.
            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                # Call the reload method on no delay.
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont

    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1
            print('Reload complete.')
            if self.missileBay > 1:
                self.missileBay = 1
            return Task.done
        elif task.time <= self.reloadTime:
            print('Reload proceeding...')
            return Task.cont

    def CheckIntervals(self, task):
        for i in Missile.intervals:
            # isPlaying returns true or false to see if the missile has gotten to the end of its path.
            if not Missile.intervals[i].isPlaying():
                # If its path is done, we get rid of everything to do with this missile.
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                print(i + ' has reached the end of its fire solution.')
                # We break because when things are deleted from a dictionary, we have to refactor the dictionary so that we can reuse it. When we delete things, there is a gap at that point.
                break

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
        self.accept('f', self.Fire)

    def EnableHUD(self):
        self.Hud = OnscreenImage(image='./Assets/Hud/Reticle3b.png', pos=Vec3(0, 0, 0), scale=0.1)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)
