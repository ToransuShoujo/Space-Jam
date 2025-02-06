from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.setup_scene()

    def setup_scene(self):
        self.universe = self.loader.loadModel('./Assets/Universe/Universe.x')
        self.universe_texture = self.loader.loadTexture('./Assets/Universe/Universe.jpg')
        self.universe.reparentTo(self.render)
        self.universe.setScale(15000)
        self.universe.setTexture(self.universe_texture, 1)

        self.planet1 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.planet1_texture = self.loader.loadTexture('./Assets/Planets/barren.png')
        self.planet1.reparentTo(self.render)
        self.planet1.setPos(150, 5000, 67)
        self.planet1.setScale(350)
        self.planet1.setTexture(self.planet1_texture, 1)

        self.planet2 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.planet2_texture = self.loader.loadTexture('./Assets/Planets/gaseous.png')
        self.planet2.reparentTo(self.render)
        self.planet2.setPos(3750, 2000, 600)
        self.planet2.setScale(450)
        self.planet2.setTexture(self.planet2_texture, 1)

        self.planet3 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.planet3_texture = self.loader.loadTexture('./Assets/Planets/marshy.png')
        self.planet3.reparentTo(self.render)
        self.planet3.setPos(-4600, 1600, 432)
        self.planet3.setScale(220)
        self.planet3.setTexture(self.planet3_texture, 1)

        self.planet4 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.planet4_texture = self.loader.loadTexture('./Assets/Planets/martian.png')
        self.planet4.reparentTo(self.render)
        self.planet4.setPos(-2300, -800, -35)
        self.planet4.setScale(157)
        self.planet4.setTexture(self.planet4_texture, 1)

        self.planet5 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.planet5_texture = self.loader.loadTexture('./Assets/Planets/sandy.png')
        self.planet5.reparentTo(self.render)
        self.planet5.setPos(-2600, -4000, 67)
        self.planet5.setScale(400)
        self.planet5.setTexture(self.planet5_texture, 1)

        self.planet6 = self.loader.loadModel('./Assets/Planets/protoPlanet.x')
        self.planet6_texture = self.loader.loadTexture('./Assets/Planets/snowy.png')
        self.planet6.reparentTo(self.render)
        self.planet6.setPos(-3900, 3570, -232)
        self.planet6.setScale(350)
        self.planet6.setTexture(self.planet6_texture, 1)

        self.space_station = self.loader.loadModel('./Assets/Space Station/spaceStation.egg')
        self.space_station.reparentTo(self.render)
        self.space_station.setPos(600, -2400, 0)
        self.space_station.setScale(25)

        self.spaceship = self.loader.loadModel('./Assets/Spaceship/Dumbledore.egg')
        self.spaceship.reparentTo(self.render)
        self.spaceship.setPos(800, 800, 0)
        self.spaceship.setScale(75)

app = MyApp()
app.run()