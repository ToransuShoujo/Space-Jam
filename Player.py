from direct.showbase.ShowBaseGlobal import aspect2d
from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3, TransparencyAttrib, CollisionTraverser, Point3, TextNode
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionHandlerEvent
from direct.interval.LerpInterval import LerpFunc
from direct.particles.ParticleEffect import ParticleEffect
from direct.interval.IntervalGlobal import Sequence
import re


class Spaceship(SphereCollideObject):
    def __init__(self, loader: Loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None],
                 traverser: CollisionTraverser, camera: NodePath, modelPath: str, parentNode: NodePath, nodeName: str,
                 texPath: str, posVec: Vec3, scaleVec: float):
        super(Spaceship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1)
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

        self.reloadTime = .75
        self.missileDistance = 4000  # Distance until the missile explodes.
        self.missileBay = 2 # Two missiles in the missile bay to be launched.

        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)

        self.EnableHUD()

        self.cntExplode = 0
        self.explodeIntervals = {}

        self.traverser = traverser

        self.handler = CollisionHandlerEvent()

        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)

        self.camera = camera
        self.firstPerson = True

        self.ammoText = TextNode('Ammo')
        self.ammoText.setText('Ammo: ' + str(self.missileBay))
        self.ammoTextPath = aspect2d.attachNewNode(self.ammoText)
        self.ammoTextPath.setScale(0.07)
        self.ammoTextPath.setPos((0.75, 0, -0.75))

        self.missilesFired = 0
        self.missilesFiredText = TextNode('MissilesFired')
        self.missilesFiredText.setText('Missiles Fired: ' + str(self.missilesFired))
        self.missilesFiredTextPath = aspect2d.attachNewNode(self.missilesFiredText)
        self.missilesFiredTextPath.setScale(0.07)
        self.missilesFiredTextPath.setPos((0.53, 0, -0.85))

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

    def BackThrust(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyBackThrust, 'backward-thrust')
        else:
            self.taskMgr.remove('backward-thrust')

    def ApplyBackThrust(self, task):
        rate = 5

        trajectory = self.render.getRelativeVector(self.modelNode, Vec3.back())
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
        if self.missileBay == 2:
            self.SpawnMissile(Vec3(40, 10, 0))
            self.SpawnMissile(Vec3(-40, -10, 0))
            self.UpdateAmmoCounter(0)
            self.missilesFired += 2
            self.UpdateMissileCounter()
        else:
            # If we aren't reloading, we want to start reloading.
            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                self.UpdateAmmoCounter("Reloading")
                # Call the reload method on no delay.
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont

    def SpawnMissile(self, positionModifier: Vec3 = Vec3(0, 0, 0)):
        travRate = self.missileDistance
        aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())  # The direction the spaceship is facing.
        aim.normalize()
        fireSolution = aim * travRate
        inFront = aim * 150
        travVec = fireSolution + self.modelNode.getPos() + positionModifier
        self.missileBay -= 1
        tag = 'Missile' + str(Missile.missileCount)
        posVec = self.modelNode.getPos() + inFront + positionModifier  # Spawn the missile in front of the node of the ship
        currentMissile = Missile(self.loader, './Assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0)
        Missile.intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos=posVec, fluid=1)
        Missile.intervals[tag].start()

        self.traverser.addCollider(currentMissile.collisionNode, self.handler)

    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 2
            print('Reload complete.')
            if self.missileBay > 2:
                self.missileBay = 2
            self.UpdateAmmoCounter(self.missileBay)
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

    def HandleInto(self, entry):
        fromNode = entry.getFromNodePath().getName()
        print("fromNode: " + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print("intoNode: " + intoNode)
        intoPosition = Vec3(entry.getSurfacePoint(self.render))
        tempVar = fromNode.split('_')
        print("tempVar: " + str(tempVar))
        shooter = tempVar[0]
        print("Shooter: " + str(shooter))
        tempVar = intoNode.split('-')
        print("tempVar1: " + str(tempVar))
        tempVar = intoNode.split('_')
        print('tempVar2: ' + str(tempVar))
        victim = tempVar[0]
        print("Victim: " + str(victim))
        strippedString = re.sub(r'[0-9]', '', victim)

        if "Drone" in strippedString or "Planet" in strippedString or "Space Station" in strippedString:
            print(victim, ' hit at ', intoPosition)
            self.DestroyObject(victim, intoPosition)

        print(shooter + ' is done.')
        try:
            Missile.intervals[shooter].finish()
        except KeyError:
            print('Could not finish ' + shooter + ' interval.')

    def DestroyObject(self, hitID, hitPosition):
        nodeID = self.render.find(hitID)
        try:
            nodeID.detachNode()
        except AssertionError:
            pass

        self.SetParticles()

        self.explodeNode.setPos(hitPosition)
        self.Explode()

    def Explode(self):
        self.cntExplode += 1
        tag = 'particles-' + str(self.cntExplode)

        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration=4.0)
        self.explodeIntervals[tag].start()

    def ExplodeLight(self, t):
        if t >= 1.0 and self.explodeEffect:
            self.explodeEffect.disable()
            explodeNodes = self.render.findAllMatches('ExplosionEffects')
            explodeNodes[0].removeNode()
        elif t == 0:
            self.explodeEffect.start(self.explodeNode)

    def SetParticles(self):
        base.enableParticles()
        self.explodeEffect = ParticleEffect()
        self.explodeEffect.loadConfig("./Assets/ParticleEffects/basic_xpld_efx.ptf")
        self.explodeEffect.setScale(20)
        self.explodeNode = self.render.attachNewNode('ExplosionEffects')

    def ChangeCamera(self):
        if self.firstPerson:
            self.camera.setFluidPos(0, -20, 2)
            self.firstPerson = False
            self.Hud.destroy()
        else:
            self.camera.setFluidPos(0, 0.22, 0)
            self.firstPerson = True
            self.EnableHUD()

    def BarrelRollLeft(self):
        currentH = self.modelNode.getH()
        currentP = self.modelNode.getP()
        currentR = self.modelNode.getR()
        hprInterval1 = self.modelNode.hprInterval(0.5, Point3(currentH, currentP, currentR - 360),
                                                  startHpr=Point3(currentH, currentP, currentR))
        barrelRoll = Sequence(hprInterval1, name="BarrelRoll")
        barrelRoll.start()

    def BarrelRollRight(self):
        currentH = self.modelNode.getH()
        currentP = self.modelNode.getP()
        currentR = self.modelNode.getR()
        hprInterval1 = self.modelNode.hprInterval(0.5, Point3(currentH, currentP, currentR + 360),
                                                  startHpr=Point3(currentH, currentP, currentR))
        barrelRoll = Sequence(hprInterval1, name="BarrelRoll")
        barrelRoll.start()

    def UpdateAmmoCounter(self, text):
        self.ammoText.setText("Ammo: " + str(text))

    def UpdateMissileCounter(self):
        self.missilesFiredText.setText("Missiles Fired: " + str(self.missilesFired))

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
        self.accept('c', self.ChangeCamera)
        self.accept('1', self.BarrelRollLeft)
        self.accept('3', self.BarrelRollRight)
        self.accept('v', self.BackThrust, [1])
        self.accept('v-up', self.BackThrust, [0])

    def EnableHUD(self):
        self.Hud = OnscreenImage(image='./Assets/Hud/Reticle3b.png', pos=Vec3(0, 0, 0), scale=0.1)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)
