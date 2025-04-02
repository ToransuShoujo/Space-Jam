from direct.showbase.ShowBase import ShowBase
import DefensePaths as defensePaths
import SpaceJamClasses as spaceJamClasses
import Player as player
from panda3d.core import CollisionTraverser, CollisionHandlerPusher, AmbientLight


class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        self.SetupScene()
        self.SetupDrones()
        self.SetCamera()
        self.SetupLighting()

        self.cTrav.traverse(self.render)
        self.pusher.addCollider(self.Spaceship.collisionNode, self.Spaceship.modelNode)
        self.cTrav.addCollider(self.Spaceship.collisionNode, self.pusher)
        # self.cTrav.showCollisions(self.render)

    def SetupScene(self):
        self.Universe = spaceJamClasses.Universe(self.loader, "./Assets/Universe/Universe.x", self.render, 'Universe',
                                                 "./Assets/Universe/Universe.jpg", (0, 0, 0), 15000)
        self.Planet1 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet1',
                                              "./Assets/Planets/barren.png", (150, 5000, 67), 350)
        self.Planet2 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet2',
                                              "./Assets/Planets/gaseous.png", (3750, 2000, 600), 450)
        self.Planet3 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet3',
                                              "./Assets/Planets/marshy.png", (-4600, 1600, 432), 220)
        self.Planet4 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet4',
                                              "./Assets/Planets/martian.png", (-2300, -800, -35), 157)
        self.Planet5 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet5',
                                              "./Assets/Planets/sandy.png", (-2600, -4000, 67), 400)
        self.Planet6 = spaceJamClasses.Planet(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Planet6',
                                              "./Assets/Planets/snowy.png", (-3900, 3570, -232), 350)
        self.Sun = spaceJamClasses.Sun(self.loader, "./Assets/Planets/protoPlanet.x", self.render, 'Sun',
                                       "./Assets/Planets/sun.jpg", (0, 0, 0),500)
        self.SpaceStation = spaceJamClasses.SpaceStation(self.loader, "./Assets/Space Station/spaceStation.egg",
                                                         self.render, 'Space Station',
                                                         "./Assets/Space Station/SpaceStation1_Dif2.png",
                                                         (600, -2400, 0), 25)
        self.Spaceship = player.Spaceship(self.loader, self.taskMgr, self.accept, self.cTrav, self.camera,
                                          "./Assets/Spaceship/Dumbledore.egg", self.render, "Spaceship",
                                          "./Assets/Spaceship/spacejet_C.png", (800, 800, 0), 75)
        self.Sentinal1 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj",
                                                 self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png",
                                                 self.Planet3, 900, "MLB", self.Spaceship)
        self.Sentinal2 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj",
                                                 self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png",
                                                 self.Planet4, 500, "Cloud", self.Spaceship)
        self.Sentinal3 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj",
                                                 self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png",
                                                 self.Planet5, 700, "MLB", self.Spaceship)
        self.Sentinal4 = spaceJamClasses.Orbiter(self.loader, self.taskMgr, "./Assets/Drone Defender/DroneDefender.obj",
                                                 self.render, "Drone", 6.0, "./Assets/Drone Defender/octotoad1_auv.png",
                                                 self.Planet6, 400, "Cloud", self.Spaceship)

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius=1):
        unitVec = defensePaths.BaseballSeams(step, numSeams, B=0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName,
                              "./Assets/Drone Defender/octotoad1_auv.png", position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = defensePaths.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName,
                              "./Assets/Drone Defender/octotoad1_auv.png", position, 10)

    def DrawRotateX(self, centralObject, droneName, step, numDrones, radius):
        unitVec = defensePaths.RotateX(step, numDrones, radius)
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName,
                              "./Assets/Drone Defender/octotoad1_auv.png", position, 10)

    def DrawRotateY(self, centralObject, droneName, step, numDrones, radius):
        unitVec = defensePaths.RotateY(step, numDrones, radius)
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName,
                              "./Assets/Drone Defender/octotoad1_auv.png", position, 10)

    def DrawRotateZ(self, centralObject, droneName, step, numDrones, radius):
        unitVec = defensePaths.RotateZ(step, numDrones, radius)
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        spaceJamClasses.Drone(self.loader, "./Assets/Drone Defender/DroneDefender.obj", self.render, droneName,
                              "./Assets/Drone Defender/octotoad1_auv.png", position, 10)

    def SetupDrones(self):
        fullCycle = 60

        for j in range(fullCycle):
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)
            self.DrawCloudDefense(self.Planet1, nickName)
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)
            self.DrawBaseballSeams(self.SpaceStation, nickName, j, fullCycle, 2)
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)
            self.DrawRotateX(self.Planet2, nickName, j, fullCycle, 50)
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)
            self.DrawRotateY(self.Planet2, nickName, j, fullCycle, 50)
            spaceJamClasses.Drone.droneCount += 1
            nickName = "Drone" + str(spaceJamClasses.Drone.droneCount)
            self.DrawRotateZ(self.Planet2, nickName, j, fullCycle, 50)
            spaceJamClasses.Drone.droneCount += 1

    def SetCamera(self):
        self.disableMouse()
        self.camera.reparentTo(self.Spaceship.modelNode)
        self.camera.setFluidPos(0, 0.22, 0)

    def SetupLighting(self):
        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor((0.4, 0.4, 0.4, 1))
        ambientLightNP = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNP)


app = MyApp()
app.run()
