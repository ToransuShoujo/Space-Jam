from direct.showbase.ShowBase import ShowBase
from SpaceJamClasses import *
from DefensePaths import *


class MyApp(ShowBase):
    def __init__(self):
        full_cycle = 60

        ShowBase.__init__(self)
        self.setup_scene()

        for j in range(full_cycle):
            Drone.drone_count += 1
            nickname = 'Drone' + str(Drone.drone_count)

            self.draw_cloud_defense(self.planet1, nickname)
            self.draw_rotate_x(self.planet2, nickname, j, full_cycle, 50.0)
            self.draw_rotate_y(self.planet2, nickname, j, full_cycle, 50.0)
            self.draw_rotate_z(self.planet2, nickname, j, full_cycle, 50.0)
            self.draw_baseball_seams(self.space_station, nickname, j, full_cycle, 2)

    def setup_scene(self):
        self.universe = Universe(self.loader, './Assets/Universe/Universe.x', self.render, 'Universe',
                                 Vec3(0, 0, 0), 15000, './Assets/Universe/Universe.jpg')
        self.planet1 = Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet 1',
                              Vec3(150, 5000, 67), 350, './Assets/Planets/barren.png')
        self.planet2 = Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet 2',
                              Vec3(3750, 2000, 600), 450, './Assets/Planets/gaseous.png')
        self.planet3 = Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet 3',
                              Vec3(-4600, 1600, 432), 220, './Assets/Planets/marshy.png')
        self.planet4 = Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet 4',
                              Vec3(-2300, -800, -35), 157, './Assets/Planets/martian.png')
        self.planet5 = Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet 5',
                              Vec3(-2600, -4000, 67), 400, './Assets/Planets/sandy.png')
        self.planet6 = Planet(self.loader, './Assets/Planets/protoPlanet.x', self.render, 'Planet 6',
                              Vec3(-3900, 3570, -232), 350, './Assets/Planets/snowy.png')
        self.space_station = SpaceStation(self.loader, './Assets/Space Station/spaceStation.egg', self.render,
                                          'Space Station', Vec3(600, -2400, 0), 25)
        self.spaceship = Spaceship(self.loader, './Assets/Spaceship/Dumbledore.egg', self.render, 'Spaceship',
                                   Vec3(800, 800, 0), 75)

    def draw_baseball_seams(self, central_object, drone_name, step, num_seams, radius=1):
        unit_vec = baseball_seams(step, num_seams, b=0.4)
        unit_vec.normalize()
        position = unit_vec * radius * 250 + central_object.model_node.getPos()
        Drone(self.loader, './Assets/Drone Defender/DroneDefender.obj', self.render, drone_name, position, 5,
              './Assets/Drone Defender/octotoad1_auv.png')

    def draw_cloud_defense(self, central_object, drone_name):
        unit_vec = cloud()
        unit_vec.normalize()
        position = unit_vec * 500 + central_object.model_node.getPos()
        Drone(self.loader, './Assets/Drone Defender/DroneDefender.obj', self.render, drone_name, position, 10,
              './Assets/Drone Defender/octotoad1_auv.png')

    def draw_rotate_x(self, central_object, drone_name, step, num_drones, radius):
        unit_vec = rotate_x(step, num_drones, radius)
        unit_vec.normalize()
        position = unit_vec * 500 + central_object.model_node.getPos()
        Drone(self.loader, './Assets/Drone Defender/DroneDefender.obj', self.render, drone_name, position, 5,
              './Assets/Drone Defender/octotoad1_auv.png')

    def draw_rotate_y(self, central_object, drone_name, step, num_drones, radius):
        unit_vec = rotate_y(step, num_drones, radius)
        unit_vec.normalize()
        position = unit_vec * 500 + central_object.model_node.getPos()
        Drone(self.loader, './Assets/Drone Defender/DroneDefender.obj', self.render, drone_name, position, 5,
              './Assets/Drone Defender/octotoad1_auv.png')

    def draw_rotate_z(self, central_object, drone_name, step, num_drones, radius):
        unit_vec = rotate_z(step, num_drones, radius)
        unit_vec.normalize()
        position = unit_vec * 500 + central_object.model_node.getPos()
        Drone(self.loader, './Assets/Drone Defender/DroneDefender.obj', self.render, drone_name, position, 5,
              './Assets/Drone Defender/octotoad1_auv.png')


app = MyApp()
app.run()
