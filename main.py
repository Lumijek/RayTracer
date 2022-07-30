import sys
import math
import numpy as np
import os
from tqdm import tqdm
from random import uniform
from utils.color import write_color
from utils.vec3 import Vec3, Color, Point3
from utils.ray import Ray
from utils.hittable_list import HittableList
from utils.hittable import HitRecord
from utils.sphere import Sphere
from utils.camera import Camera
from utils.material import Lambertian, Metal, Dielectric


def ray_color(r, world, depth):
    rec = HitRecord()
    if depth <= 0:
        return Color(0, 0, 0)
    if (world.hit(r, 0.001, np.inf, rec)):
        scattered = Ray(Point3(), Vec3())
        attenuation = Color(0, 0, 0)
        if(rec.mat.scatter(r, rec, attenuation, scattered)):
            return attenuation * ray_color(scattered, world, depth - 1)
    unit_direction = r.direction().unit_vector()
    t = 0.5 * (unit_direction.y() + 1)
    return Color(1, 1, 1) * (1 - t) + Color(0.5, 0.7, 1) * t

def random_scene():
    world = HittableList()

    ground_material = Lambertian(Color(0.5, 0.5, 0.5))
    world.add(Sphere(Point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = uniform(0, 1)
            center = Point3(a + 0.9 * uniform(0, 1), 0.2, b + 0.9 * uniform(0, 1))

            if ((center - Point3(4, 0.2, 0)).length() > 0.9):
                if choose_mat < 0.8:
                    albedo = Color().rand()
                    sphere_material = Lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))

                elif choose_mat < 0.95:
                    albedo = Color().rand(0.5, 1)
                    fuzz = uniform(0, 0.5)
                    sphere_material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))

                else:
                    sphere_material = Dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1 = Dielectric(1.5)
    world.add(Sphere(Point3(0, 1, 0), 1, material1))

    material2 = Lambertian(Color(0.4, 0.2, 0.1))
    world.add(Sphere(Point3(-4, 1, 0), 1, material2))

    material3 = Metal(Color(0.7, 0.6, 0.5), 0)
    world.add(Sphere(Point3(4, 1, 0), 1, material3))

    return world

def main():

    # Image

    aspect_ratio = 3 / 2
    image_width = 400
    image_height = int(image_width / aspect_ratio)
    samples_per_pixel = 100
    max_depth = 50

    # World

    world = random_scene()

    # Camera

    lookfrom = Point3(13, 2, 3)
    lookat = Point3(0, 0, 0)
    vup = Vec3(0, 1, 0)
    dist_to_focus = 10
    aperture = 0.1
    cam = Camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus)

    f = open("image.ppm", "w")
    f.write(f"P3\n{image_width} {image_height}\n255\n")

    for j in tqdm(range(image_height - 1, -1, -1)):
        for i in tqdm(range(image_width)):
            pixel_color = Color(0, 0, 0)
            for _ in range(samples_per_pixel):
                u = (i + uniform(0, 1)) / (image_width - 1)
                v = (j + uniform(0, 1)) / (image_height - 1)
                r = cam.get_ray(u, v)
                pixel_color += ray_color(r, world, max_depth)
            write_color(f, pixel_color, samples_per_pixel)

    f.close()
    os.system("open image.ppm")


main()
