import math, random
from panda3d.core import *


def cloud(radius=1):
    x = 2 * random.random() - 1
    y = 2 * random.random() - 1
    z = 2 * random.random() - 1

    unit_vec = Vec3(x, y, z)
    unit_vec.normalize()

    return unit_vec * radius


def baseball_seams(step, num_seams, b, f=1):
    time = step / float(num_seams) * 2 * math.pi

    f4 = 0

    r = 1

    xxx = math.cos(time) - b * math.cos(3 * time)
    yyy = math.sin(time) + b * math.sin(3 * time)
    zzz = f * math.cos(2 * time) + f4 * math.cos(4 * time)

    rrr = math.sqrt(xxx ** 2 + yyy ** 2 + zzz ** 2)

    x = r * xxx / rrr
    y = r * yyy / rrr
    z = r * zzz / rrr

    return Vec3(x, y, z)


def rotate_x(step, num_drones, radius):
    theta = math.radians(step * (360 / num_drones))
    unit_vec = Vec3(radius * math.cos(theta), radius * math.sin(theta), 0.0)

    return unit_vec


def rotate_y(step, num_drones, radius):
    theta = math.radians(step * (360 / num_drones))
    unit_vec = Vec3(0.0, radius * math.sin(theta), radius * math.cos(theta))

    return unit_vec


def rotate_z(step, num_drones, radius):
    theta = math.radians(step * (360 / num_drones))
    unit_vec = Vec3(radius * math.cos(theta), 0.0, radius * math.sin(theta))

    return unit_vec
